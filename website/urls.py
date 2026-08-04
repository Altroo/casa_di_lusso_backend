from django.urls import path

from .views import ContactRequestView, NewsletterSubscribeView, SiteContentView

app_name = "website"

urlpatterns = [
    path("content/", SiteContentView.as_view(), name="content"),
    path("contact/", ContactRequestView.as_view(), name="contact"),
    path("newsletter/", NewsletterSubscribeView.as_view(), name="newsletter"),
]
