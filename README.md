# Vinicius Rodrigues · Portfolio

English-first personal portfolio with English, Spanish, Brazilian Portuguese and Simplified Chinese. Built with semantic HTML, CSS and a small JavaScript enhancement. No application dependencies or build step required to serve the site.

**Website:** https://viniciusrodriguesai.github.io/

## Local preview

Run `python -m http.server 4173` from this directory, then open http://localhost:4173.

## Update

- `index.html`: content, project descriptions, evidence links, contact and metadata.
- `styles.css`: responsive layout, typography and reduced-motion support.
- `script.js`: language selection, optional preference persistence, localized metadata and accessible email-copy feedback.
- `i18n.js`: generated dictionaries for all four languages. Translations run locally, without an external translation service.
- `assets/`: authentic project capture, locally hosted font, curriculum, favicon and social preview.
- `scripts/create_resume.py`: public-facing curriculum generator; requires ReportLab. Run from the repository root.
- `scripts/create_translated_resumes.py`: generates the English and Simplified Chinese PDFs from `scripts/resume_translations.json`. Requires ReportLab, DejaVu Sans and an embeddable Chinese TrueType font; Windows defaults to Microsoft YaHei. Chinese font paths can be overridden with `PORTFOLIO_CJK_FONT` and `PORTFOLIO_CJK_BOLD`.

Push to `main` to update GitHub Pages. Keep `.nojekyll` in the root.

## Languages

First-time visitors see English. The header selector remembers an explicit choice in local storage when available. Shareable `?lang=en`, `?lang=es`, `?lang=pt` and `?lang=zh` URLs override the saved preference. Changing language preserves the current section and expanded project details. If JavaScript or the dictionary fails to load, the static English content remains available.

To edit translations, update `scripts/localization_rows.json`. Each row contains a stable source index followed by English, Spanish and Simplified Chinese. `scripts/localization_source.json` preserves the Portuguese source. Run `python scripts/build_locales.py` (requires BeautifulSoup4) to regenerate `i18n.js` and synchronize the English HTML fallback. Translation markers preserve the identity of text nodes without replacing links, SVGs or project content.

Recorded source quotations and the authentic screenshot retain their original language. Their captions and accessible descriptions are localized. Résumé download links follow the selected language: English, Portuguese or Simplified Chinese. Spanish uses the English PDF, explicitly labeled as English. The static HTML also links to the English PDF, so the default download works without JavaScript.

## Sources and assets

- Creator Growth screenshot: `docs/images/next-experiment.png` from [the project](https://github.com/viniciusrodriguesai/creator-growth-feedback-loop). Figures shown belong to analyzed public videos, not growth caused by this product.
- Resume Match schematic: the fictional Alex Example resume and [documented demonstration](https://github.com/viniciusrodriguesai/resume-agent-system/blob/main/docs/DEMO.md). Labeled as a diagram, not a screenshot.
- Credit chart: exact ROC-AUC values from [UCI_RESULTS.md](https://github.com/viniciusrodriguesai/credit-risk-classification/blob/main/docs/UCI_RESULTS.md). UCI replication and Home Credit study are distinct.
- Manrope: locally hosted variable font, distributed under the included SIL Open Font License in `assets/Manrope-OFL.txt`.
- Favicon and social preview: original typographic artwork.

No analytics, cookies, external font requests or contact-form backend. GitHub Pages hosting has its own operational logging.
