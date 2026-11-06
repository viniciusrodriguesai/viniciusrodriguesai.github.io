# Vinicius Rodrigues · Portfolio

English-first personal portfolio with English, Spanish, Brazilian Portuguese, French, Simplified Chinese, Korean and Hindi. Built with semantic HTML, CSS and a small JavaScript enhancement. No application dependencies or build step required to serve the site.

**Website:** https://viniciusrodriguesai.github.io/

## Local preview

Run `python -m http.server 4173` from this directory, then open http://localhost:4173.

## Update

- `index.html`: content, project descriptions, evidence links, contact and metadata.
- `styles.css`: responsive layout, typography and reduced-motion support.
- `script.js`: language selection, optional preference persistence, localized metadata and accessible email-copy feedback.
- `i18n.js`: generated dictionaries for all seven languages. Translations run locally, without an external translation service.
- `assets/`: authentic project capture, locally hosted font, curriculum, favicon and social preview.
- `scripts/create_resume.py`: public-facing curriculum generator; requires ReportLab. Run from the repository root.
- `scripts/create_translated_resumes.py`: generates English, Spanish, French, Chinese, Korean and Hindi PDFs from `scripts/resume_translations.json` and `scripts/resume_extra_translations.json`. Pass locale codes to regenerate only selected versions, e.g. `python scripts/create_translated_resumes.py es fr ko hi`. Requires ReportLab, fontTools and DejaVu Sans. Windows defaults to Microsoft YaHei for Chinese, Malgun Gothic for Korean and Nirmala UI for Hindi. Hindi also requires `uharfbuzz` and ReportLab shaping support; Unicode ActualText spans preserve logical text for compatible PDF readers. Selected font subsets are embedded in each PDF; font files are not published as site assets.

Push to `main` to update GitHub Pages. Keep `.nojekyll` in the root.

## Languages

First-time visitors see English. The header selector remembers an explicit choice in local storage when available. Shareable `?lang=en`, `?lang=es`, `?lang=pt`, `?lang=fr`, `?lang=zh`, `?lang=ko` and `?lang=hi` URLs override the saved preference. Changing language preserves the current section and expanded project details. If JavaScript or the dictionary fails to load, the static English content remains available.

To edit translations, update `scripts/localization_rows.json` (stable source index followed by English, Spanish and Simplified Chinese) or `scripts/localization_extra_rows.json` (index followed by French, Korean and Hindi). `scripts/localization_source.json` preserves the Portuguese source. Run `python scripts/build_locales.py` (requires BeautifulSoup4) to regenerate `i18n.js` and synchronize the English HTML fallback. The builder rejects incomplete locales. Translation markers preserve the identity of text nodes without replacing links, SVGs or project content.

Recorded source quotations and the authentic screenshot retain their original language. Their captions and accessible descriptions are localized. Every language has its own résumé PDF: English, Spanish, Portuguese, French, Simplified Chinese, Korean and Hindi. All three download buttons update their target, filename and document-language hint when the visitor changes language. The static HTML also links to the English PDF, so the default download works without JavaScript. Translations retain the same factual content and English-proficiency description.

## Sources and assets

- Creator Growth screenshot: `docs/images/next-experiment.png` from [the project](https://github.com/viniciusrodriguesai/creator-growth-feedback-loop). Figures shown belong to analyzed public videos, not growth caused by this product.
- Creator Growth walkthrough: user-provided screen recording, compressed to H.264/AAC MP4 at 15 fps without reducing the frame dimensions. The player loads the video only when opened.
- Resume Match schematic: the fictional Alex Example resume and [documented demonstration](https://github.com/viniciusrodriguesai/resume-agent-system/blob/main/docs/DEMO.md). Labeled as a diagram, not a screenshot.
- Credit chart: exact ROC-AUC values from [UCI_RESULTS.md](https://github.com/viniciusrodriguesai/credit-risk-classification/blob/main/docs/UCI_RESULTS.md). UCI replication and Home Credit study are distinct.
- Manrope: locally hosted variable font, distributed under the included SIL Open Font License in `assets/Manrope-OFL.txt`.
- Favicon and social preview: original typographic artwork.

[Cloudflare Web Analytics](https://developers.cloudflare.com/web-analytics/about/) collects page views and visits through a browser beacon without analytics cookies. There are no external font requests or contact-form backend. GitHub Pages hosting has its own operational logging.
