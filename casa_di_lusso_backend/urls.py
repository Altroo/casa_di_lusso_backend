from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from website.views import PressUploadedImageView


def health_check(_request):
    return JsonResponse({"status": "healthy"})


urlpatterns = [
    path("api/health/", health_check, name="health-check"),
    path("api/website/", include("website.urls")),
    path("media/press/<str:folder>/<str:filename>", PressUploadedImageView.as_view(), name="press-uploaded-image"),
    path(f"{settings.ADMIN_URL_PATH}/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
