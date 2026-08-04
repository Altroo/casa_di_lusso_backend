from django.db import migrations


def seed_figma_content(apps, schema_editor):
    SiteSettings = apps.get_model("website", "SiteSettings")
    ValueItem = apps.get_model("website", "ValueItem")
    Metric = apps.get_model("website", "Metric")
    Service = apps.get_model("website", "Service")
    PortfolioItem = apps.get_model("website", "PortfolioItem")
    Partner = apps.get_model("website", "Partner")
    Testimonial = apps.get_model("website", "Testimonial")

    SiteSettings.objects.update_or_create(
        pk=1,
        defaults={
            "brand_name": "Casa di Lusso",
            "hero_eyebrow": "CASA DI LUSSO",
            "hero_title": "L’exception au quotidien",
            "hero_text": "Nous concevons des espaces et des expériences uniques alliant design, élégance et excellence sur mesure.",
            "about_title": "À propos",
            "about_text": "Casa di Lusso est une marque dédiée à l’univers du luxe et du design. Nous transformons vos idées en créations uniques, élégantes et raffinées.\n\nOur showroom brings together the world’s most prestigious brands, all under one roof, delivering results that are truly unmatched.",
            "project_title": "Vous avez un projet? Donnons vie à votre vision.",
            "partners_intro": "Nous collaborons avec des partenaires de confiance pour garantir qualité et excellence.",
            "partners_outro": "Nos partenaires partagent notre vision de l’excellence et du raffinement.",
            "video_title": "Découvrez l’univers Casa di Lusso",
            "address": "Route N1, Al Moustakbal Roundabout\n90000\nTangier, Morocco",
            "phone": "+212 123456789",
            "email": "contact@casadilusso.ma",
            "map_embed_url": "https://www.google.com/maps?q=Casa+di+Lusso+Tangier+Morocco&output=embed",
            "map_link": "https://www.google.com/maps/search/?api=1&query=Casa+di+Lusso+Tangier+Morocco",
        },
    )

    values = (
        ("Design haut de gamme", "design"),
        ("Créations sur mesure", "bespoke"),
        ("Qualité et finition premium", "quality"),
        ("Accompagnement personnalisé", "support"),
    )
    for order, (title, icon) in enumerate(values):
        ValueItem.objects.update_or_create(
            title=title,
            defaults={"icon": icon, "order": order, "is_active": True},
        )

    metrics = (
        ("Clients servis", "[ 180 +]"),
        ("années d'expérience", "[ 10 +]"),
        ("projets livrés", "[200 +]"),
        ("Client satisfait", "[45 +]"),
    )
    for order, (title, value) in enumerate(metrics):
        Metric.objects.update_or_create(
            title=title,
            defaults={"value": value, "order": order, "is_active": True},
        )

    services = (
        ("Design intérieur de luxe", "Création d’espaces élégants et modernes adaptés à votre style de vie."),
        ("Architecture & conception", "Conception de projets architecturaux uniques et personnalisés"),
        ("Aménagement sur mesure", "Optimisation et transformation de vos espaces."),
        ("Conseil en décoration", "Accompagnement dans le choix des matériaux, couleurs et styles."),
        ("Suivi de projet", "Gestion complète de votre projet du début à la fin."),
    )
    for order, (title, description) in enumerate(services):
        Service.objects.update_or_create(
            title=title,
            defaults={"description": description, "order": order, "is_active": True},
        )

    portfolio = (
        ("Cuisine Kali", "/assets/casa/partner-kali.jpg"),
        ("Bomma", "/assets/casa/partner-bomma.jpg"),
        ("Living Collection", "/assets/casa/partner-images-20.png"),
        ("Fragments Lighting", "/assets/casa/partner-fragments.jpg"),
        ("Giessegi Living", "/assets/casa/partner-giessegi.jpg"),
    )
    for order, (title, fallback_path) in enumerate(portfolio):
        PortfolioItem.objects.update_or_create(
            title=title,
            defaults={
                "fallback_path": fallback_path,
                "alt_text": title,
                "order": order,
                "is_active": True,
            },
        )

    partners = ("Flaminia", "Bomma", "Kali", "Giessegi", "Vibia")
    for order, title in enumerate(partners):
        Partner.objects.update_or_create(
            title=title,
            defaults={"order": order, "is_active": True},
        )

    testimonials = (
        "Un excellent endroit pour acheter du mobilier de bureau : le personnel est compétent, efficace et serviable, et propose de grandes marques. J'y retournerai avec plaisir et je le recommande vivement à tous mes amis et à ma famille.",
        "Quel que soit le design que vous recherchez, vous trouverez assurément votre bonheur ici. N'hésitez pas à vérifier par vous-même.",
        "C'est le moment de vous procurer les meilleurs meubles à des prix attractifs dans notre magasin. Superbe collection.",
    )
    for order, quote in enumerate(testimonials):
        Testimonial.objects.update_or_create(
            title=f"Témoignage {order + 1}",
            defaults={"quote": quote, "order": order, "is_active": True},
        )


def reverse_seed(apps, schema_editor):
    model_names = (
        "Testimonial",
        "Partner",
        "PortfolioItem",
        "Service",
        "Metric",
        "ValueItem",
        "SiteSettings",
    )
    for model_name in model_names:
        apps.get_model("website", model_name).objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("website", "0001_initial")]
    operations = [migrations.RunPython(seed_figma_content, reverse_seed)]
