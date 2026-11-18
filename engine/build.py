"""Build every business site from engine/data/*.json into site/.

Each data file describes one business. Output paths:
  example mode -> data["outputs"] (e.g. {"premium": "premium-example", "standard": "standard-example"})
  preview mode -> site/p/<slug>/ (premium) and site/p/<slug>/standard/
  live mode    -> site/live/<slug>/ (copied to the client's own Netlify site)

Usage: python3 engine/build.py [slug ...]   (no slugs = build all)
"""
import json, pathlib, sys
from jinja2 import Environment, FileSystemLoader

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENGINE = ROOT / "engine"
SITE = ROOT / "site"

ICONS = {
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"/>',
    "house": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "board": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7h8M8 11h8M8 15h4"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "bulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
    "leaf": '<path d="M5 19c0-8 6-14 15-14 0 9-6 15-14 15"/><path d="M5 19l7-7"/>',
    "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    "flame": '<path d="M12 3c1 3 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3.5 2-4.5 0 2 1 3 2 3 0-3-1-5 1-8.5z"/>',
    "roof": '<path d="M2 12l10-8 10 8"/><path d="M5 10v9h14v-9"/><path d="M9 19v-5h6v5"/>',
    "brush": '<path d="M14 4l6 6-8 8H6v-6l8-8z"/><path d="M12 6l6 6"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
    "wrench": '<path d="M14.5 6.5a4 4 0 0 0-5.3 5.3L4 17l3 3 5.2-5.2a4 4 0 0 0 5.3-5.3l-2.5 2.5-2.5-.5-.5-2.5z"/>',
    "hammer": '<path d="M14 6l4 4-9 9-3-3 9-9"/><path d="M12 4l6 6 3-3-6-6z"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.1 15.9M14.5 14.5L20 20M8.1 8.1L12 12"/>',
    "paw": '<circle cx="7" cy="9" r="2"/><circle cx="12" cy="6" r="2"/><circle cx="17" cy="9" r="2"/><path d="M12 12c-3 0-5 3-5 5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2c0-2-2-5-5-5z"/>',
    "car": '<path d="M5 17h14v-5l-2-5H7l-2 5z"/><circle cx="8" cy="17" r="2"/><circle cx="16" cy="17" r="2"/>',
    "cup": '<path d="M4 8h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M17 10h2a2 2 0 0 1 0 4h-2"/><path d="M8 3v2M12 3v2"/>',
    "dumbbell": '<path d="M6 7v10M18 7v10M3 10v4M21 10v4M6 12h12"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "pin": '<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "check": '<path d="M5 12l5 5L20 7"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "other": '<circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/>',
}


def on_accent(hex_colour):
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    lum = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    # pick whichever of near-black / white gives more contrast on the accent
    dark = (lum + 0.05) / (0.0062 + 0.05)
    light = 1.05 / (lum + 0.05)
    return "#0D1015" if dark >= light else "#FFFFFF"


def outputs_for(d):
    if d.get("outputs"):
        return d["outputs"]
    if d["mode"] == "preview":
        return {"premium": f"p/{d['slug']}", "standard": f"p/{d['slug']}/standard"}
    if d["mode"] == "live":
        return {d.get("tier", "premium"): f"live/{d['slug']}"}
    raise SystemExit(f"{d['slug']}: no outputs for mode {d['mode']}")


def main(slugs):
    env = Environment(loader=FileSystemLoader(str(ENGINE / "templates")),
                      autoescape=True, trim_blocks=True, lstrip_blocks=True)
    env.globals["ICONS"] = ICONS
    files = sorted((ENGINE / "data").glob("*.json"))
    built = []
    for f in files:
        d = json.loads(f.read_text())
        if slugs and d["slug"] not in slugs:
            continue
        d.setdefault("work", {"enabled": False})
        d.setdefault("credits", "")
        for tier, rel in outputs_for(d).items():
            html = env.get_template(f"{tier}.html.j2").render(d=d, accent=d["accent"], on_accent=on_accent(d["accent"]))
            out = SITE / rel / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html)
            built.append(str(out.relative_to(ROOT)))
    print("\n".join(built) or "nothing built")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
