#!/usr/bin/env python3
"""Assemble _site and fail if the portfolio is missing required facts."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PAGES = ("index.html", "404.html")
COPY = ("index.html", "404.html", "css", "js", "assets", "revenue-quality")

REQUIRED = (
    "LaDarius Jackson",
    "spell the given name Ladarius",
    "Business Analytics",
    "University of Mississippi",
    "Computer Science",
    "May 2027",
    "QuickBooks ProAdvisor",
    "Double Eagle Financial LLC",
    "Olive Branch",
    "id=\"projects\"",
    "id=\"skills\"",
    "id=\"about\"",
    "id=\"contact\"",
    "e4a0933",
    "25bd00c",
    "5ec1eec",
    "sign-in page",
    "HTTP 404",
    "not a fair-lending finding",
    "not a drift event",
    "pull/3",
    "Holdout",
    "Planning dollars",
    "prefers-reduced-motion",
    "$22,800",
    "$37,200",
    "8.9%",
    "0.793",
    "0.772",
    "$139,000",
    "$826,400",
    "$965,400",
    "$1,535,000",
    "94.9%",
    "0.703",
    "0.704",
    "0.670",
    "0.89",
    "$10,903",
    "$10,903.354",
    "$6,411.164",
    "$17,314.518",
    "$4,828.164",
    "$6,411",
    "$17,315",
    "76 of 95",
    "18.3",
    "0.752",
    "0.800",
    "$2,102",
    "$5,728",
    "£11,629.44",
    "£9,762,760.55",
    "9668ce5784023b22adbc0ea89b6a859f02bd56d7",
    "/revenue-quality/",
    "no payment date",
    "not a client",
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


def gbp(pence: int) -> str:
    sign = "-" if pence < 0 else ""
    pence = abs(int(pence))
    return f"{sign}£{pence // 100:,}.{pence % 100:02d}"


def verify_revenue_explorer(root: Path) -> None:
    page = root / "revenue-quality" / "index.html"
    snap_path = root / "revenue-quality" / "data" / "uci_snapshot.json"
    if not page.is_file() or not snap_path.is_file():
        fail("revenue explorer or snapshot is missing")
    html = page.read_text(encoding="utf-8")
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    if snap["gross_pence"] + snap["cancellations_pence"] + snap["returns_pence"] != snap["net_pence"]:
        fail("snapshot merchandise identity does not hold")
    required = [
        gbp(snap["net_pence"]),
        gbp(snap["gross_pence"]),
        gbp(snap["cancellations_pence"]),
        gbp(snap["duplicate_extra_pence"]),
        gbp(snap["duplicate_bridge"]["net_if_extras_removed_pence"]),
        gbp(snap["missing_customer_pence"]),
        gbp(snap["adjustment_invoice_pence"]),
        f"{snap['raw_rows']:,}",
        f"{snap['identified_customers']:,}",
        f"{snap['active_one_month_later']:,}",
        f"{snap['raw_rows'] - snap['partial_rows'] - snap['unparseable_rows'] - snap['non_product_rows'] - snap['bad_price_rows']:,}",
        "recon_components_equal_net",
        "recon_lines_equal_daily",
        snap["xlsx_sha256"],
        "CC BY 4.0",
        "9668ce5784023b22adbc0ea89b6a859f02bd56d7",
    ]
    for item in required:
        if item not in html:
            fail(f"explorer HTML does not show snapshot value: {item}")
    uk = snap["countries"][0]
    if uk["country"] != "United Kingdom" or f"{uk['share_bps'] / 100:.2f}%" not in html:
        fail("explorer country table does not match the snapshot")
    for name in (
        "uci_snapshot.json",
        "country_revenue.csv",
        "cohort_by_month.csv",
        "daily_merchandise.csv",
    ):
        text = (root / "revenue-quality" / "data" / name).read_text(encoding="utf-8")
        header = text.splitlines()[0].lower()
        if "customer_id" in header or "customerid" in header or "invoiceno" in header:
            fail(f"{name} publishes a customer or invoice identifier")
        if re.search(r"\b(api[_-]?key|secret|password)\b", text, re.I):
            fail(f"{name} contains a secret-like field")
    if html.count('class="table-scroll"') != 2:
        fail("explorer tables are not in keyboard-scrollable regions")


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
    if "linkedin.com" in blob.lower() or "LINKEDIN_PLACEHOLDER" in blob:
        fail("do not publish a LinkedIn URL or an empty LinkedIn placeholder")
    if "active PTIN" in blob or ">Senior<" in index:
        fail("do not state an unverified PTIN or class year")
    if "Live demo" in index:
        fail("do not label an unverified Streamlit URL as a live demo")
    if "not merged" in index.lower() or "not on main" in index.lower() or "open pull request" in index.lower():
        fail("flagship pull request 3 is merged; do not leave an open-PR label")
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

    verify_revenue_explorer(ROOT)

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
