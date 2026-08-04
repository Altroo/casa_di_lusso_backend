from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import Metric, Partner, PortfolioItem, Service, SiteSettings, Testimonial, ValueItem
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
)


class PublicAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]


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
