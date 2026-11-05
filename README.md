# Vinicius Rodrigues · Portfolio

Personal portfolio in Brazilian Portuguese, built with semantic HTML, CSS and a small JavaScript enhancement. No build step or application dependencies.

**Website:** https://viniciusrodriguesai.github.io/

## Local preview

Run `python -m http.server 4173` from this directory, then open http://localhost:4173.

## Update

- `index.html`: content, project descriptions, evidence links, contact and metadata.
- `styles.css`: responsive layout, typography and reduced-motion support.
- `script.js`: optional email-copy button, with an accessible failure message.
- `assets/`: authentic project capture, locally hosted font, curriculum, favicon and social preview.
- `scripts/create_resume.py`: public-facing curriculum generator; requires ReportLab. Run from the repository root.

Push to `main` to update GitHub Pages. Keep `.nojekyll` in the root.

## Sources and assets

- Creator Growth screenshot: `docs/images/next-experiment.png` from [the project](https://github.com/viniciusrodriguesai/creator-growth-feedback-loop). Figures shown belong to analyzed public videos, not growth caused by this product.
- Resume Match schematic: the fictional Alex Example resume and [documented demonstration](https://github.com/viniciusrodriguesai/resume-agent-system/blob/main/docs/DEMO.md). Labeled as a diagram, not a screenshot.
- Credit chart: exact ROC-AUC values from [UCI_RESULTS.md](https://github.com/viniciusrodriguesai/credit-risk-classification/blob/main/docs/UCI_RESULTS.md). UCI replication and Home Credit study are distinct.
- Manrope: locally hosted variable font, distributed under the included SIL Open Font License in `assets/Manrope-OFL.txt`.
- Favicon and social preview: original typographic artwork.

No analytics, cookies, external font requests or contact-form backend. GitHub Pages hosting has its own operational logging.
