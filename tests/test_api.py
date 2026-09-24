from io import BytesIO

import pytest

from app import create_app
from app.extensions import db
from app.models import AdminUser, Article, ArticleCategory
from app.seed import ARTICLES


@pytest.fixture()
def app(tmp_path):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "AUTO_CREATE_SCHEMA": False,
        "UPLOAD_FOLDER": str(tmp_path / "uploads"),
    })
    with app.app_context():
        db.create_all()
        ArticleCategory.ensure_defaults()
        admin = AdminUser(username="editor")
        admin.set_password("good-password")
        article = Article()
        article.apply(ARTICLES[0])
        db.session.add_all([admin, article])
        db.session.commit()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client):
    response = client.post("/api/auth/login", json={"username": "editor", "password": "good-password"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.get_json()['token']}"}


def test_public_api_only_returns_published_articles(client):
    response = client.get("/api/articles")
    assert response.status_code == 200
    assert [item["slug"] for item in response.get_json()["articles"]] == [ARTICLES[0]["slug"]]


def test_admin_can_create_update_and_delete_article(client):
    headers = login(client)
    payload = {**ARTICLES[1], "slug": "a-new-story", "published": False}

    created = client.post("/api/admin/articles", headers=headers, json=payload)
    assert created.status_code == 201
    article = created.get_json()["article"]
    assert article["published"] is False

    payload["published"] = True
    payload["title"] = {"en": "Updated story", "fa": "مقاله ویرایش‌شده"}
    updated = client.put(f"/api/admin/articles/{article['id']}", headers=headers, json=payload)
    assert updated.status_code == 200
    assert updated.get_json()["article"]["title"]["fa"] == "مقاله ویرایش‌شده"

    deleted = client.delete(f"/api/admin/articles/{article['id']}", headers=headers)
    assert deleted.status_code == 200
    assert client.get("/api/articles/a-new-story").status_code == 404


def test_admin_routes_require_a_valid_token(client):
    response = client.get("/api/admin/articles")
    assert response.status_code == 401


def test_admin_can_manage_empty_categories_and_public_only_sees_used_categories(client):
    headers = login(client)
    created = client.post("/api/admin/categories", headers=headers, json={
        "key": "newCategory",
        "label": {"en": "New category", "fa": "دسته تازه"},
    })
    assert created.status_code == 201
    category = created.get_json()["category"]
    assert all(item["key"] != "newCategory" for item in client.get("/api/categories").get_json()["categories"])

    article_payload = {
        **ARTICLES[1],
        "slug": "story-in-a-new-category",
        "category": "newCategory",
        "published": True,
    }
    article_response = client.post("/api/admin/articles", headers=headers, json=article_payload)
    assert article_response.status_code == 201
    article = article_response.get_json()["article"]
    assert any(item["key"] == "newCategory" for item in client.get("/api/categories").get_json()["categories"])

    in_use = client.delete(f"/api/admin/categories/{category['id']}", headers=headers)
    assert in_use.status_code == 409

    assert client.delete(f"/api/admin/articles/{article['id']}", headers=headers).status_code == 200
    deleted = client.delete(f"/api/admin/categories/{category['id']}", headers=headers)
    assert deleted.status_code == 200


def test_article_update_keeps_existing_image_when_payload_image_is_blank(client):
    headers = login(client)
    article = client.get("/api/admin/articles", headers=headers).get_json()["articles"][0]
    original_image = article["image"]
    article["image"] = ""

    updated = client.put(f"/api/admin/articles/{article['id']}", headers=headers, json=article)
    assert updated.status_code == 200
    assert updated.get_json()["article"]["image"] == original_image


def test_upload_rejects_images_larger_than_400_kilobytes(client):
    headers = login(client)
    response = client.post(
        "/api/admin/uploads",
        headers=headers,
        data={"image": (BytesIO(b"x" * (400 * 1024 + 1)), "too-large.jpg")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 413
    assert "۴۰۰" in response.get_json()["message"]
