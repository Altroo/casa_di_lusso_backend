from rest_framework import generics, status
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import Metric, Partner, PortfolioItem, Service, SiteSettings, Testimonial, ValueItem
from .models import PressArticle, PressCategory
from .serializers import (
    ContactRequestSerializer,
    MetricSerializer,
    NewsletterSubscriberSerializer,
    PartnerSerializer,
    PortfolioItemSerializer,
    ServiceSerializer,
    SiteSettingsSerializer,
    TestimonialSerializer,
    ValueItemSerializer,
    PressArticleSerializer,
    PressArticleDetailSerializer,
    PressCategorySerializer,
)


class PublicAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]


class PressCategoryListView(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    pagination_class = None
    serializer_class = PressCategorySerializer
    queryset = PressCategory.objects.filter(is_active=True)


class PressArticleListView(generics.ListAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    pagination_class = None
    serializer_class = PressArticleSerializer

    def get_queryset(self):
        return PressArticle.objects.filter(
            is_published=True, published_at__lte=timezone.now(), categories__is_active=True,
        ).distinct().prefetch_related("categories")


class PressArticleDetailView(generics.RetrieveAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = PressArticleDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return PressArticle.objects.filter(
            is_published=True, published_at__lte=timezone.now(), categories__is_active=True,
        ).distinct().prefetch_related("categories")


class PressArticleImageView(PublicAPIView):
    """Serve only a published article's image, including on the IP-based demo."""

    @staticmethod
    def get(request, slug, kind):
        field_name = {"cover": "image_file", "hero": "hero_image"}.get(kind)
        if field_name is None:
            raise Http404
        article = get_object_or_404(
            PressArticle.objects.filter(
                is_published=True, published_at__lte=timezone.now(), categories__is_active=True,
            ).distinct(), slug=slug,
        )
        field = getattr(article, field_name)
        if not field:
            raise Http404
        try:
            response = FileResponse(field.open("rb"))
        except FileNotFoundError:
            raise Http404 from None
        response["X-Content-Type-Options"] = "nosniff"
        response["Cache-Control"] = "no-cache"
        return response


class SiteContentView(PublicAPIView):
    @staticmethod
    def get(request):
        settings = SiteSettings.objects.first()
        if settings is None:
            return Response({"detail": "Le contenu du site n'est pas encore configuré."}, status=503)

        context = {"request": request}
        return Response(
            {
                "settings": SiteSettingsSerializer(settings, context=context).data,
                "values": ValueItemSerializer(ValueItem.objects.filter(is_active=True), many=True).data,
                "metrics": MetricSerializer(Metric.objects.filter(is_active=True), many=True).data,
                "services": ServiceSerializer(Service.objects.filter(is_active=True), many=True).data,
                "portfolio": PortfolioItemSerializer(
                    PortfolioItem.objects.filter(is_active=True), many=True, context=context
                ).data,
                "partners": PartnerSerializer(
                    Partner.objects.filter(is_active=True), many=True, context=context
                ).data,
                "testimonials": TestimonialSerializer(
                    Testimonial.objects.filter(is_active=True), many=True
                ).data,
            }
        )


class ContactRequestView(PublicAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"

    @staticmethod
    def post(request):
        serializer = ContactRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Votre demande a bien été envoyée."},
            status=status.HTTP_201_CREATED,
        )


class NewsletterSubscribeView(PublicAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "newsletter"

    @staticmethod
    def post(request):
        serializer = NewsletterSubscriberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Votre inscription est confirmée."},
            status=status.HTTP_201_CREATED,
        )
