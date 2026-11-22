"""Write engine/data/<slug>.json for batch 4 of preview leads (22 Nov 2026).

Only 1 lead today: 9 were already made earlier on 22 Nov (batch 3), and the runbook allows at most 10 a day.
Every fact comes from the business's own Which? Trusted Traders page or its own website.
Reviews are real 5-star Which? reviews, word for word (trimmed with … only).
Photos: Unsplash (download_asset called for each one), credited per site.
"""
import json, pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
U = "https://images.unsplash.com/photo-{}?ixlib=rb-4.1.0&auto=format&fit=crop&w={}&q=80"
PH = {  # photo id -> (photographer, username)
    "1676210134190-3f2c0d5cf58d": ("Timur Shakerzianov", "shaker_jpg"),
    "1676210134188-4c05dd172f89": ("Timur Shakerzianov", "shaker_jpg"),
    "1763485955497-f5ef5d178698": ("Peter Muniz", "petepxl"),
}
UTM = "?utm_source=simonrobert_web_design&utm_medium=referral"


def credits(ids):
    seen = []
    for i in ids:
        p = PH[i]
        if p not in seen:
            seen.append(p)
    links = [f'<a href="https://unsplash.com/@{u}{UTM}">{n}</a>' for n, u in seen]
    names = links[0] if len(links) == 1 else ", ".join(links[:-1]) + " and " + links[-1]
    return f'Stock photos for this preview by {names} on <a href="https://unsplash.com/{UTM}">Unsplash</a>'


def svc(title, text, icon, img=None, alt="", tag=None):
    s = {"title": title, "text": text, "icon": icon}
    if img:
        s["image"] = U.format(img, 1400)
        s["image_alt"] = alt
    if tag:
        s["tag"] = tag
    return s


def rev(text, where, who=None):
    return {"text": text, "who": who or f"Customer in {where}", "label": "Which? review"}


STEPS = [
    {"title": "Get in touch", "text": "Call, or send the quote form with a few details. Photos help."},
    {"title": "We take a look", "text": "We talk it through, look at the job and give you a clear quote."},
    {"title": "Job done properly", "text": "The work is done with care and the site left clean and tidy."},
]
REV_INTRO = "Real reviews from customers on Which? Trusted Traders."


def lead(slug, accent, biz, seo, hero, pills, marquee, services, reviews, jobs, faqs, cta, areas, photos, free_quotes=False):
    hero_img, hero_alt = hero.pop("img")
    d = {
        "slug": slug,
        "mode": "preview",
        "accent": accent,
        "business": biz,
        "seo": seo,
        "hero": {**hero, "image": U.format(hero_img, 2000), "image_alt": hero_alt},
        "pills": pills,
        "marquee": marquee,
        "services": services,
        "work": {"enabled": False},
        "steps": STEPS,
        "reviews": {"heading": ["What customers", "say about us."], "intro": REV_INTRO, "items": reviews},
        "quote": {"intro": "Three quick steps and we’ll get back to you.", "jobs": jobs},
        "faqs": faqs,
        "cta": {"heading": cta},
        "areas": areas,
        "credits": credits([hero_img] + photos),
    }
    if free_quotes:
        d["free_quotes"] = True
    (DATA / f"{slug}.json").write_text(json.dumps(d, indent=2, ensure_ascii=False))
    return slug


WHICH_FAQ = lambda name: {"q": "Can I read more reviews?", "a": f"Yes. {name} is a Which? Trusted Trader, and you can read all our customer reviews on our Which? page."}
QUOTE_FAQ = lambda phone: {"q": "How do I get a quote?", "a": f"Use the quote form on this page or call {phone}. A few photos of the job help us give you an accurate price."}


made = []

