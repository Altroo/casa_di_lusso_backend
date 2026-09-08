from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model("website", "PressCategory")
    for order, (slug, title) in enumerate((
        ("tendances-deco", "Tendances déco"),
        ("nouveautes-marques", "Nouveautés des marques partenaires"),
        ("conseils-amenagement", "Conseils d’aménagement"),
    )):
        Category.objects.using(schema_editor.connection.alias).get_or_create(
            slug=slug, defaults={"title": title, "order": order},
        )


class Migration(migrations.Migration):
    dependencies = [("website", "0006_press_articles")]
    operations = [migrations.RunPython(seed_categories, migrations.RunPython.noop)]
