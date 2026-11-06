# LaDarius Jackson

Personal portfolio for LaDarius Jackson, published with GitHub Pages from this repository. The GitHub profile uses that spelling. Some project READMEs spell the given name Ladarius.

The page is static HTML, CSS, and JavaScript. It keeps a short film title card, then the three public studies a reviewer can actually open: credit risk, loan approval, and fraud review. Holdout measurements, planning dollars, and business outcomes are labeled separately. Open pull requests are described as not merged.

Live site, once Pages is enabled: [https://ladariusjackson1.github.io/](https://ladariusjackson1.github.io/)

## Run it locally

From the repository root:

```bash
python3 -m http.server 8080
```

Open [http://127.0.0.1:8080/](http://127.0.0.1:8080/). Use a local server. Root-absolute paths such as `/css/styles.css` do not resolve if you open `index.html` as a file.

## Check the build

```bash
python3 scripts/check_site.py
```

The script writes a deployable copy to `_site/` and fails if a required section, README figure, or source link is missing. It also fails if the page contains an email address, a phone number, a LinkedIn URL, an unverified PTIN, or a “Live demo” label on an app that was not verified as public.

GitHub Actions runs the same script on every pull request (`.github/workflows/pages.yml`). A push to `main` uploads `_site` and deploys it.

## GitHub Pages setting

In the repository: **Settings → Pages → Build and deployment → Source = GitHub Actions**.

The workflow cannot turn that setting on by itself. Until the source is GitHub Actions, the site will not publish, even if the workflow file is on `main`.

## What the page is allowed to claim

Project figures are copied from the public READMEs. Nothing is estimated, rounded into a new metric, or taken from a fork.

| Reel | Source |
| --- | --- |
| Credit risk | [credit-risk-prediction](https://github.com/ladariusjackson1/credit-risk-prediction) |
| Loan approval | [loan-approval-prediction](https://github.com/ladariusjackson1/loan-approval-prediction) |
| Fraud review | [fraud-detection-ml](https://github.com/ladariusjackson1/fraud-detection-ml) |
| Daily sales forecast | [revenue-prediction-model](https://github.com/ladariusjackson1/revenue-prediction-model) |
| Double Eagle Financial | [double-eagle-financial-site](https://github.com/ladariusjackson1/double-eagle-financial-site) |
| Elite Concrete sample | [elite-concrete](https://github.com/ladariusjackson1/elite-concrete) |
| Double Eagle Agency | [double-eagle-agency-site](https://github.com/ladariusjackson1/double-eagle-agency-site) |

The three desk GIFs are the files committed on `main` in those repos (`docs/credit-desk-demo.gif`, `docs/demo.gif`, `docs/review-desk.gif`). The page shows a still first. Play loads the GIF. Churn, lead scoring, and the other revenue-repo studies do not publish a headline number, so the page does not invent one.

School, degree, minor, May 2027, Olive Branch, tax preparer, QuickBooks ProAdvisor, and Double Eagle Financial LLC follow the public GitHub profile. The page does not state a PTIN, a class year, an employer, or a salary.

On 6 Nov 2026, unauthenticated requests to the three Streamlit URLs in those READMEs were redirected to a Streamlit sign-in page, and `doubleeaglefinancial.com` returned HTTP 404. The page says so. The Elite Concrete sample returned HTTP 200. Pull request 3 is merged on each flagship `main` (credit `e4a0933`, loan `25bd00c`, fraud `5ec1eec`). The page describes that code as on `main` and still does not treat the Streamlit hosts as verified public demos.

## Motion

The title card plays once per browser tab, then the letterbox bars settle. Project frames tilt under a fine pointer. `prefers-reduced-motion: reduce` skips the title card, the drift, and the tilt. Demo recordings stay still until Play in every browser, so the large GIFs are not part of the first load.

## Contact

GitHub only. No LinkedIn URL is published, because none is on the public profile.

## Layout

```
index.html          Portfolio
404.html            Unknown paths
css/styles.css      Film styling, including reduced motion
js/main.js          Intro, reveals, tilt, the current scene label
assets/reel/        Demo GIFs and stills
assets/fonts/       Self-hosted text
.github/workflows/pages.yml
scripts/check_site.py
```
