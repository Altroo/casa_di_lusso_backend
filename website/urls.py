from django.urls import path

from .views import ContactRequestView, NewsletterSubscribeView, SiteContentView
from .views import PressCategoryListView, PressArticleListView, PressArticleDetailView, PressArticleImageView

app_name = "website"

urlpatterns = [
    path("press/categories/", PressCategoryListView.as_view(), name="press-categories"),
    path("press/articles/", PressArticleListView.as_view(), name="press-articles"),
    path("press/articles/<slug:slug>/", PressArticleDetailView.as_view(), name="press-detail"),
    path("press/articles/<slug:slug>/images/<str:kind>/", PressArticleImageView.as_view(), name="press-image"),
    path("content/", SiteContentView.as_view(), name="content"),
    path("contact/", ContactRequestView.as_view(), name="contact"),
    path("newsletter/", NewsletterSubscribeView.as_view(), name="newsletter"),
]
