from datetime import date, datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


DEFAULT_ARTICLE_CATEGORIES = [
    {"key": "clinicalAI", "label": {"en": "Clinical AI", "fa": "هوش مصنوعی بالینی"}},
    {"key": "medicalSoftware", "label": {"en": "Medical Software", "fa": "نرم‌افزار پزشکی"}},
    {"key": "responsibleAI", "label": {"en": "Responsible AI", "fa": "هوش مصنوعی مسئولانه"}},
    {"key": "digitalCare", "label": {"en": "Digital Care", "fa": "مراقبت دیجیتال"}},
    {"key": "dataPrivacy", "label": {"en": "Data & Privacy", "fa": "داده و حریم خصوصی"}},
]


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class AdminUser(db.Model):
    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ArticleCategory(db.Model):
    __tablename__ = "article_categories"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False, index=True)
    label = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    def to_dict(self, article_count=0):
        return {
            "id": self.id,
            "key": self.key,
            "label": self.label,
            "articleCount": int(article_count or 0),
        }

    @classmethod
    def ensure_defaults(cls):
        if cls.query.first():
            return
        db.session.add_all([cls(key=item["key"], label=item["label"]) for item in DEFAULT_ARTICLE_CATEGORIES])
        db.session.commit()


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    featured = db.Column(db.Boolean, nullable=False, default=False)
    published = db.Column(db.Boolean, nullable=False, default=False, index=True)
    medical = db.Column(db.Boolean, nullable=False, default=True)
    title = db.Column(db.JSON, nullable=False)
    summary = db.Column(db.JSON, nullable=False)
    author = db.Column(db.JSON, nullable=False)
    reviewer = db.Column(db.JSON, nullable=True)
    date_published = db.Column(db.Date, nullable=False, default=date.today)
    date_modified = db.Column(db.Date, nullable=False, default=date.today)
    reading_minutes = db.Column(db.Integer, nullable=False, default=5)
    image = db.Column(db.String(600), nullable=False)
    image_srcset = db.Column(db.Text, nullable=True)
    image_width = db.Column(db.Integer, nullable=True)
    image_height = db.Column(db.Integer, nullable=True)
    alt = db.Column(db.JSON, nullable=False)
    sections = db.Column(db.JSON, nullable=False, default=list)
    sources = db.Column(db.JSON, nullable=False, default=list)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    @staticmethod
    def _date(value, fallback=None):
        if isinstance(value, date):
            return value
        if value:
            return date.fromisoformat(value)
        return fallback or date.today()

    def apply(self, payload):
        self.slug = str(payload.get("slug", "")).strip().lower()
        self.category = payload.get("category", "medicalSoftware")
        self.featured = bool(payload.get("featured", False))
        self.published = bool(payload.get("published", False))
        self.medical = bool(payload.get("medical", True))
        self.title = payload.get("title") or {"en": "", "fa": ""}
        self.summary = payload.get("summary") or {"en": "", "fa": ""}
        self.author = payload.get("author") or {"en": "Editorial desk", "fa": "تحریریه"}
        self.reviewer = payload.get("reviewer") or {"en": "", "fa": ""}
        self.date_published = self._date(payload.get("datePublished"), self.date_published)
        self.date_modified = self._date(payload.get("dateModified"), date.today())
        self.reading_minutes = int(payload.get("readingMinutes", 5))
        self.image = str(payload.get("image", "")).strip()
        self.image_srcset = str(payload.get("imageSrcset", "")).strip() or None
        self.image_width = payload.get("imageWidth") or None
        self.image_height = payload.get("imageHeight") or None
        self.alt = payload.get("alt") or {"en": "", "fa": ""}
        self.sections = payload.get("sections") or []
        self.sources = payload.get("sources") or []

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "category": self.category,
            "featured": self.featured,
            "published": self.published,
            "medical": self.medical,
            "title": self.title,
            "summary": self.summary,
            "author": self.author,
            "reviewer": self.reviewer,
            "datePublished": self.date_published.isoformat(),
            "dateModified": self.date_modified.isoformat(),
            "readingMinutes": self.reading_minutes,
            "image": self.image,
            "imageSrcset": self.image_srcset,
            "imageWidth": self.image_width,
            "imageHeight": self.image_height,
            "alt": self.alt,
            "sections": self.sections or [],
            "sources": self.sources or [],
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }
