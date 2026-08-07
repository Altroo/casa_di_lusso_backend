from django.db import migrations, models


HERO_TEXT = (
    "Entrez dans un univers où chaque détail sublime votre espace. Casa di Lusso "
    "imagine des intérieurs uniques, élégants et entièrement sur mesure, conçus pour "
    "refléter votre personnalité et votre art de vivre."
)
HERO_TAGLINE = "ARCHITECTURE INTÉRIEURE  •  DESIGN  •  MOBILIER  •  SUR MESURE"
ABOUT_TITLE = "À propos de Casa di Lusso"
ABOUT_TEXT = (
    "Casa di Lusso est une maison d’architecture intérieure et de design basée à Tanger, "
    "où le savoir-faire italien rencontre l’élégance de l’art de vivre marocain.\n\n"
    "Nous imaginons et réalisons des espaces résidentiels, commerciaux et hôteliers "
    "d’exception, en associant des marques internationales exclusives, des matériaux de "
    "haute qualité et des solutions entièrement personnalisées.\n\n"
    "De la conception à la réalisation, Casa di Lusso accompagne chaque projet avec "
    "exigence, créativité et précision afin de créer des intérieurs raffinés, fonctionnels "
    "et intemporels."
)
SERVICES_HEADING = "Des espaces pensés dans les moindres détails"
SERVICES_INTRO = (
    "Des solutions sur mesure, de la conception à la réalisation, pour créer des espaces "
    "élégants, fonctionnels et durables."
)
SERVICES_TAGLINE = "CONCEPTION  •  SÉLECTION  •  COORDINATION  •  RÉALISATION"

SERVICES = (
    (
        "Design intérieur d’exception",
        "Nous imaginons des intérieurs raffinés et harmonieux, conçus pour refléter votre "
        "personnalité et sublimer votre art de vivre.",
    ),
    (
        "Architecture et conception",
        "Nous créons des projets architecturaux uniques où l’esthétique, la fonctionnalité "
        "et l’innovation s’unissent avec précision.",
    ),
    (
        "Aménagement sur mesure",
        "Nous optimisons et transformons chaque espace grâce à des solutions personnalisées, "
        "parfaitement adaptées à vos besoins.",
    ),
    (
        "Conseil en décoration",
        "Nous vous accompagnons dans le choix des matières, des couleurs, du mobilier et des "
        "finitions afin de créer une ambiance élégante et cohérente.",
    ),
    (
        "Gestion et suivi de projet",
        "De la première esquisse à la livraison finale, nous coordonnons chaque étape avec "
        "rigueur pour garantir une réalisation fidèle à votre vision.",
    ),
)

PREVIOUS_SERVICES = (
    ("Design intérieur de luxe", "Création d’espaces élégants et modernes adaptés à votre style de vie."),
    ("Architecture & conception", "Conception de projets architecturaux uniques et personnalisés"),
    ("Aménagement sur mesure", "Optimisation et transformation de vos espaces."),
    ("Conseil en décoration", "Accompagnement dans le choix des matériaux, couleurs et styles."),
    ("Suivi de projet", "Gestion complète de votre projet du début à la fin."),
)


def update_homepage_copy(apps, schema_editor):
    SiteSettings = apps.get_model("website", "SiteSettings")
    Service = apps.get_model("website", "Service")

    SiteSettings.objects.filter(singleton_key="site").update(
        hero_title="L’exception au quotidien",
        hero_text=HERO_TEXT,
        hero_tagline=HERO_TAGLINE,
        about_title=ABOUT_TITLE,
        about_text=ABOUT_TEXT,
        services_heading=SERVICES_HEADING,
        services_intro=SERVICES_INTRO,
        services_tagline=SERVICES_TAGLINE,
    )
    for order, (title, description) in enumerate(SERVICES):
        service, _ = Service.objects.get_or_create(order=order, defaults={"title": title})
        service.title = title
        service.description = description
        service.is_active = True
        service.save(update_fields=("title", "description", "is_active"))


def restore_homepage_copy(apps, schema_editor):
    SiteSettings = apps.get_model("website", "SiteSettings")
    Service = apps.get_model("website", "Service")

    SiteSettings.objects.filter(singleton_key="site").update(
        hero_text=(
            "Nous concevons des espaces et des expériences uniques alliant design, "
            "élégance et excellence sur mesure."
        ),
        about_title="À propos",
        about_text=(
            "Casa di Lusso est une marque dédiée à l’univers du luxe et du design. Nous "
            "transformons vos idées en créations uniques, élégantes et raffinées.\n\n"
            "Our showroom brings together the world’s most prestigious brands, all under "
            "one roof, delivering results that are truly unmatched."
        ),
    )
    for order, (title, description) in enumerate(PREVIOUS_SERVICES):
        Service.objects.filter(order=order).update(title=title, description=description)


class Migration(migrations.Migration):
    dependencies = [("website", "0003_sitesettings_singleton_key_and_more")]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="hero_tagline",
            field=models.CharField(default=HERO_TAGLINE, max_length=220, verbose_name="Signature du héros"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="services_heading",
            field=models.CharField(default=SERVICES_HEADING, max_length=180, verbose_name="Accroche services"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="services_intro",
            field=models.TextField(default=SERVICES_INTRO, verbose_name="Introduction services"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="services_tagline",
            field=models.CharField(default=SERVICES_TAGLINE, max_length=220, verbose_name="Signature services"),
        ),
        migrations.RunPython(update_homepage_copy, restore_homepage_copy),
    ]
