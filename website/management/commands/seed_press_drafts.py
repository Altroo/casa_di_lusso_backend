from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from website.models import PressArticle, PressCategory


EXAMPLES = (
    ("vita-gessi-caffe", "Vita Gessi Caffè", "bespoke-blog1.png",
     "Gessi transforme un geste quotidien en une véritable expérience de design.",
     "Avec Vita Gessi Caffè, Gessi transforme un geste quotidien en une véritable expérience de design. "
     "L’innovation associe l’univers de l’eau au plaisir du café dans une solution pensée pour les cuisines contemporaines les plus raffinées. "
     "Élégante, intuitive et discrètement technologique, elle reflète la vision de la maison italienne : faire de la fonctionnalité un élément à part entière de l’esthétique de l’espace."),
    ("active-surfaces", "Active Surfaces", "bespoke-blog2.png",
     "Ariostea donne à la céramique une dimension supplémentaire. Au-delà de l’esthétique, ces surfaces sont conçues pour contribuer activement à l’hygiène et au bien-être des espaces intérieurs comme extérieurs.",
     "Ariostea donne à la céramique une dimension supplémentaire. Au-delà de l’esthétique, ces surfaces sont conçues pour contribuer activement à l’hygiène et au bien-être des espaces intérieurs comme extérieurs."),
    ("gessi-haute-culture", "Gessi Haute Culture", "bespoke-blog3.png",
     "Avec Haute Culture, Gessi porte sa vision du design à son expression la plus exclusive.",
     "Avec Haute Culture, Gessi porte sa vision du design à son expression la plus exclusive."),
)


class Command(BaseCommand):
    help = "Importe les trois exemples Figma en brouillons, sans modifier les articles existants ni envoyer de newsletters."

    def add_arguments(self, parser):
        parser.add_argument("--assets-dir", required=True, type=Path)

    def handle(self, *args, **options):
        directory = options["assets_dir"]
        for _, _, name, _, _ in EXAMPLES:
            if not (directory / name).is_file():
                raise CommandError(f"Image absente : {name}")
        categories = list(PressCategory.objects.filter(is_active=True))
        if not categories:
            raise CommandError("Créez d’abord les catégories presse.")
        with transaction.atomic():
            for order, (slug, title, image, excerpt, body) in enumerate(EXAMPLES):
                article, created = PressArticle.objects.get_or_create(slug=slug, defaults={
                    "title": title, "excerpt": excerpt, "content_title": title,
                    "body_html": f"<p>{body}</p>", "sort_order": order, "is_published": False,
                    "image_alt": title,
                })
                if created:
                    with (directory / image).open("rb") as source:
                        article.image_file.save(image, File(source))
                    article.categories.set(categories)
                self.stdout.write(f"{slug}: {'brouillon créé' if created else 'article existant conservé'}")
