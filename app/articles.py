import re
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, jsonify, request, send_from_directory, url_for
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from .auth import require_admin
from .extensions import db
from .models import Article, ArticleCategory

bp = Blueprint("articles", __name__)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_IMAGE_BYTES = 400 * 1024
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CATEGORY_KEY_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9-]{0,49}$")


def validate(payload):
    required_localized = ("title", "summary", "author", "alt")
    for field in required_localized:
        value = payload.get(field) or {}
        if not str(value.get("en", "")).strip() or not str(value.get("fa", "")).strip():
            return f"هر دو نسخه فارسی و انگلیسیِ {field} الزامی است."
    slug = str(payload.get("slug", "")).strip()
    if not SLUG_PATTERN.fullmatch(slug):
        return "آدرس مقاله فقط می‌تواند شامل حروف کوچک انگلیسی، عدد و خط تیره باشد."
    if not str(payload.get("image", "")).strip():
        return "تصویر مقاله الزامی است."
    if not payload.get("sections"):
        return "مقاله باید دست‌کم یک بخش داشته باشد."
    if not ArticleCategory.query.filter_by(key=payload.get("category")).first():
        return "دسته‌بندی مقاله معتبر نیست."
    try:
        Article._date(payload.get("datePublished"))
        Article._date(payload.get("dateModified"))
    except (TypeError, ValueError):
        return "تاریخ انتشار یا ویرایش معتبر نیست."
    try:
        minutes = int(payload.get("readingMinutes", 0))
        if not 1 <= minutes <= 120:
            raise ValueError
    except (TypeError, ValueError):
        return "زمان مطالعه باید بین ۱ تا ۱۲۰ دقیقه باشد."
    return None


def ordered_query(query):
    return query.order_by(Article.featured.desc(), Article.date_published.desc(), Article.id.desc())


def keep_single_featured(item):
    if item.featured:
        Article.query.filter(Article.id != item.id).update({Article.featured: False})


@bp.get("/api/articles")
def public_articles():
    items = ordered_query(Article.query.filter_by(published=True)).all()
    return jsonify(articles=[item.to_dict() for item in items])


@bp.get("/api/categories")
def public_categories():
    rows = (
        db.session.query(ArticleCategory, func.count(Article.id))
        .join(Article, Article.category == ArticleCategory.key)
        .filter(Article.published.is_(True))
        .group_by(ArticleCategory.id)
        .order_by(ArticleCategory.id.asc())
        .all()
    )
    return jsonify(categories=[category.to_dict(count) for category, count in rows])


@bp.get("/api/articles/<slug>")
def public_article(slug):
    item = Article.query.filter_by(slug=slug, published=True).first_or_404()
    return jsonify(article=item.to_dict())


@bp.get("/api/admin/articles")
@require_admin
def admin_articles():
    return jsonify(articles=[item.to_dict() for item in ordered_query(Article.query).all()])


@bp.get("/api/admin/categories")
@require_admin
def admin_categories():
    rows = (
        db.session.query(ArticleCategory, func.count(Article.id))
        .outerjoin(Article, Article.category == ArticleCategory.key)
        .group_by(ArticleCategory.id)
        .order_by(ArticleCategory.id.asc())
        .all()
    )
    return jsonify(categories=[category.to_dict(count) for category, count in rows])


@bp.post("/api/admin/categories")
@require_admin
def create_category():
    payload = request.get_json(silent=True) or {}
    key = str(payload.get("key", "")).strip()
    label = payload.get("label") or {}
    if not CATEGORY_KEY_PATTERN.fullmatch(key):
        return jsonify(message="شناسه دسته‌بندی باید با حرف انگلیسی شروع شود و فقط شامل حروف انگلیسی، عدد و خط تیره باشد."), 422
    if not str(label.get("fa", "")).strip() or not str(label.get("en", "")).strip():
        return jsonify(message="عنوان فارسی و انگلیسی دسته‌بندی الزامی است."), 422
    category = ArticleCategory(key=key, label={"fa": label["fa"].strip(), "en": label["en"].strip()})
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="این شناسه دسته‌بندی قبلاً استفاده شده است."), 409
    return jsonify(category=category.to_dict()), 201


@bp.delete("/api/admin/categories/<int:category_id>")
@require_admin
def delete_category(category_id):
    category = db.get_or_404(ArticleCategory, category_id)
    if Article.query.filter_by(category=category.key).first():
        return jsonify(message="دسته‌بندی دارای مقاله را نمی‌توان حذف کرد؛ ابتدا مقاله‌ها را منتقل کنید."), 409
    db.session.delete(category)
    db.session.commit()
    return jsonify(message="دسته‌بندی حذف شد.")


@bp.post("/api/admin/articles")
@require_admin
def create_article():
    payload = request.get_json(silent=True) or {}
    validation_error = validate(payload)
    if validation_error:
        return jsonify(message=validation_error), 422
    item = Article()
    item.apply(payload)
    db.session.add(item)
    db.session.flush()
    keep_single_featured(item)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="این آدرس مقاله قبلاً استفاده شده است."), 409
    return jsonify(article=item.to_dict()), 201


@bp.put("/api/admin/articles/<int:article_id>")
@require_admin
def update_article(article_id):
    item = db.get_or_404(Article, article_id)
    payload = request.get_json(silent=True) or {}
    if not str(payload.get("image", "")).strip():
        payload["image"] = item.image
    if "imageSrcset" not in payload:
        payload["imageSrcset"] = item.image_srcset or ""
    validation_error = validate(payload)
    if validation_error:
        return jsonify(message=validation_error), 422
    item.apply(payload)
    keep_single_featured(item)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="این آدرس مقاله قبلاً استفاده شده است."), 409
    return jsonify(article=item.to_dict())


@bp.delete("/api/admin/articles/<int:article_id>")
@require_admin
def delete_article(article_id):
    item = db.get_or_404(Article, article_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(message="مقاله حذف شد.")


@bp.post("/api/admin/uploads")
@require_admin
def upload_image():
    image = request.files.get("image")
    if not image or not image.filename:
        return jsonify(message="یک فایل تصویر انتخاب کنید."), 422
    original = secure_filename(image.filename)
    extension = original.rsplit(".", 1)[-1].lower() if "." in original else ""
    if extension not in ALLOWED_EXTENSIONS:
        return jsonify(message="فرمت تصویر باید PNG، JPG یا WebP باشد."), 422
    image.stream.seek(0, 2)
    image_size = image.stream.tell()
    image.stream.seek(0)
    if image_size > MAX_IMAGE_BYTES:
        return jsonify(message="حجم تصویر نباید بیشتر از ۴۰۰ کیلوبایت باشد."), 413
    filename = f"{uuid4().hex}.{extension}"
    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)
    image.save(upload_dir / filename)
    return jsonify(url=url_for("articles.uploaded_file", filename=filename, _external=True)), 201


@bp.get("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
