# Ladarius Jackson

Personal portfolio for Ladarius Jackson, published with GitHub Pages from this repository.

The page is a static site: HTML, CSS, and JavaScript, with no framework and no install step. It opens like a short film title card, then presents the public analytics work for a recruiter who wants the decision, the dollar figure, and the limit of the study.

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

The script writes a deployable copy to `_site/` and fails if a required section, demo GIF, source link, or README figure is missing. It also fails if the page contains an email address, a phone number, or a LinkedIn URL.

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

The three desk GIFs are the files committed in those repos (`docs/credit-desk-demo.gif`, `docs/demo.gif`, `docs/review-desk.gif`). They load lazily. Churn, lead scoring, and the other revenue-repo studies do not publish a headline number in their READMEs, so the page does not invent one.

School, degree, minor, May 2027, Olive Branch, the PTIN, the QuickBooks ProAdvisor credential, and Double Eagle Financial LLC are stated in the site copy. The PTIN number itself is not published here.

## Motion

The title card plays once per browser tab, then the letterbox bars settle. Project frames tilt and glow under a fine pointer. Scene numbers drift slightly on scroll. `prefers-reduced-motion: reduce` skips the title card, the drift, and the tilt, and shows a still from each demo until you press Play demo.

## LinkedIn

Contact is the GitHub profile only. In `index.html`, the contact section has an HTML comment marked `LINKEDIN_PLACEHOLDER`. Replace that comment with a real profile URL when one exists. Do not add a guessed link.

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
