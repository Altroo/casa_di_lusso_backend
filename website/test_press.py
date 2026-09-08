from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse
from django.utils import timezone

from .forms import PressArticleAdminForm
from .models import PressArticle, PressCategory


pytestmark = pytest.mark.django_db


def article(**overrides):
    values = {"title": "Vita Gessi Caffè", "excerpt": "Le design au quotidien.",
              "body_html": "<p>Un nouvel espace de vie.</p>", "is_published": True}
    values.update(overrides)
    obj = PressArticle.objects.create(**values)
    obj.categories.add(PressCategory.objects.first())
    return obj


def test_press_categories_follow_figma_and_can_be_hidden(client):
    categories = PressCategory.objects.all()
    assert list(categories.values_list("title", flat=True)) == [
        "Tendances déco", "Nouveautés des marques partenaires", "Conseils d’aménagement",
    ]
    categories.filter(slug="tendances-deco").update(is_active=False)
    response = client.get(reverse("website:press-categories"))
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_press_slug_is_unique_and_stable():
    first, second = article(), article()
    assert first.slug == "vita-gessi-caffe"
    assert second.slug == "vita-gessi-caffe-1"
    first.title = "Un nouveau titre"
    first.save()
    assert first.slug == "vita-gessi-caffe"


def test_only_published_current_categorized_articles_are_public(client):
    public = article()
    draft = article(is_published=False)
    future = article(published_at=timezone.now() + timedelta(days=1))
    orphan = article()
    orphan.categories.clear()
    response = client.get(reverse("website:press-articles"))
    assert [entry["id"] for entry in response.json()] == [public.pk]
    assert "body_html" not in response.json()[0]
    for obj in (draft, future, orphan):
        assert client.get(reverse("website:press-detail", args=[obj.slug])).status_code == 404
    assert client.get(reverse("website:press-detail", args=["unknown"])).status_code == 404
    assert client.post(reverse("website:press-articles"), {"title": "No public writes"}).status_code == 405


def test_press_order_and_multiple_categories_do_not_duplicate_articles(client):
    later = article(sort_order=4)
    earlier = article(sort_order=1)
    earlier.categories.set(PressCategory.objects.all())
    response = client.get(reverse("website:press-articles"))
    assert [entry["id"] for entry in response.json()] == [earlier.pk, later.pk]
    assert len(response.json()[0]["categories"]) == 3


def test_unpublish_is_immediately_reflected_in_list_and_detail(client):
    obj = article()
    url = reverse("website:press-detail", args=[obj.slug])
    assert client.get(url).status_code == 200
    obj.is_published = False
    obj.save()
    assert client.get(url).status_code == 404
    assert client.get(reverse("website:press-articles")).json() == []


def test_article_html_is_sanitized_on_save_and_read(client):
    unsafe = '<p style="text-align:center;position:fixed" onclick="bad()">Texte</p><script>bad()</script><a href="javascript:bad()">Lien</a><iframe src="https://bad.test"></iframe>'
    obj = article(body_html=unsafe, image_file="press/articles/cover.jpg")
    assert "script" not in obj.body_html
    # Guard direct imports/bulk updates too, not just Model.save().
    PressArticle.objects.filter(pk=obj.pk).update(body_html=unsafe)
    payload = client.get(reverse("website:press-detail", args=[obj.slug])).json()
    assert payload["image_url"].startswith("http://testserver/api/website/press/articles/vita-gessi-caffe/images/cover/?v=")
    for forbidden in ("onclick", "javascript:", "script", "iframe", "position:"):
        assert forbidden not in payload["body_html"]
    assert "text-align:center" in payload["body_html"]


def test_admin_form_supports_drafts_and_requires_content_to_publish():
    data = {"title": "Brouillon", "excerpt": "Résumé", "published_at": "2026-09-08 12:00:00",
            "sort_order": 0, "categories": [PressCategory.objects.first().pk]}
    form = PressArticleAdminForm(data=data)
    assert form.is_valid(), form.errors
    obj = form.save()
    assert not obj.is_published
    assert obj.slug == "brouillon"
    form = PressArticleAdminForm(data={**data, "is_published": True})
    assert not form.is_valid()
    assert "body_html" in form.errors


