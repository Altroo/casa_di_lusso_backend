import pytest
from django.db import IntegrityError, transaction
from django.urls import reverse
from rest_framework.test import APIClient

from .models import ContactRequest, NewsletterSubscriber, SiteSettings


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_public_content_endpoint_is_available_without_authentication(api_client):
    SiteSettings.objects.update_or_create(
        pk=1,
        defaults={
            "hero_text": "Texte héros",
            "about_text": "Texte à propos",
            "project_title": "Votre projet",
            "partners_intro": "Partenaires",
            "partners_outro": "Excellence",
            "address": "Tanger",
            "phone": "+212 500000000",
            "email": "contact@casadilusso.ma",
        },
    )

    response = api_client.get(reverse("website:content"))

    assert response.status_code == 200
    assert response.data["settings"]["brand_name"] == "Casa di Lusso"
    assert "services" in response.data
    assert "portfolio" in response.data


@pytest.mark.django_db
def test_site_settings_is_enforced_as_a_database_singleton():
    assert SiteSettings.objects.count() == 1

    with pytest.raises(IntegrityError), transaction.atomic():
        SiteSettings.objects.create(
            hero_text="Second héros",
            about_text="Second à propos",
            project_title="Second projet",
            partners_intro="Seconds partenaires",
            partners_outro="Seconde conclusion",
            address="Tanger",
            phone="+212 500000000",
            email="second@casadilusso.ma",
        )


@pytest.mark.django_db
def test_contact_endpoint_persists_request(api_client):
    payload = {
        "full_name": "Client Casa",
        "email": "client@example.com",
        "phone": "+212 600000000",
        "message": "Je souhaite discuter de mon projet.",
        "website": "",
    }

    response = api_client.post(reverse("website:contact"), payload, format="json")

    assert response.status_code == 201
    assert ContactRequest.objects.filter(email="client@example.com").exists()


@pytest.mark.django_db
def test_contact_honeypot_rejects_bots(api_client):
    response = api_client.post(
        reverse("website:contact"),
        {
            "full_name": "Robot",
            "email": "robot@example.com",
            "phone": "00000000",
            "message": "Spam",
            "website": "https://spam.example.com",
        },
        format="json",
    )

    assert response.status_code == 400
    assert ContactRequest.objects.count() == 0


@pytest.mark.django_db
def test_newsletter_resubscribe_is_idempotent(api_client):
    url = reverse("website:newsletter")

    first = api_client.post(url, {"email": "NEWS@example.com"}, format="json")
    second = api_client.post(url, {"email": "news@example.com"}, format="json")

    assert first.status_code == 201
    assert second.status_code == 201
    assert NewsletterSubscriber.objects.filter(email="news@example.com", is_active=True).count() == 1
