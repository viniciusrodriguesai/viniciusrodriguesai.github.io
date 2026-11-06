# Vinicius Rodrigues · Portfolio

English-first personal portfolio with English, Spanish, Brazilian Portuguese, French, German, Italian, Russian, Simplified Chinese, Japanese, Korean and Hindi. Built with semantic HTML, CSS and a small JavaScript enhancement. No application dependencies or build step required to serve the site.

**Website:** https://viniciusrodriguesai.github.io/

## Local preview

Run `python -m http.server 4173` from this directory, then open http://localhost:4173.

## Update

- `index.html`: content, project descriptions, evidence links, contact and metadata.
- `styles.css`: responsive layout, typography and reduced-motion support.
- `script.js`: language selection, optional preference persistence, localized metadata and accessible email-copy feedback.
- `i18n.js`: generated dictionaries for all eleven languages. Translations run locally, without an external translation service.
- `assets/`: authentic project capture, locally hosted font, curriculum, favicon and social preview.
- `scripts/create_resume_2026.py`: generates the ten translated PDFs from the manually translated text in `scripts/resume_2026_manual.json` and `scripts/resume_2026_european.json`. Pass language codes to regenerate selected versions, e.g. `python scripts/create_resume_2026.py de it ru`. Requires ReportLab, PyMuPDF, fontTools, uharfbuzz and DejaVu Sans; on Windows it uses Microsoft YaHei, Yu Gothic, Malgun Gothic and Nirmala UI for the respective scripts. The English PDF is the supplied original with the phone number removed. The older `create_resume.py` and `create_translated_resumes.py` generate previous versions and should not be used for the current résumé.

Push to `main` to update GitHub Pages. Keep `.nojekyll` in the root.

## Languages

First-time visitors see English. The header selector remembers an explicit choice in local storage when available. Shareable `?lang=en`, `?lang=es`, `?lang=pt`, `?lang=fr`, `?lang=de`, `?lang=it`, `?lang=ru`, `?lang=zh`, `?lang=ja`, `?lang=ko` and `?lang=hi` URLs override the saved preference. Changing language preserves the current section and expanded project details. If JavaScript or the dictionary fails to load, the static English content remains available.

To edit translations, update `scripts/localization_rows.json` (stable source index followed by English, Spanish and Simplified Chinese), `scripts/localization_extra_rows.json` (index followed by French, Korean and Hindi), `scripts/localization_ja.json` (Japanese keyed by source index), or `scripts/localization_european.json` (German, Italian and Russian keyed by source index). `scripts/localization_source.json` preserves the Portuguese source. Run `python scripts/build_locales.py` (requires BeautifulSoup4) to regenerate `i18n.js` and synchronize the English HTML fallback. The builder rejects incomplete locales. Translation markers preserve the identity of text nodes without replacing links, SVGs or project content.

The fictional résumé excerpt is translated in each language, with its highlighted skills preserved. The authentic screenshot retains its original language; its caption and accessible description are localized. Every language has its own résumé PDF. All three download buttons update their target, filename and document-language hint when the visitor changes language. The static HTML also links to the English PDF, so the default download works without JavaScript. The translated résumés follow the supplied English document and omit its phone number.

## Sources and assets

- Creator Growth screenshot: `docs/images/next-experiment.png` from [the project](https://github.com/viniciusrodriguesai/creator-growth-feedback-loop). Figures shown belong to analyzed public videos, not growth caused by this product.
- Creator Growth walkthrough: user-provided screen recording, compressed to H.264/AAC MP4 at 15 fps without reducing the frame dimensions. The player loads the video only when opened.
- Resume Match schematic: the fictional Alex Example resume and [documented demonstration](https://github.com/viniciusrodriguesai/resume-agent-system/blob/main/docs/DEMO.md). Labeled as a diagram, not a screenshot.
- Credit chart: exact ROC-AUC values from [UCI_RESULTS.md](https://github.com/viniciusrodriguesai/credit-risk-classification/blob/main/docs/UCI_RESULTS.md). UCI replication and Home Credit study are distinct.
- Manrope: locally hosted variable font, distributed under the included SIL Open Font License in `assets/Manrope-OFL.txt`.
- Favicon and social preview: original typographic artwork.

[Cloudflare Web Analytics](https://developers.cloudflare.com/web-analytics/about/) collects page views and visits through a browser beacon without analytics cookies. There are no external font requests or contact-form backend. GitHub Pages hosting has its own operational logging.