def test_admin_can_create_edit_and_publish_article(client):
    user = get_user_model().objects.create_superuser(email="press-admin@example.com", password="test-only")
    client.force_login(user)
    data = {"title": "Article administré", "excerpt": "Résumé", "body_html": "<p>Texte complet</p>",
            "categories": [PressCategory.objects.first().pk], "sort_order": "0",
            "published_at_0": "2026-01-01", "published_at_1": "12:00:00", "_save": "Enregistrer"}
    response = client.post(reverse("admin:website_pressarticle_add"), data)
    assert response.status_code == 302
    obj = PressArticle.objects.get(title=data["title"])
    assert not obj.is_published
    response = client.post(reverse("admin:website_pressarticle_change", args=[obj.pk]), {**data, "is_published": "on"})
    assert response.status_code == 302
    obj.refresh_from_db()
    assert obj.is_published
    assert client.get(reverse("website:press-detail", args=[obj.slug])).status_code == 200


def test_admin_is_not_available_anonymously(client):
    response = client.get(reverse("admin:website_pressarticle_add"))
    assert response.status_code == 302
    assert "login" in response.url


@pytest.mark.parametrize("body", ["<script>alert(1)</script>", "<p>&nbsp;</p>", "<p> </p>"])
def test_admin_rejects_content_that_is_empty_after_sanitizing(body):
    form = PressArticleAdminForm(data={
        "title": "Article", "excerpt": "Résumé", "body_html": body, "is_published": True,
        "published_at": "2026-09-08 12:00:00", "sort_order": 0,
        "categories": [PressCategory.objects.first().pk],
    })
    assert not form.is_valid()
    assert "body_html" in form.errors


def test_seed_examples_are_drafts_and_preserve_existing_edits(tmp_path, settings):
    from PIL import Image
    from website.management.commands.seed_press_drafts import EXAMPLES

    settings.MEDIA_ROOT = tmp_path / "media"
    for _, _, name, _, _ in EXAMPLES:
        Image.new("RGB", (2, 2)).save(tmp_path / name)
    call_command("seed_press_drafts", assets_dir=tmp_path)
    assert PressArticle.objects.count() == 3
    assert not PressArticle.objects.filter(is_published=True).exists()
    obj = PressArticle.objects.first()
    obj.title = "Titre édité"
    obj.save()
    call_command("seed_press_drafts", assets_dir=tmp_path)
    obj.refresh_from_db()
    assert obj.title == "Titre édité"
    assert PressArticle.objects.count() == 3


def test_published_images_work_with_debug_off_and_change_url_after_edits(client, tmp_path, settings):
    from django.core.files.base import ContentFile

    settings.MEDIA_ROOT = tmp_path
    settings.DEBUG = False
    obj = article()
    obj.image_file.save("cover.png", ContentFile(b"test-image-content"))
    detail_url = reverse("website:press-detail", args=[obj.slug])
    first_url = client.get(detail_url).json()["image_url"]
    response = client.get(first_url)
    assert response.status_code == 200
    assert response["Content-Type"] == "image/png"
    assert b"".join(response.streaming_content) == b"test-image-content"
    obj.save()
    assert client.get(detail_url).json()["image_url"] != first_url
    for kind in ("hero", "invalid"):
        assert client.get(reverse("website:press-image", args=[obj.slug, kind])).status_code == 404
    obj.is_published = False
    obj.save()
    assert client.get(first_url).status_code == 404


def test_draft_upload_links_require_admin_permission(client, tmp_path, settings):
    from django.core.files.base import ContentFile

    settings.MEDIA_ROOT = tmp_path
    settings.DEBUG = False
    obj = article(is_published=False)
    obj.image_file.save("draft.png", ContentFile(b"draft-image"))
    url = obj.image_file.url
    assert client.get(url).status_code == 404
    admin = get_user_model().objects.create_superuser(email="preview@example.test", password="test-only")
    client.force_login(admin)
    response = client.get(url)
    assert response.status_code == 200
    assert response["Cache-Control"] == "private, no-store"
    assert b"".join(response.streaming_content) == b"draft-image"
    assert client.get("/media/press/articles/missing.png").status_code == 404
    client.logout()
    obj.is_published = True
    obj.save()
    assert client.get(url).status_code == 200
