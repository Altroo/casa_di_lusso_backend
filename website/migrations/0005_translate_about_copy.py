from django.db import migrations


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


def translate_about_copy(apps, schema_editor):
    SiteSettings = apps.get_model("website", "SiteSettings")
    SiteSettings.objects.filter(singleton_key="site").update(
        about_title=ABOUT_TITLE,
        about_text=ABOUT_TEXT,
    )


class Migration(migrations.Migration):
    dependencies = [("website", "0004_refresh_homepage_copy")]

    operations = [
        migrations.RunPython(translate_about_copy, migrations.RunPython.noop),
    ]
