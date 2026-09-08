import nh3


# Only editorial formatting: no scripts, embeds, remote images, or layout CSS.
_cleaner = nh3.Cleaner(
    tags={"p", "br", "h2", "h3", "h4", "strong", "b", "em", "i", "u", "s", "span",
          "ul", "ol", "li", "blockquote", "a", "hr", "table", "thead", "tbody", "tr", "th", "td"},
    clean_content_tags={"script", "style", "iframe", "object", "svg", "math"},
    attributes={"a": {"href", "title"}, "*": {"style"}, "td": {"colspan", "rowspan"},
                "th": {"colspan", "rowspan"}},
    filter_style_properties={"text-align", "font-weight", "font-style", "text-decoration"},
    url_schemes={"http", "https", "mailto", "tel"},
    link_rel="noopener noreferrer",
)


def sanitize_article_html(value):
    return _cleaner.clean(value or "")
