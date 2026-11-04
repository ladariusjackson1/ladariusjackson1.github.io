#!/usr/bin/env python3
"""Assemble _site and fail if the portfolio is missing required facts."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PAGES = ("index.html", "404.html")
COPY = ("index.html", "404.html", "css", "js", "assets")

REQUIRED = (
    "Ladarius Jackson",
    "Business Analytics",
    "University of Mississippi",
    "Computer Science",
    "May 2027",
    "active PTIN",
    "QuickBooks ProAdvisor",
    "Double Eagle Financial LLC",
    "Olive Branch",
    "id=\"projects\"",
    "id=\"skills\"",
    "id=\"about\"",
    "id=\"contact\"",
    "LINKEDIN_PLACEHOLDER",
    "prefers-reduced-motion",
    "$22,800",
    "$37,200",
    "8.9%",
    "0.793",
    "0.772",
    "$137,000",
    "$828,400",
    "$965,400",
    "$1,535,000",
    "94.8%",
    "0.704",
    "0.670",
    "$10,903",
    "$6,411",
    "$17,315",
    "76 of 95",
    "18.3",
    "0.752",
    "0.800",
    "$2,102",
    "$5,728",
    "£11,629.44",
    "£12,283.78",
    "About £654",
    "https://credit-risk-prediction.streamlit.app",
    "https://loan-approval-prediction.streamlit.app",
    "https://fraud-detection-ml.streamlit.app",
    "https://github.com/ladariusjackson1",
    "https://doubleeaglefinancial.com",
    "https://ladariusjackson1.github.io/elite-concrete/",
    "https://github.com/ladariusjackson1/revenue-prediction-model",
    "https://github.com/ladariusjackson1/double-eagle-agency-site",
    "/assets/reel/credit-desk.gif",
    "/assets/reel/loan-desk.gif",
    "/assets/reel/fraud-desk.gif",
    "not a real concrete business",
)

LOCAL_ASSETS = (
    "assets/reel/credit-desk.gif",
    "assets/reel/loan-desk.gif",
    "assets/reel/fraud-desk.gif",
    "assets/reel/credit-desk.jpg",
    "assets/reel/loan-desk.jpg",
    "assets/reel/fraud-desk.jpg",
    "assets/fonts/cormorant-garamond.woff2",
    "assets/fonts/cormorant-garamond-italic.woff2",
    "assets/fonts/outfit.woff2",
    "assets/noise.png",
    "assets/favicon.svg",
    "assets/og.png",
    "assets/apple-touch.png",
    "css/styles.css",
    "js/main.js",
)

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?:\+?1[\s.-]?)?(?:\(\d{3}\)|\d{3})[\s.-]\d{3}[\s.-]\d{4}")
ATTR = re.compile(r"""(?:src|href)\s*=\s*["']([^"']+)["']""", re.I)


def fail(message: str) -> None:
    print(f"check_site: {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    page_404 = (ROOT / "404.html").read_text(encoding="utf-8")
    css = (ROOT / "css" / "styles.css").read_text(encoding="utf-8")
    script = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
    workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")

    for fact in REQUIRED:
        if fact not in index and fact not in css and fact not in script:
            fail(f"missing required text: {fact}")

    blob = "\n".join((index, page_404, css, script))
    if "linkedin.com" in blob.lower():
        fail("a LinkedIn URL is present; leave only the LINKEDIN_PLACEHOLDER comment")
    if "mailto:" in blob.lower() or EMAIL.search(blob):
        fail("an email address is present")
    if "tel:" in blob.lower() or PHONE.search(blob):
        fail("a phone number is present")
    if "prefers-reduced-motion" not in css or "reduce-motion" not in script:
        fail("reduced-motion handling is incomplete")
    if "upload-pages-artifact" not in workflow or "deploy-pages" not in workflow:
        fail("Pages workflow is missing the deploy actions")
    if "FinceptTerminal" in blob:
        fail("forked FinceptTerminal repo should not be presented as a project")

    for rel in LOCAL_ASSETS:
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing asset: {rel}")
        if rel.endswith(".gif") and not path.read_bytes()[:6] in (b"GIF87a", b"GIF89a"):
            fail(f"not a GIF: {rel}")

    for name in PAGES:
        html = (ROOT / name).read_text(encoding="utf-8")
        for ref in ATTR.findall(html):
            if ref.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
                if ref.startswith("http://"):
                    fail(f"{name} uses a non-https URL: {ref}")
                continue
            local = ref.split("#", 1)[0].split("?", 1)[0]
            if not local:
                continue
            target = ROOT / local.lstrip("/")
            if not target.exists():
                fail(f"{name} references missing file: {ref}")

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    for item in COPY:
        src = ROOT / item
        dest = SITE / item
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
    if not (SITE / "index.html").is_file():
        fail("site build did not produce index.html")
    print(f"check_site: ok ({SITE})")


if __name__ == "__main__":
    main()
