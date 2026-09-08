from rest_framework import serializers
from django.urls import reverse

from .models import (
    ContactRequest,
    Metric,
    NewsletterSubscriber,
    Partner,
    PortfolioItem,
    Service,
    SiteSettings,
    Testimonial,
    ValueItem,
    PressArticle,
    PressCategory,
)


def absolute_file_url(request, field):
    if not field:
        return ""
    url = field.url
    return request.build_absolute_uri(url) if request else url


class SiteSettingsSerializer(serializers.ModelSerializer):
    hero_image_url = serializers.SerializerMethodField()
    about_image_url = serializers.SerializerMethodField()
    project_image_url = serializers.SerializerMethodField()
    values_background_url = serializers.SerializerMethodField()
    video_cover_url = serializers.SerializerMethodField()
    catalog_url = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        exclude = (
            "singleton_key",
            "hero_image",
            "about_image",
            "project_image",
            "values_background",
            "video_cover",
            "catalog",
        )

    def _url(self, obj, field_name):
        return absolute_file_url(self.context.get("request"), getattr(obj, field_name))

    def get_hero_image_url(self, obj):
        return self._url(obj, "hero_image")

    def get_about_image_url(self, obj):
        return self._url(obj, "about_image")

    def get_project_image_url(self, obj):
        return self._url(obj, "project_image")

    def get_values_background_url(self, obj):
        return self._url(obj, "values_background")

    def get_video_cover_url(self, obj):
        return self._url(obj, "video_cover")

    def get_catalog_url(self, obj):
        return self._url(obj, "catalog")


class OrderedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title", "order")


class ValueItemSerializer(OrderedSerializer):
    class Meta(OrderedSerializer.Meta):
        model = ValueItem
        fields = OrderedSerializer.Meta.fields + ("icon",)


class MetricSerializer(OrderedSerializer):
    class Meta(OrderedSerializer.Meta):
        model = Metric
        fields = OrderedSerializer.Meta.fields + ("value",)


class ServiceSerializer(OrderedSerializer):
    class Meta(OrderedSerializer.Meta):
        model = Service
        fields = OrderedSerializer.Meta.fields + ("description",)


class PortfolioItemSerializer(OrderedSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta(OrderedSerializer.Meta):
        model = PortfolioItem
        fields = OrderedSerializer.Meta.fields + ("image_url", "fallback_path", "alt_text")

    def get_image_url(self, obj):
        return absolute_file_url(self.context.get("request"), obj.image)


class PartnerSerializer(OrderedSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta(OrderedSerializer.Meta):
        model = Partner
        fields = OrderedSerializer.Meta.fields + ("logo_url", "fallback_path", "website_url")

    def get_logo_url(self, obj):
        return absolute_file_url(self.context.get("request"), obj.logo)


class TestimonialSerializer(OrderedSerializer):
    class Meta(OrderedSerializer.Meta):
        model = Testimonial
        fields = OrderedSerializer.Meta.fields + ("quote", "customer_name")


class ContactRequestSerializer(serializers.ModelSerializer):
    website = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = ContactRequest
        fields = ("full_name", "email", "phone", "message", "website")

    @staticmethod
    def validate_website(value):
        if value:
            raise serializers.ValidationError("Envoi invalide.")
        return value

    def create(self, validated_data):
        validated_data.pop("website", None)
        return super().create(validated_data)


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ("email",)
        extra_kwargs = {"email": {"validators": []}}

    def create(self, validated_data):
        subscriber, _ = self.Meta.model.objects.update_or_create(
            email=validated_data["email"].lower(), defaults={"is_active": True}
        )
        return subscriber


class PressCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PressCategory
        fields = ("id", "title", "slug")


class PressArticleSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = PressArticle
        fields = ("id", "title", "slug", "categories", "excerpt", "image_url", "image_alt",
                  "published_at", "updated_at", "is_featured")
        read_only_fields = fields

    def get_image_url(self, obj):
        return self.article_image_url(obj, "cover", obj.image_file)

    def article_image_url(self, obj, kind, field):
        if not field:
            return ""
        # Versioned URLs invalidate optimized images immediately after an admin edit.
        url = reverse("website:press-image", args=[obj.slug, kind])
        url += f"?v={int(obj.updated_at.timestamp() * 1000000)}"
        request = self.context.get("request")
        return request.build_absolute_uri(url) if request else url

    def get_categories(self, obj):
        return PressCategorySerializer([category for category in obj.categories.all() if category.is_active], many=True).data


class PressArticleDetailSerializer(PressArticleSerializer):
    body_html = serializers.SerializerMethodField()
    hero_image_url = serializers.SerializerMethodField()

    class Meta(PressArticleSerializer.Meta):
        fields = PressArticleSerializer.Meta.fields + ("content_title", "introduction", "body_html", "hero_image_url")
        read_only_fields = fields

    def get_body_html(self, obj):
        from .rich_text import sanitize_article_html
        return sanitize_article_html(obj.body_html)

    def get_hero_image_url(self, obj):
        return self.article_image_url(obj, "hero", obj.hero_image)
