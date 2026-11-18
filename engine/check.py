"""Safety checks to run before every push. Exit code 0 = safe to push.

  python3 engine/check.py           # check data, build everything, browser QA
  python3 engine/check.py --prune   # also delete preview folders whose data file was removed
  python3 engine/check.py --no-browser

What it checks
  1. Every engine/data/*.json has the fields the templates need, valid phone/email,
     and no over-promising words (see BANNED).
  2. Preview reviews are labelled as real reviews (never "Example review").
  3. "free quote" wording only appears where the business itself offers free quotes.
  4. The site builds, and no built page contains template leftovers.
  5. The homepage never links to a client preview (previews stay unlisted).
  6. Every site/p/<slug>/ folder has a matching data file (orphans fail, or are removed with --prune).
  7. Browser QA (if Playwright + Chrome are available): every page on a laptop and a phone
     size, no sideways scrolling, no JavaScript errors.
"""
import json, pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "engine" / "data"
SITE = ROOT / "site"

BANNED = [
    r"\bguarantee[ds]?\b", r"top of google", r"\bno\.? ?1\b", r"number one", r"\bbest in\b",
    r"\bcheapest\b", r"award[- ]winning", r"\b100% satisf", r"lorem ipsum", r"\bdonec\b",
]
REQUIRED = {
    "business": ["name", "short", "sub", "logo_icon", "town", "county", "phone", "phone_tel", "email", "company_line"],
    "seo": ["title", "description"],
    "hero": ["eyebrow", "h1", "h1_accent", "lead", "image", "image_alt"],
}

errors, warnings = [], []


def err(slug, msg):
    errors.append(f"{slug}: {msg}")


def walk_text(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k not in ("credits", "image", "before", "after"):
                yield from walk_text(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_text(v)


def check_data():
    slugs = set()
    for f in sorted(DATA.glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except Exception as e:
            err(f.name, f"not valid JSON ({e})")
            continue
        slug = d.get("slug", f.stem)
        if slug != f.stem:
            err(slug, f"slug does not match file name {f.name}")
        if slug in slugs:
            err(slug, "duplicate slug")
        slugs.add(slug)
        if d.get("mode") not in ("example", "preview", "live"):
            err(slug, "mode must be example, preview or live")
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", d.get("accent", "")):
            err(slug, "accent must be a #RRGGBB colour")
        for section, keys in REQUIRED.items():
            for k in keys:
                if k not in d.get(section, {}):
                    err(slug, f"missing {section}.{k}")
        b = d.get("business", {})
        if b.get("phone_tel") and not re.fullmatch(r"\+?\d{10,13}", b["phone_tel"]):
            err(slug, f"phone_tel '{b['phone_tel']}' should be digits only")
        if b.get("email") and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z.]{2,}", b["email"]):
            err(slug, f"email '{b['email']}' looks wrong")
        items = d.get("services", {}).get("items", [])
        if len(items) < 3:
            err(slug, "needs at least 3 services")
        for s in items:
            if not all(k in s for k in ("title", "text", "icon")):
                err(slug, f"service missing title/text/icon: {s}")
            if s.get("image") and not s.get("image_alt"):
                err(slug, f"service image needs image_alt: {s.get('title')}")
        reviews = d.get("reviews", {}).get("items", [])
        if not reviews:
            err(slug, "needs at least 1 review")
        for r in reviews:
            if d.get("mode") != "example" and "example" in (r.get("label") or "").lower():
                err(slug, "real business must not use 'Example review' labels")
            if len(r.get("text", "")) > 320:
                warnings.append(f"{slug}: a review is long ({len(r['text'])} chars), consider trimming with …")
        if not d.get("areas"):
            err(slug, "needs areas")
        if d.get("mode") == "preview" and "unsplash" in json.dumps(d) and "Unsplash" not in d.get("credits", ""):
            err(slug, "uses Unsplash photos but has no credits line")
        text = " ".join(walk_text(d)).lower()
        for pat in BANNED:
            if re.search(pat, text):
                err(slug, f"over-promising or placeholder wording matched /{pat}/")
        if not d.get("free_quotes") and re.search(r"free (quote|estimate)", text):
            err(slug, "mentions free quotes but free_quotes is not set (only set it if the business says so)")
    return slugs


def check_orphans(slugs, prune):
    pdir = SITE / "p"
    if not pdir.exists():
        return
    for d in sorted(pdir.iterdir()):
        if d.is_dir() and d.name not in slugs:
            if prune:
                shutil.rmtree(d)
                print(f"removed orphan preview site/p/{d.name}/")
            else:
                err(d.name, "site/p folder has no data file (run with --prune to remove it)")


def check_built():
    home = (SITE / "index.html").read_text()
    if re.search(r'href="[^"]*/p/', home):
        err("homepage", "links to a client preview; previews must stay unlisted")
    for page in SITE.rglob("index.html"):
        html = page.read_text()
        rel = page.relative_to(ROOT)
        for leftover in ("{{", "{%", "undefined", "None</", ">None<"):
            body = re.sub(r"<(style|script)[^>]*>.*?</\1>", "", html, flags=re.S)
            if leftover in body:
                err(str(rel), f"contains template leftover '{leftover}'")
        if "/p/" in str(rel) and 'name="robots" content="noindex' not in html:
            err(str(rel), "preview page is missing noindex")


def browser_qa():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        warnings.append("Playwright not installed: skipped browser QA (pip install playwright --break-system-packages)")
        return
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
    pages = sorted(SITE.rglob("index.html"))
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(executable_path=chrome, args=["--no-sandbox"]) if chrome else p.chromium.launch()
        except Exception as e:
            warnings.append(f"Could not start a browser, skipped browser QA ({e})")
            return
        for page in pages:
            for name, w, h in (("laptop", 1366, 900), ("phone", 390, 844)):
                pg = b.new_page(viewport={"width": w, "height": h})
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.route("**/*", lambda r: r.abort() if r.request.url.startswith("http") else r.continue_())
                pg.goto(page.as_uri())
                pg.add_style_tag(content=".rv{opacity:1!important;transform:none!important}")
                pg.wait_for_timeout(250)
                over = pg.evaluate("document.documentElement.scrollWidth > innerWidth + 1")
                rel = page.relative_to(ROOT)
                if over:
                    err(str(rel), f"scrolls sideways on {name}")
                if errs:
                    err(str(rel), f"JavaScript error on {name}: {errs[0][:120]}")
                pg.close()
        b.close()
    print(f"browser QA: {len(pages)} pages x 2 sizes")


def main():
    prune = "--prune" in sys.argv
    slugs = check_data()
    if not errors:
        r = subprocess.run([sys.executable, str(ROOT / "engine" / "build.py")], capture_output=True, text=True)
        if r.returncode:
            err("build", r.stderr.strip()[-400:])
    check_orphans(slugs, prune)
    if not errors:
        check_built()
    if not errors and "--no-browser" not in sys.argv:
        browser_qa()
    for w in warnings:
        print("WARNING", w)
    if errors:
        print("\nNOT SAFE TO PUSH:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print(f"\nAll checks passed ({len(slugs)} data files). Safe to push.")


if __name__ == "__main__":
    main()
