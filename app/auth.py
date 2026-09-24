from functools import wraps

from flask import Blueprint, current_app, g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from .extensions import db
from .models import AdminUser

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="admin-session")


def issue_token(user):
    return serializer().dumps({"user_id": user.id})


def require_admin(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        token = header.removeprefix("Bearer ").strip() if header.startswith("Bearer ") else ""
        if not token:
            return jsonify(message="برای ادامه وارد حساب مدیر شوید."), 401
        try:
            data = serializer().loads(token, max_age=current_app.config["TOKEN_MAX_AGE"])
        except SignatureExpired:
            return jsonify(message="نشست شما منقضی شده است. دوباره وارد شوید."), 401
        except BadSignature:
            return jsonify(message="نشست معتبر نیست."), 401
        g.admin = db.session.get(AdminUser, data.get("user_id"))
        if not g.admin:
            return jsonify(message="حساب مدیر پیدا نشد."), 401
        return view(*args, **kwargs)
    return wrapped


@bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", ""))
    user = AdminUser.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify(message="نام کاربری یا رمز عبور درست نیست."), 401
    return jsonify(token=issue_token(user), user={"id": user.id, "username": user.username})


@bp.get("/me")
@require_admin
def me():
    return jsonify(user={"id": g.admin.id, "username": g.admin.username})
