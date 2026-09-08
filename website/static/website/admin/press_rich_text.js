(function () {
    const TINYMCE_SRC = "https://cdn.jsdelivr.net/npm/tinymce@7/tinymce.min.js";
    const TINYMCE_BASE_URL = "https://cdn.jsdelivr.net/npm/tinymce@7";

    const loadScript = (src) =>
        new Promise((resolve, reject) => {
            const existing = document.querySelector(`script[src="${src}"]`);
            if (existing) {
                existing.addEventListener("load", resolve, { once: true });
                existing.addEventListener("error", reject, { once: true });
                if (window.tinymce) resolve();
                return;
            }

            const script = document.createElement("script");
            script.src = src;
            script.referrerPolicy = "no-referrer";
            script.addEventListener("load", resolve, { once: true });
            script.addEventListener("error", reject, { once: true });
            document.head.appendChild(script);
        });

    const showFallbackMessage = (textarea) => {
        textarea.classList.add("press-rich-text-source--fallback");
        const message = document.createElement("p");
        message.className = "press-rich-text-fallback";
        message.textContent = "L'editeur avance n'a pas pu etre charge. Vous pouvez continuer avec le champ HTML.";
        textarea.insertAdjacentElement("beforebegin", message);
    };

    const initEditor = (textarea) => {
        if (textarea.dataset.richTextReady === "true") return;
        textarea.dataset.richTextReady = "true";

        window.tinymce.init({
            target: textarea,
            base_url: TINYMCE_BASE_URL,
            suffix: ".min",
            license_key: "gpl",
            branding: false,
            promotion: false,
            height: 560,
            min_height: 420,
            resize: true,
            statusbar: true,
            menubar: "file edit view insert format tools table help",
            plugins:
                "advlist autolink lists link charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime table wordcount help",
            toolbar: [
                "undo redo | blocks | bold italic underline strikethrough | removeformat",
                "alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link blockquote table | preview fullscreen code",
            ],
            toolbar_mode: "wrap",
            block_formats: "Paragraphe=p; Titre 2=h2; Titre 3=h3; Titre 4=h4; Citation=blockquote",
            font_family_formats:
                "Arial=arial,helvetica,sans-serif; Georgia=georgia,palatino,serif; Times New Roman=times new roman,times,serif; Verdana=verdana,geneva,sans-serif",
            font_size_formats: "12px 14px 16px 18px 20px 24px 28px 32px 36px",
            paste_data_images: false,
            convert_urls: false,
            link_default_target: "_blank",
            table_default_attributes: {
                border: "1",
            },
            table_default_styles: {
                width: "100%",
                "border-collapse": "collapse",
            },
            content_style: [
                "body { font-family: Arial, Helvetica, sans-serif; font-size: 15px; line-height: 1.7; color: #141310; }",
                "h2, h3, h4 { font-family: Georgia, 'Times New Roman', serif; font-weight: 400; line-height: 1.2; }",
                "blockquote { border-left: 4px solid #c9a84c; margin-left: 0; padding-left: 16px; color: #5f5a52; }",
                "table { border-collapse: collapse; width: 100%; }",
                "td, th { border: 1px solid #d6d0c4; padding: 8px; }",
            ].join(" "),
            setup: (editor) => {
                const sync = () => editor.save();
                editor.on("change input undo redo keyup", sync);
                editor.on("init", () => {
                    textarea.classList.add("press-rich-text-source--enhanced");
                    sync();
                });
            },
        });
    };

    const initAllEditors = async () => {
        const textareas = Array.from(document.querySelectorAll("textarea.press-rich-text-source"));
        if (!textareas.length) return;

        try {
            await loadScript(TINYMCE_SRC);
            textareas.forEach(initEditor);
        } catch {
            textareas.forEach(showFallbackMessage);
        }
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initAllEditors, { once: true });
    } else {
        initAllEditors();
    }
})();
