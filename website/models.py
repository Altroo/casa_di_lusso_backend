from django.core.validators import MinValueValidator
from django.db import models


class OrderedContent(models.Model):
    title = models.CharField("Titre", max_length=180)
    order = models.PositiveSmallIntegerField(
        "Ordre", default=0, validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField("Visible", default=True)

    class Meta:
        abstract = True
        ordering = ("order", "id")

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    singleton_key = models.CharField(
        max_length=16,
        default="site",
        unique=True,
        editable=False,
    )
    brand_name = models.CharField("Nom de la marque", max_length=120, default="Casa di Lusso")
    hero_eyebrow = models.CharField("Sur-titre du héros", max_length=120, default="CASA DI LUSSO")
    hero_title = models.CharField("Titre du héros", max_length=180, default="L’exception au quotidien")
    hero_text = models.TextField("Texte du héros")
    hero_tagline = models.CharField(
        "Signature du héros",
        max_length=220,
        default="ARCHITECTURE INTÉRIEURE  •  DESIGN  •  MOBILIER  •  SUR MESURE",
    )
    hero_image = models.ImageField("Image du héros", upload_to="website/hero/", blank=True)
    about_title = models.CharField("Titre À propos", max_length=120, default="À propos")
    about_text = models.TextField("Texte À propos")
    about_image = models.ImageField("Image À propos", upload_to="website/about/", blank=True)
    services_heading = models.CharField(
        "Accroche services",
        max_length=180,
        default="Des espaces pensés dans les moindres détails",
    )
    services_intro = models.TextField(
        "Introduction services",
        default=(
            "Des solutions sur mesure, de la conception à la réalisation, pour créer "
            "des espaces élégants, fonctionnels et durables."
        ),
    )
    services_tagline = models.CharField(
        "Signature services",
        max_length=220,
        default="CONCEPTION  •  SÉLECTION  •  COORDINATION  •  RÉALISATION",
    )
    project_title = models.CharField("Titre du projet", max_length=220)
    project_image = models.ImageField("Image du projet", upload_to="website/project/", blank=True)
    values_background = models.ImageField("Fond des valeurs", upload_to="website/values/", blank=True)
    partners_intro = models.TextField("Introduction partenaires")
    partners_outro = models.TextField("Conclusion partenaires")
    catalog = models.FileField("Catalogue", upload_to="website/catalogs/", blank=True)
    video_title = models.CharField("Titre vidéo", max_length=180, blank=True)
    video_url = models.URLField("Lien vidéo", blank=True)
    video_cover = models.ImageField("Couverture vidéo", upload_to="website/video/", blank=True)
    address = models.TextField("Adresse")
    phone = models.CharField("Téléphone", max_length=40)
    email = models.EmailField("E-mail")
    map_embed_url = models.URLField("Lien Google Maps intégré", blank=True)
    map_link = models.URLField("Lien Google Maps", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    facebook_url = models.URLField("Facebook", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)
    whatsapp_url = models.URLField("WhatsApp", blank=True)
    updated_at = models.DateTimeField("Dernière modification", auto_now=True)

    class Meta:
        verbose_name = "Paramètres du site"
        verbose_name_plural = "Paramètres du site"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(singleton_key="site"),
                name="website_site_settings_singleton",
            )
        ]

    def __str__(self):
        return self.brand_name


class ValueItem(OrderedContent):
    icon = models.CharField(
        "Icône",
        max_length=32,
        choices=(
            ("design", "Design"),
            ("bespoke", "Sur mesure"),
            ("quality", "Qualité"),
            ("support", "Accompagnement"),
        ),
        default="design",
    )

    class Meta(OrderedContent.Meta):
        verbose_name = "Valeur"
        verbose_name_plural = "Valeurs"


class Metric(OrderedContent):
    value = models.CharField("Valeur", max_length=30)

    class Meta(OrderedContent.Meta):
        verbose_name = "Chiffre clé"
        verbose_name_plural = "Chiffres clés"


class Service(OrderedContent):
    description = models.TextField("Description")

    class Meta(OrderedContent.Meta):
        verbose_name = "Service"
        verbose_name_plural = "Services"


class PortfolioItem(OrderedContent):
    image = models.ImageField("Image", upload_to="website/portfolio/", blank=True)
    fallback_path = models.CharField("Image livrée avec le site", max_length=255, blank=True)
    alt_text = models.CharField("Texte alternatif", max_length=180, blank=True)

    class Meta(OrderedContent.Meta):
        verbose_name = "Projet du portfolio"
        verbose_name_plural = "Portfolio"


class Partner(OrderedContent):
    logo = models.ImageField("Logo", upload_to="website/partners/", blank=True)
    fallback_path = models.CharField("Logo livré avec le site", max_length=255, blank=True)
    website_url = models.URLField("Site web", blank=True)

    class Meta(OrderedContent.Meta):
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"


class Testimonial(OrderedContent):
    quote = models.TextField("Témoignage")
    customer_name = models.CharField("Nom du client", max_length=120, blank=True)

    class Meta(OrderedContent.Meta):
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"


class ContactRequest(models.Model):
    full_name = models.CharField("Nom complet", max_length=180)
    email = models.EmailField("E-mail")
    phone = models.CharField("Téléphone", max_length=40)
    message = models.TextField("Message")
    is_processed = models.BooleanField("Traité", default=False)
    created_at = models.DateTimeField("Reçu le", auto_now_add=True)

    class Meta:
        verbose_name = "Demande de contact"
        verbose_name_plural = "Demandes de contact"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.full_name} — {self.created_at:%d/%m/%Y}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField("E-mail", unique=True)
    is_active = models.BooleanField("Actif", default=True)
    created_at = models.DateTimeField("Inscrit le", auto_now_add=True)

    class Meta:
        verbose_name = "Abonné newsletter"
        verbose_name_plural = "Abonnés newsletter"
        ordering = ("-created_at",)

    def __str__(self):
        return self.email
