from django.contrib import admin

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
)


admin.site.site_header = "Administration Casa di Lusso"
admin.site.site_title = "Casa di Lusso"
admin.site.index_title = "Site d’administration"


class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identité", {"fields": ("brand_name",)}),
        (
            "Héros",
            {"fields": ("hero_eyebrow", "hero_title", "hero_text", "hero_tagline", "hero_image")},
        ),
        ("À propos", {"fields": ("about_title", "about_text", "about_image")}),
        ("Services", {"fields": ("services_heading", "services_intro", "services_tagline")}),
        ("Valeurs et projet", {"fields": ("values_background", "project_title", "project_image")}),
        ("Partenaires", {"fields": ("partners_intro", "partners_outro", "catalog")}),
        ("Vidéo", {"fields": ("video_title", "video_url", "video_cover")}),
        ("Contact", {"fields": ("address", "phone", "email", "map_embed_url", "map_link")}),
        ("Réseaux sociaux", {"fields": ("instagram_url", "facebook_url", "linkedin_url", "whatsapp_url")}),
    )

    @staticmethod
    def has_add_permission(request):
        return not SiteSettings.objects.exists()

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False


class OrderedAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "created_at", "is_processed")
    list_filter = ("is_processed", "created_at")
    search_fields = ("full_name", "email", "phone", "message")
    readonly_fields = ("full_name", "email", "phone", "message", "created_at")


class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("email",)


admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(ValueItem, OrderedAdmin)
admin.site.register(Metric, OrderedAdmin)
admin.site.register(Service, OrderedAdmin)
admin.site.register(PortfolioItem, OrderedAdmin)
admin.site.register(Partner, OrderedAdmin)
admin.site.register(Testimonial, OrderedAdmin)
admin.site.register(ContactRequest, ContactRequestAdmin)
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
