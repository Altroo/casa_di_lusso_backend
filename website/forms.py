from django import forms
from django.utils.html import strip_tags

from .models import PressArticle
from .rich_text import sanitize_article_html


class RichTextWidget(forms.Textarea):
    class Media:
        css = {"all": ("website/admin/press_rich_text.css",)}
        js = ("website/admin/press_rich_text.js",)

    def __init__(self, attrs=None):
        super().__init__({"class": "vLargeTextField press-rich-text-source", "rows": 18, **(attrs or {})})


class PressArticleAdminForm(forms.ModelForm):
    class Meta:
        model = PressArticle
        fields = "__all__"
        widgets = {"body_html": RichTextWidget()}

    def clean(self):
        data = super().clean()
        data["body_html"] = sanitize_article_html(data.get("body_html", ""))
        if data.get("is_published"):
            if not strip_tags(data["body_html"]).replace("&nbsp;", " ").strip():
                self.add_error("body_html", "Rédigez le contenu avant de publier cet article.")
            if not data.get("categories"):
                self.add_error("categories", "Choisissez au moins une catégorie.")
        return data
