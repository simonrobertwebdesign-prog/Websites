"""Write engine/data/<slug>.json for batch 5 of preview leads (23 Nov 2026).

7 new leads (the 23 Nov scheduled run was skipped, so this batch was made by hand in Simon's chat).
Every fact comes from the business's own Which? Trusted Traders page or its own website.
Reviews are real 5-star Which? reviews, word for word (trimmed with … only).
Photos: Unsplash (download_asset called for each one), credited per site.
"""
import json, pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
U = "https://images.unsplash.com/photo-{}?ixlib=rb-4.1.0&auto=format&fit=crop&w={}&q=80"
PH = {  # photo id -> (photographer, username)
    "1711098256574-7b497260cdc9": ("Elise Brown", "elise_flauntdigital"),
    "1719324923613-ff0884b031ed": ("Tile Merchant Ireland", "tilemerchant"),
    "1734079692147-c6fc9438a2d0": ("FRAEM GmbH", "fraem"),
    "1701850009190-2859ba2aeea6": ("Solømen", "solomen"),
    "1604177772727-521c04d3bdb5": ("Jon Moore", "thejmoore"),
    "1617720356637-6264c1c0b4bb": ("Oladipo Adejumo", "eniyato"),
    "1683115096447-5d01c11d3ead": ("Ryno Marais", "ryno_marais"),
    "1683115099191-51e617fc5ff1": ("Ryno Marais", "ryno_marais"),
    "1683115099260-5d5ae7e71a09": ("Ryno Marais", "ryno_marais"),
    "1754322449005-bdc38c631682": ("Zack Masters", "masters25"),
    "1754321860056-ca7254d5e7ac": ("Zack Masters", "masters25"),
    "1631300313270-227604e71ea5": ("henry perks", "hjkp"),
    "1732660513320-a6b489f3fece": ("Marc Zeman", "der_zeman"),
    "1618840626133-54463084a141": ("Peter Herrmann", "tama66"),
    "1650551182991-b07558247564": ("Immo Wegmann", "tinkerman"),
    "1581037417787-dda6c19e06ad": ("Lachlan Matthews", "lachiee"),
    "1792630862663-5efa4de633e3": ("Josh Lemmon", "wolfie_website"),
    "1607708131130-19ed5e90043b": ("Shelter", "shelter"),
    "1562259949-e8e7689d7828": ("Theme Photos", "themephotos"),
    "1652829069862-87874e119527": ("Callum Hill", "inkyhills"),
    "1672130515395-32583062f72b": ("Piotr Rogalski", "progalski"),
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

# 1. New Century Landscaping Ltd (Oxhey, Watford) ------------------------------
made.append(lead(
    "new-century-landscaping", "#4F8A3C",
    {"name": "New Century Landscaping", "short": "New Century", "sub": "Landscaping", "logo_icon": "leaf",
     "trade": "Landscape gardeners", "town": "Oxhey", "county": "Hertfordshire",
     "phone": "01923 224882", "phone_tel": "01923224882", "email": "new.century@ntlworld.com",
     "hours": "Mon–Fri 8am–5pm", "company_line": "New Century Landscaping Ltd. · Company no. 05772181"},
    {"title": "New Century Landscaping – Landscape Gardeners in Hertfordshire & North West London",
     "description": "Patios, driveways, decking, turfing and complete garden design in Hertfordshire and North West London. Landscaping gardens for over 40 years."},
    {"eyebrow": "Oxhey · Hertfordshire · North West London", "h1": "Where the grass", "h1_accent": "really is greener.",
     "lead": "Landscaping gardens for over 40 years, from small terraced gardens to large commercial premises. Whether it is for the individual client or the busy property developer, we can tailor the landscaping project to your needs.",
     "img": ("1711098256574-7b497260cdc9", "Landscaped garden patio with furniture and plants")},
    ["Which? Trusted Trader", "Established 1982", "Over 40 years landscaping", "Free, friendly expert advice"],
    ["Patios", "Driveways", "Natural stone", "Resin bound stone", "Decking", "Turfing", "Artificial lawns", "Drystone walling", "Garden structures", "Irrigation systems"],
    {"eyebrow": "What we do", "heading": ["Complete gardens,", "built properly."],
     "intro": "We work closely with architects and surveyors, and we can build a complete garden from designs already drawn out.",
     "items": [
         svc("Patios", "Patio installation and maintenance, including natural stone surfacing.", "board", "1719324923613-ff0884b031ed", "Paved patio with outdoor furniture"),
         svc("Driveways", "Driveway installation and maintenance, including resin bonded, resin bound and porous, SUDS compliant surfacing.", "car"),
         svc("Decking & garden structures", "Decking, sheds and shed bases, and other garden structures.", "hammer", "1734079692147-c6fc9438a2d0", "Wooden deck beside a natural stone wall"),
         svc("Lawns & turfing", "Turfing, artificial lawns, artificial green walls and irrigation systems.", "leaf"),
         svc("Walls & hard landscaping", "Hard landscaping and drystone walling.", "house"),
         svc("Garden design", "A complete garden design service, from installing outside lighting to building a water feature.", "sparkle"),
     ]},
    [rev("I am so very happy with New Century Landscaping, they have done a 1st class job! Paul & Matt who actually did the work are very friendly, hard working and did an amazing job! Dave who is the owner of the company is very friendly & gave me a great idea of what to do, really good company & workers would thoroughly recommend.", "Buckinghamshire"),
     rev("Dave and his team laid a new Indian stone path and patio, and refurbished the existing patio. It was completed to schedule and budget. … They respected the existing garden plantings and always left the site tidy. We would certainly recommend them to friends and neighbours.", "Hertfordshire"),
     rev("Dave Leete and his lads did a small height 15.5 metre railway sleeper wall in my garden. … In all, a well done and professional job which looked good and was reasonably priced. I happily recommend this firm to others.", "Hertfordshire")],
    [["Patio", "board"], ["Driveway", "car"], ["Decking", "hammer"], ["Lawn or turf", "leaf"], ["Garden design", "sparkle"], ["Something else", "other"]],
    [WHICH_FAQ("New Century Landscaping"),
     {"q": "Do you work for developers as well as homeowners?", "a": "Yes. We work on everything from small terraced gardens to large commercial premises, for individual clients and property developers."},
     {"q": "Can you build a garden from plans we already have?", "a": "Yes. We work closely with architects and surveyors and can build a complete garden from designs already drawn out."},
     {"q": "Which areas do you cover?", "a": "Hertfordshire and North West London."},
     QUOTE_FAQ("01923 224882")],
    "Planning a new garden?",
    ["Oxhey", "Watford", "Hertfordshire", "North West London"],
    ["1719324923613-ff0884b031ed", "1734079692147-c6fc9438a2d0"],
))

# 2. Attymass Brickwork Limited (North West London) -----------------------------
made.append(lead(
    "attymass-brickwork", "#B5562F",
    {"name": "Attymass Brickwork", "short": "Attymass", "sub": "Brickwork & Building", "logo_icon": "hammer",
     "trade": "Bricklayers & builders", "town": "North West London", "county": "London",
     "phone": "07940 582424", "phone_tel": "07940582424", "email": "john@attymassbrickwork.com",
     "hours": "Mon–Sat 8am–8pm", "company_line": "Attymass Brickwork Limited · Company no. 05543903"},
    {"title": "Attymass Brickwork – Bricklayers & Builders in North West London",
     "description": "Specialists in every aspect of brickwork: new builds, extensions, renovations and all styles of pointing. Formed in 2004, with 30 years in the industry."},
    {"eyebrow": "North West London", "h1": "Brickwork", "h1_accent": "specialists.",
     "lead": "Formed in 2004 and backed by 30 years in the industry. We specialise in every aspect of brickwork, including new builds, extensions, renovations and all styles of pointing on period properties or new builds.",
     "img": ("1701850009190-2859ba2aeea6", "Bricklayer spreading mortar on a brick wall")},
    ["Which? Trusted Trader", "Formed in 2004", "30 years in the industry", "Member of the Guild of Bricklayers"],
    ["New builds", "Extensions", "Renovations", "Pointing", "Heritage brickwork", "Brick & stone cleaning", "Groundworks", "Plastering", "Decorating", "Building maintenance"],
    {"eyebrow": "What we do", "heading": ["From the ground works", "to the finishing trades."],
     "intro": "We have worked on various domestic and commercial properties and grown to undertake all aspects of construction, from the ground works through to the finishing trades.",
     "items": [
         svc("Bricklaying", "New builds, extensions and renovations, with every aspect of brickwork covered.", "hammer", "1617720356637-6264c1c0b4bb", "Builder laying blocks on a wall"),
         svc("Pointing & heritage brickwork", "All styles of pointing on period properties or new builds.", "house", "1604177772727-521c04d3bdb5", "Close-up of a brick wall"),
         svc("Brick & stone cleaning", "Brick and stonework cleaning, plus graffiti and oil stain removal.", "sparkle"),
         svc("Groundworks", "Groundwork, brickwork paving and guttering repairs.", "wrench"),
         svc("Decorating & carpentry", "Plastering, interior and exterior decorating, and carpentry.", "brush"),
         svc("Building maintenance", "A building maintenance service. New for 2026: house clearance.", "shield"),
     ]},
    [rev("John and his team did a fantastic job of cleaning and repointing our house. The team went above and beyond to ensure they delivered the work to the highest standard. … Big thanks to the team we couldn't be happier with the final result.", "Greater London"),
     rev("John and his team were simply fantastic in every way. From initial contact to job completion everything was perfect. The team repointed two chimneys and repaired some brickwork in our very old (400 years) house. Everything was done with utmost care and the final results are just beautiful. …", "Buckinghamshire"),
     rev("Third time I have used Attymass and they did exceptional work as usual. Used them for a full room painting, repair of leaking window, and some brick repointing work around the window.", "Greater London")],
    [["Brickwork", "hammer"], ["Pointing", "house"], ["Cleaning", "sparkle"], ["Groundworks", "wrench"], ["Decorating", "brush"], ["Something else", "other"]],
    [WHICH_FAQ("Attymass Brickwork"),
     {"q": "Do you work on period properties?", "a": "Yes. We do all styles of pointing on period properties as well as new builds."},
     {"q": "Do you take on commercial work?", "a": "Yes. We have worked on various domestic and commercial properties."},
     QUOTE_FAQ("07940 582424")],
    "Got a brickwork job in mind?",
    ["North West London", "Greater London"],
    ["1617720356637-6264c1c0b4bb", "1604177772727-521c04d3bdb5"],
))

# 3. Good With Wood (London) Ltd (Greenford) ------------------------------------
made.append(lead(
    "good-with-wood", "#8A5A2B",
    {"name": "Good With Wood", "short": "Good With Wood", "sub": "Carpentry & Joinery", "logo_icon": "hammer",
     "trade": "Carpenter & joiner", "town": "Greenford", "county": "West London",
     "phone": "07956 372059", "phone_tel": "07956372059", "email": "kevin@goodwithwoodlondon.co.uk",
     "hours": "", "company_line": "Good With Wood (London) Limited · Company no. 09785530"},
    {"title": "Good With Wood – Carpenter & Joiner in Ealing and West London",
     "description": "Kevin Brosnan, carpenter and joiner with over 30 years' experience. Kitchens, bedrooms, bookcases, cabinets and understair storage, made in his own workshop."},
    {"eyebrow": "Greenford · Ealing · West London", "h1": "Carpentry & joinery,", "h1_accent": "start to finish.",
     "lead": "I am a carpenter and joiner with over 30 years' experience. I personally carry out all the works myself from start to finish, and all purpose made units, furniture and joinery are built in my spacious workshop.",
     "img": ("1683115096447-5d01c11d3ead", "Carpenter working on a piece of wood")},
    ["Which? Trusted Trader", "Over 30 years' experience", "Advanced City & Guilds", "Fully insured"],
    ["Kitchens", "Bedroom furniture", "Bookcases", "Cabinets", "Understair storage", "Joinery", "Purpose made units"],
    {"eyebrow": "What I do", "heading": ["Purpose made,", "fitted with care."],
     "intro": "No work is sub contracted out, and I also project manage jobs if required.",
     "items": [
         svc("Joinery & carpentry", "Purpose made units, furniture and joinery, built in my own workshop.", "hammer", "1683115099260-5d5ae7e71a09", "Carpenter cutting a board with a circular saw"),
         svc("Kitchens", "Kitchen design, installation and refurbishment.", "house"),
         svc("Bedroom fitting", "Bedroom fitting, with purpose made units.", "sparkle"),
         svc("Bookcases & cabinets", "Bookcases and cabinets, purpose made for your home.", "board", "1683115099191-51e617fc5ff1", "Woodworking tools hanging on a workshop wall"),
         svc("Understair storage", "Make use of the space under your stairs with purpose made storage.", "wrench"),
         svc("Project management", "I can project manage jobs if required.", "shield"),
     ]},
    [rev("Kevin was one of the best trades I had during my renovation. Very good communication, honest, helpful and dependable. He did an excellent job removing the creaks from my victorian staircase and helped trouble shot and fix some odd jobs. Clearly a very talented carpenter who I wouldn’t hesitate to recommend and use again!", "Greater London"),
     rev("Kevin did a superb job working on our front door, adding peephole and fixing a faulty lock. … He is very attentive to detail and is very good with wood indeed! Kind, punctual and also very helpful advising what tools or hardware will be needed to achieve your vision.", "Greater London"),
     rev("Good With Wood is carpentry of excellence. Kevin runs this business, and is a craftsman of distinction. … Basically, you will get the very highest quality work from Good With Wood at a fair price.", "Greater London")],
    [["Kitchen", "house"], ["Bedroom", "sparkle"], ["Shelves & cabinets", "board"], ["Understairs", "wrench"], ["Joinery", "hammer"], ["Something else", "other"]],
    [{"q": "Can I read more reviews?", "a": "Yes. Good With Wood is a Which? Trusted Trader, and you can read all my customer reviews on my Which? page."},
     {"q": "Who does the work?", "a": "I personally carry out all the works myself from start to finish. No work is sub contracted out."},
     {"q": "Are you insured?", "a": "Yes, I’m fully insured with public liability."},
     {"q": "How do I get a quote?", "a": "Use the quote form on this page or call 07956 372059. A few photos of the job help me give you an accurate price."}],
    "Need something made or fitted?",
    ["Greenford", "Ealing", "West London"],
    ["1683115099260-5d5ae7e71a09", "1683115099191-51e617fc5ff1"],
))

# 4. Urban Treescapes Limited (Rickmansworth) -----------------------------------
made.append(lead(
    "urban-treescapes", "#2E7D4F",
    {"name": "Urban Treescapes", "short": "Urban Treescapes", "sub": "Tree Surgery", "logo_icon": "leaf",
     "trade": "Tree surgeons", "town": "Rickmansworth", "county": "Hertfordshire",
     "phone": "01923 778681", "phone_tel": "01923778681", "email": "info@urbantreescapes.co.uk",
     "hours": "Mon–Fri 8am–5pm", "company_line": "Urban Treescapes Limited · Company no. 07033322"},
    {"title": "Urban Treescapes – Tree Surgeons in Rickmansworth, Croxley & Chorleywood",
     "description": "Family run tree surgery founded in 2009. NPTC qualified team, work to British Standard 3998, free no obligation quotes and advice."},
    {"eyebrow": "Rickmansworth · Croxley · Chorleywood", "h1": "Tree surgery,", "h1_accent": "with care.",
     "lead": "We always take into consideration the needs and requirements of the client alongside the health of the tree, the season and the surrounding environment.",
     "img": ("1754322449005-bdc38c631682", "Tree surgeon working high in a tree with climbing gear")},
    ["Which? Trusted Trader", "Family run since 2009", "NPTC qualified team", "Work to BS 3998"],
    ["Crown reductions", "Re-shapes", "Tree felling", "Deadwooding", "Crown lifting", "Pollarding", "Hedge cutting", "Stump grinding", "Commercial work", "Emergency call outs"],
    {"eyebrow": "What we do", "heading": ["Skilful work,", "friendly service."],
     "intro": "All of our team are fully trained and NPTC qualified, and all work is carried out to British Standard 3998 (Tree Work).",
     "items": [
         svc("Crown reductions & re-shapes", "Reducing and reshaping trees, with the health of the tree in mind.", "leaf", "1631300313270-227604e71ea5", "Tree surgeon working on a tree branch"),
         svc("Tree felling", "Tree felling and removal.", "wrench", "1754321860056-ca7254d5e7ac", "Arborist cutting a tree with a chainsaw"),
         svc("Deadwooding, lifting & pollarding", "Deadwooding, crown lifting and pollarding.", "sparkle"),
         svc("Hedge cutting", "Hedge cutting and maintenance.", "scissors"),
         svc("Stump grinding", "Stump grinding to clear the ground after a tree comes down.", "bolt"),
         svc("Permissions handled", "We carry out TPO and Conservation area checks and apply for council permissions if required, free of charge.", "shield"),
     ]},
    [rev("We’ve been using Urban Treescapes for years and wouldn’t go elsewhere. Danny is very much an expert arborist and very professional in his approach. … I’d have no hesitation in recommending Danny and his colleague for any tree pruning or felling.", "Hertfordshire"),
     rev("This is the second time we’ve asked Urban Treescapes to carry out work in our garden. Once again, they did a brilliant job. This time Danny reduced by 30% and reshaped an overgrown Norway maple near the boundary with our neighbours. …", "Hertfordshire"),
     rev("Danny and Alan did an excellent job of trimming our (very tall) Eucalyptus tree, reducing the crown by about 30% and reshaping it. They did the work safely and carefully, and the end result is brilliant. They were really considerate, tidy and friendly. Would fully recommend them.", "Greater London")],
    [["Reduce or reshape", "leaf"], ["Felling", "wrench"], ["Hedges", "scissors"], ["Stump grinding", "bolt"], ["Emergency", "shield"], ["Something else", "other"]],
    [WHICH_FAQ("Urban Treescapes"),
     {"q": "Do you handle council permissions?", "a": "Yes. We carry out TPO and Conservation area checks and apply for council permissions if required, free of charge for our clients."},
     {"q": "Are you insured?", "a": "Yes. We are fully insured with public liability cover to £5 million and employers liability to £10 million."},
     {"q": "Which areas do you cover?", "a": "Rickmansworth, Croxley, Chorleywood and the surrounding areas."},
     QUOTE_FAQ("01923 778681")],
    "Got a tree that needs work?",
    ["Rickmansworth", "Croxley", "Chorleywood", "Mill End"],
    ["1631300313270-227604e71ea5", "1754321860056-ca7254d5e7ac"],
    free_quotes=True,
))

# 5. Save Your Energy Ltd (Watford) ---------------------------------------------
made.append(lead(
    "save-your-energy", "#D9480F",
    {"name": "Save Your Energy", "short": "Save Your Energy", "sub": "Plumbing & Heating", "logo_icon": "flame",
     "trade": "Plumbing & heating engineers", "town": "Watford", "county": "Hertfordshire",
     "phone": "01923 338285", "phone_tel": "01923338285", "email": "savegas@live.co.uk",
     "hours": "Open 24 hours, 7 days", "company_line": "Save Your Energy Ltd · Company no. 07308920"},
    {"title": "Save Your Energy – Plumbing & Heating Engineers in Watford",
     "description": "Boiler repairs, installations and servicing, central heating and plumbing across Herts, Beds, Bucks and parts of North and North West London. Gas Safe registered."},
    {"eyebrow": "Watford · Herts · Beds · Bucks", "h1": "Plumbing & heating,", "h1_accent": "whatever the job.",
     "lead": "We offer a friendly, reliable service at very competitive prices, whether it's a dripping tap or a new heating system. Over 20 years' experience, fully qualified and insured.",
     "img": ("1732660513320-a6b489f3fece", "Heating engineer at work in a home")},
    ["Which? Trusted Trader", "Gas Safe registered 520291", "Over 20 years' experience", "Worcester Bosch accredited"],
    ["Boiler repairs", "Boiler installation", "Boiler servicing", "Gas safety checks", "Central heating", "Radiators", "Powerflush", "Unvented cylinders", "Water softeners", "Emergency plumbing"],
    {"eyebrow": "What we do", "heading": ["From a dripping tap", "to a new heating system."],
     "intro": "A local plumbing and heating company: Gas Safe registered, CIPHE members and an accredited installer and repairer of Worcester Bosch boilers.",
     "items": [
         svc("Boiler repairs", "Boiler breakdowns diagnosed and repaired.", "wrench", "1618840626133-54463084a141", "Close-up of metal heating pipework"),
         svc("Boiler installation & servicing", "Boiler installation and servicing, including Worcester Bosch boilers.", "flame", "1650551182991-b07558247564", "Pipes and valves on a heating system"),
         svc("Central heating", "Central heating systems installed and serviced, plus radiators, pumps and controls.", "house"),
         svc("Gas safety checks", "Gas safety testing and inspection.", "shield"),
         svc("Plumbing", "Taps, showers, toilets and bathrooms, plus emergency plumbing.", "drop"),
         svc("Cylinders, softeners & powerflush", "Unvented cylinder and water softener installation and maintenance, and powerflushing.", "bolt"),
     ]},
    [rev("Mark came out to us (at my elderly father’s house) at short notice on NYE when the heating broke down. He managed to get it working again to help us into the new year with some warmth – many thanks for helping us out of a tight spot!", "Hertfordshire"),
     rev("I had already had an emergency plumber attend courtesy of my insurance service and had been told they would need to make a hole in my kitchen/toilet wall to fix the leak. … they did not have to knock any hole in my walls. Just replaced the leaking pipe, cleaned up and gave me an invoice to pay. Absolutely first rate service and I would totally recommend them.", "Hertfordshire", "Anne in Hertfordshire"),
     rev("Had an issue with the boiler not working. Mark arrived, introduced himself, showed ID … Diagnosed the issue, provided approx cost, changed the part, checked all the system was working and explained the bill. Good value and would recommend, as arrived also when he said he would.", "Hertfordshire", "Declan in Hertfordshire")],
    [["Boiler repair", "wrench"], ["New boiler", "flame"], ["Service", "check"], ["Heating", "house"], ["Plumbing", "drop"], ["Something else", "other"]],
    [WHICH_FAQ("Save Your Energy"),
     {"q": "Are you Gas Safe registered?", "a": "Yes. Our Gas Safe registration number is 520291."},
     {"q": "Which areas do you cover?", "a": "Herts, Beds, Bucks and some of North and North West London."},
     {"q": "Do you take on small jobs?", "a": "Yes. Whether it’s a dripping tap or a new heating system, we’re happy to help."},
     QUOTE_FAQ("01923 338285")],
    "Boiler, heating or plumbing problem?",
    ["Watford", "Hertfordshire", "Bedfordshire", "Buckinghamshire", "North & North West London"],
    ["1618840626133-54463084a141", "1650551182991-b07558247564"],
))

# 6. G Hill & Sons Limited (Minster Lovell, Witney) -----------------------------
made.append(lead(
    "g-hill-and-sons", "#C27C0E",
    {"name": "G Hill & Sons", "short": "G Hill & Sons", "sub": "Driveways & Surfacing", "logo_icon": "car",
     "trade": "Driveway & surfacing contractors", "town": "Minster Lovell", "county": "Oxfordshire",
     "phone": "01993 775568", "phone_tel": "01993775568", "email": "gordonhill.sons@btopenworld.com",
     "hours": "", "company_line": "G Hill & Sons Limited · Company no. 04641457"},
    {"title": "G Hill & Sons – Driveways, Road Construction & Surfacing in Oxfordshire",
     "description": "Family business in Minster Lovell with over 40 years' experience. Tarmac and asphalt drives, resin, block paving, patios and road surfacing across Oxfordshire."},
    {"eyebrow": "Minster Lovell · Witney · Oxfordshire", "h1": "From driveways", "h1_accent": "to road construction.",
     "lead": "A long established family business in Minster Lovell, with over 40 years' experience and expertise across Oxfordshire and the surrounding counties.",
     "img": ("1581037417787-dda6c19e06ad", "Freshly surfaced road between trees")},
    ["Which? Trusted Trader", "Over 40 years' experience", "Local authority approved", "Federation of Master Builders"],
    ["Tarmac drives", "Asphalt drives", "Resin bound stone", "Resin bonded stone", "Block paving", "Patios", "Natural stone", "Porous surfacing", "Road surfacing", "Concrete"],
    {"eyebrow": "What we do", "heading": ["Driveways and roads,", "done properly."],
     "intro": "We hold all the relevant street works qualifications, are fully insured, and are a local authority and county council approved contractor.",
     "items": [
         svc("Tarmac & asphalt drives", "Tarmac and asphalt driveways, laid and maintained.", "car", "1792630862663-5efa4de633e3", "Long asphalt driveway leading to a house"),
         svc("Resin driveways", "Resin bound and resin bonded stone surfacing.", "sparkle"),
         svc("Block paving & patios", "Block paving, natural stone surfacing and patio installation and maintenance.", "board", "1607708131130-19ed5e90043b", "Close-up of brick paving"),
         svc("Road construction & surfacing", "Road construction and surfacing, with all the relevant street works qualifications.", "wrench"),
         svc("Porous surfacing", "Porous, SUDS compliant surfacing.", "drop"),
         svc("Approved & insured", "Fully insured, and members of Constructionline, the Guild of Master Craftsmen and the Federation of Master Builders.", "shield"),
     ]},
    [rev("Gordon and his team of lads resurfaced our shared drive in tarmac. The quote was very reasonable, they turned up on time and their work was efficient and quick. … They were very respectful, didn’t hear any bad language, they tidied up as they worked and completed the work in a day. Would definitely recommend!", "Oxfordshire"),
     rev("Gordon and team repaired and resurfaced a part of the road, for our private lane. They were excellent, gave a good quote, came at the day and time stated and did exactly what was agreed, They were friendly and helpful and it was clear they worked as a team. …", "Oxfordshire"),
     rev("My son and I are very pleased with my new resin driveway and footpaths. Gordon Hill and Sons acted professionally and efficiently and worked well as a team; they were punctual and friendly. … They charged a fair price, and liaised well with the team who laid the resin on the final day. We are delighted with the finished driveway …", "Gloucestershire")],
    [["Driveway", "car"], ["Resin", "sparkle"], ["Block paving", "board"], ["Road or lane", "wrench"], ["Patio", "house"], ["Something else", "other"]],
    [WHICH_FAQ("G Hill & Sons"),
     {"q": "Are you approved and insured?", "a": "Yes. We are fully insured and a local authority and county council approved contractor, with all the relevant street works qualifications."},
     {"q": "Which areas do you cover?", "a": "Oxfordshire and the surrounding counties."},
     QUOTE_FAQ("01993 775568")],
    "Need a new driveway or surface?",
    ["Minster Lovell", "Witney", "Oxfordshire", "Surrounding counties"],
    ["1792630862663-5efa4de633e3", "1607708131130-19ed5e90043b"],
    free_quotes=True,
))

# 7. Andrew Farkas Limited – AFL Decorating (Harrow) ----------------------------
made.append(lead(
    "afl-decorating", "#5B4BB7",
    {"name": "AFL Decorating", "short": "AFL", "sub": "Painting & Decorating", "logo_icon": "brush",
     "trade": "Painters & decorators", "town": "Harrow", "county": "Middlesex",
     "phone": "07951 706 547", "phone_tel": "07951706547", "email": "andrewfarkas@hotmail.co.uk",
     "hours": "Mon–Sat 8am–8pm", "company_line": "Andrew Farkas Limited · Company no. 04821805"},
    {"title": "AFL Decorating – Painters & Decorators in Harrow, London",
     "description": "Andrew Farkas Limited: quality painting and decorating since 1992, covering London and the Home Counties. Interior and exterior decorating, wallpapering, plastering and more."},
    {"eyebrow": "Harrow · London · Home Counties", "h1": "Painting & decorating,", "h1_accent": "since 1992.",
     "lead": "A client centred business, fully insured, focused on value for money while keeping the highest standards. We can manage your project from start to finish.",
     "img": ("1562259949-e8e7689d7828", "Paint roller applying blue paint to a wall")},
    ["Which? Trusted Trader", "Established 1992", "Fully insured", "Traditional or eco-friendly materials"],
    ["Interior decorating", "Exterior decorating", "Wallpapering", "Wall murals", "Hand painted kitchens", "Plastering", "Coving", "Floor sanding", "Doors", "Schools & commercial"],
    {"eyebrow": "What we do", "heading": ["Quality decorating,", "start to finish."],
     "intro": "We are able to use traditional materials or eco-friendly alternatives, depending on what you need.",
     "items": [
         svc("Interior decorating", "Painting and decorating inside your home, managed from start to finish.", "brush", "1652829069862-87874e119527", "Paint roller with fresh paint"),
         svc("Exterior decorating", "Exterior painting and protection.", "house"),
         svc("Wallpapering & murals", "Wallpapering and wall murals.", "board", "1672130515395-32583062f72b", "Bedroom wall with a floral pattern"),
         svc("Hand painted kitchens", "Give your kitchen a new look with a hand painted finish.", "sparkle"),
         svc("Plastering & coving", "Plastering, skimming, rendering, coving and plaster mouldings.", "wrench"),
         svc("Floors, doors & carpentry", "Wood flooring, floor sanding and polishing, door repairs and carpentry.", "hammer"),
     ]},
    [rev("Andrew Farkas and his team worked very efficiently. They carried out external painting and repaired garage doors and a gate. The work was carried out as agreed and according to budget. Andrew and his team were helpful, reliable and kept me fully informed. I am very pleased with the result and would use them again. Highly recommended.", "Greater London"),
     rev("Detailed quote (which was stuck to), good communications throughout, excellent work and thorough cleaning up afterwards. We had the dining room repaired and decorated - strong recommendation from me.", "Greater London"),
     rev("I recently received a quote for the work required. The work commenced at the arranged time and date and was completed in time to my satisfaction. The painter/decorator was more than helpful and went the 'extra mile' to do all that I requested. …", "Greater London")],
    [["Interior", "brush"], ["Exterior", "house"], ["Wallpaper", "board"], ["Kitchen", "sparkle"], ["Plastering", "wrench"], ["Something else", "other"]],
    [{"q": "Can I read more reviews?", "a": "Yes. Andrew Farkas Ltd is a Which? Trusted Trader, and you can read all our customer reviews on our Which? page."},
     {"q": "Do you take on schools and commercial work?", "a": "Yes. As well as homes, we decorate schools and commercial premises."},
     {"q": "Which areas do you cover?", "a": "London and the Home Counties."},
     QUOTE_FAQ("07951 706 547")],
    "Got a room or a house that needs decorating?",
    ["Harrow", "London", "Middlesex", "Home Counties"],
    ["1652829069862-87874e119527", "1672130515395-32583062f72b"],
))

print("\n".join(made))