# 1. Kings Plumbing & Heating Limited (Maidenhead) --------------------------------
made.append(lead(
    "kings-plumbing-heating", "#EF7D1A",
    {"name": "Kings Plumbing & Heating", "short": "Kings", "sub": "Plumbing & Heating", "logo_icon": "drop",
     "trade": "Plumbers & heating engineers", "town": "Maidenhead", "county": "Berkshire",
     "phone": "01628 337477", "phone_tel": "01628337477", "email": "info@kingsplumbing.co.uk",
     "hours": "", "company_line": "Kings Plumbing & Heating Limited · Company no. 04553090"},
    {"title": "Kings Plumbing & Heating – Plumbers & Heating Engineers in Maidenhead",
     "description": "Family-run plumbing, heating and bathrooms in Maidenhead since 1979. Boilers, central heating, bathroom refurbishments and power flushing. Gas Safe registered."},
    {"eyebrow": "Maidenhead · Berkshire", "h1": "Plumbing & heating,", "h1_accent": "since 1979.",
     "lead": "A family-run business with qualified, experienced plumbers, ready for anything from emergencies to efficient central heating systems and bespoke bathroom installations.",
     "img": ("1676210134190-3f2c0d5cf58d", "Heating engineer working on a hot water cylinder")},
    ["Which? Trusted Trader", "Serving Maidenhead since 1979", "Gas Safe registered", "Worcester Bosch accredited"],
    ["Boiler installation", "Boiler servicing", "Central heating", "Radiators", "Bathrooms", "Wet rooms", "Power flushing", "Unvented cylinders", "Water softeners", "Emergency plumbing"],
    {"eyebrow": "What we do", "heading": ["Family run,", "proud of our work."],
     "intro": "We are equipped to deal with a vast range of plumbing and heating work, and we pride ourselves on our professionalism, reliability and expertise.",
     "items": [
         svc("Boiler installation", "Efficient boilers, with the system designed to fit neatly into your home. We look at the whole system, not just the boiler.", "flame", "1676210134188-4c05dd172f89", "Plumber working on pipework in a wall"),
         svc("Bathrooms & wet rooms", "Bathroom design and refurbishment, with tile samples and computer aided designs so your final decision is the right one.", "sparkle", "1763485955497-f5ef5d178698", "Modern bathroom with double vanity and walk-in shower"),
         svc("Servicing & repairs", "Boiler servicing, boiler repairs and gas safety checks.", "wrench"),
         svc("Central heating & radiators", "Radiators and central heating systems, plus power flushing.", "house"),
         svc("Hot water & water softeners", "Unvented cylinders and water softeners installed and maintained.", "drop"),
         svc("Emergency plumbing", "No call out charge, and we make sure we are there when you call.", "shield"),
     ]},
    [rev("Russ designed, project managed and fitted a lovely bathroom that replaced a very dated and bodged 90s suite. It looks so incredibly nice… It's clear Russ is very knowledgeable and has high standards, so I have no hesitation in recommending this company.", "Berkshire"),
     rev("Kings completely removed my ancient and failing central heating system and installed a new one. Everything now works perfectly. Russell, who did most of the work, was unfailingly pleasant and left everything tidy. I would recommend Kings.", "Berkshire"),
     rev("Since 2013 when Mike & Russell replaced our central heating system, we have been fortunate to be able to call on them for all our heating and plumbing needs… They are completely reliable and their work is first class!", "Windsor and Maidenhead")],
    [["New boiler", "flame"], ["Service or repair", "wrench"], ["Bathroom", "sparkle"], ["Heating", "house"], ["Plumbing", "drop"], ["Something else", "other"]],
    [WHICH_FAQ("Kings Plumbing & Heating"),
     {"q": "Do you charge a call out fee?", "a": "No. There’s no call out charge."},
     {"q": "How do you keep disruption down on a bathroom job?", "a": "We keep dust down to a minimum, make sure you have the facilities you need each evening, and clean and tidy up each night."},
     {"q": "Which areas do you cover?", "a": "Maidenhead and the surrounding areas."},
     QUOTE_FAQ("01628 337477")],
    "Boiler, heating or bathroom job?",
    ["Maidenhead", "Marlow", "Holyport", "Burnham", "Hurley"],
    ["1676210134188-4c05dd172f89", "1763485955497-f5ef5d178698"],
    free_quotes=True,
))

print("\n".join(made))
