"""Write engine/data/<slug>.json for batch 3 of preview leads (22 Nov 2026).

Every fact comes from the business's own Which? Trusted Traders page or its own website.
Reviews are real 5-star Which? reviews, word for word (trimmed with … only).
Photos: Unsplash (download_asset called for each one), credited per site.
"""
import json, pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
U = "https://images.unsplash.com/photo-{}?ixlib=rb-4.1.0&auto=format&fit=crop&w={}&q=80"
PH = {  # photo id -> (photographer, username)
    "1688372199140-cade7ae820fe": ("Ali Mkumbwa", "mkumbwajr"),
    "1562259949-e8e7689d7828": ("Theme Photos", "themephotos"),
    "1722605090433-41d1183a792d": ("Stephen Owen", "stephenowen23"),
    "1650551182991-b07558247564": ("Immo Wegmann", "tinkerman"),
    "1618840626133-54463084a141": ("Peter Herrmann", "tama66"),
    "1732660513320-a6b489f3fece": ("Marc Zeman", "der_zeman"),
    "1593012671976-1422185230fb": ("Brett Jordan", "brett_jordan"),
    "1593786267440-550458cc882a": ("Brett Jordan", "brett_jordan"),
    "1633759593085-1eaeb724fc88": ("Zohair Mirza", "zamclicks"),
    "1518736346281-76873166a64a": ("Michael Jasmund", "jasmund"),
    "1593012672015-4fabc32c67aa": ("Brett Jordan", "brett_jordan"),
    "1628745277862-bc0b2d68c50c": ("Zac Gudakov", "zacgudakov"),
    "1638799869566-b17fa794c4de": ("Lotus Design N Print", "lotusdnp"),
    "1693985120993-e9b203ce7631": ("Andrew Itaga", "and73w"),
    "1652829069862-87874e119527": ("Callum Hill", "inkyhills"),
    "1696987007764-7f8b85dd3033": ("Clay Banks", "claybanks"),
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

# 1. Chris Roach Limited (no website) --------------------------------------------
made.append(lead(
    "chris-roach", "#4A90C2",
    {"name": "Chris Roach", "short": "Chris Roach", "sub": "Painting & Decorating", "logo_icon": "brush",
     "trade": "Painters & decorators", "town": "Ruislip", "county": "Middlesex",
     "phone": "07889 397 102", "phone_tel": "07889397102", "email": "chrisroachlimited@gmail.com",
     "hours": "Mon–Fri 9am–5pm", "company_line": "Chris Roach Limited · Company no. 04699002"},
    {"title": "Chris Roach – Painter & Decorator in Ruislip",
     "description": "Domestic painting and decorating in Ruislip, Eastcote, Pinner, Northwood and nearby. Established in 1986, with over 45 years’ experience."},
    {"eyebrow": "Ruislip · Eastcote · Pinner · Northwood", "h1": "Decorating,", "h1_accent": "done properly.",
     "lead": "A time-served decorator with over 45 years’ experience, offering a hassle-free service from careful preparation to a professional finish. Established in 1986.",
     "img": ("1688372199140-cade7ae820fe", "Decorator painting a wall with a roller")},
    ["Which? Trusted Trader", "Established 1986", "45+ years’ experience", "Public liability insured"],
    ["Interior decorating", "Painting", "Wallpapering", "Hand painted kitchens", "Dust-free sanding", "Water based paints"],
    {"eyebrow": "What we do", "heading": ["Reliable, trustworthy,", "honest, respectful."],
     "intro": "Every job starts with full protection of your home and thorough preparation, for a clean working environment and a professional finish.",
     "items": [
         svc("Interior decorating", "Walls, ceilings and woodwork decorated to a professional standard.", "brush", "1562259949-e8e7689d7828", "Paint roller applying blue paint to a wall"),
         svc("Wallpapering", "Wallpaper hung neatly, including murals.", "board"),
         svc("Hand painted kitchens", "Refurbish your old kitchen with a hand painted finish instead of replacing it.", "sparkle", "1722605090433-41d1183a792d", "Kitchen with white cabinets and marble worktops"),
         svc("Dust-free sanding", "Preparation with a 95% dust-free sanding system.", "shield"),
         svc("Water based paints", "The latest water based paints, for a clean and healthy working environment.", "drop"),
         svc("Careful protection", "Furniture and floors protected before any work starts.", "house"),
     ]},
    [rev("First rate work, neat & tidy and completely professional. Turned up every day dead on time and worked late as necessary. Removed fitting including radiator, door knobs etc. rather than paint/paste around them; and refitted later… Overall, brilliant job.", "Greater London"),
     rev("We have asked Chris back to do various decorating jobs over many years. Genuinely delighted with all his work. Chris is everything you could ask for in a tradesman - helpful, reliable and a good communicator. Very happy to recommend him.", "Greater London"),
     rev("Chris recently completed redecorating my sitting room which has a very high ceiling and had unsightly cracks in the plaster. He is meticulous and methodical in his preparation, takes great care in covering and protecting furniture and flooring, etc and I am delighted with the end result…", "Greater London")],
    [["Painting", "brush"], ["Wallpaper", "board"], ["Kitchen", "sparkle"], ["Whole house", "house"], ["Small job", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("Chris Roach"),
     {"q": "Which areas do you cover?", "a": "Ruislip, Eastcote, Pinner, Northwood, Rickmansworth, The Chalfonts, Gerrards Cross, Chorleywood and the surrounding areas."},
     QUOTE_FAQ("07889 397 102")],
    "Got a room that needs decorating?",
    ["Ruislip", "Eastcote", "Pinner", "Northwood", "Rickmansworth", "The Chalfonts", "Gerrards Cross", "Chorleywood"],
    ["1562259949-e8e7689d7828", "1722605090433-41d1183a792d"],
))

# 2. Phoenix Heating Limited (no website) ----------------------------------------
made.append(lead(
    "phoenix-heating", "#E4572E",
    {"name": "Phoenix Heating", "short": "Phoenix", "sub": "Heating & Plumbing", "logo_icon": "flame",
     "trade": "Heating engineers", "town": "Harrow", "county": "Greater London",
     "phone": "07921 360246", "phone_tel": "07921360246", "email": "kieranbradley1983@gmail.com",
     "hours": "", "company_line": "Phoenix Heating Limited · Company no. 06054794"},
    {"title": "Phoenix Heating – Boilers & Plumbing in Harrow",
     "description": "Boiler installation, servicing and breakdowns, unvented hot water cylinders, water softeners and plumbing in Harrow. Set up in 2007."},
    {"eyebrow": "Harrow · Greater London", "h1": "Boilers & heating,", "h1_accent": "done right.",
     "lead": "Boiler installation, servicing and breakdowns, hot water cylinders, water softeners and plumbing, with high quality workmanship and the best materials. In the trade since 1999.",
     "img": ("1650551182991-b07558247564", "Heating pipes and valves")},
    ["Which? Trusted Trader", "Set up in 2007", "In the trade since 1999", "Boilers & plumbing"],
    ["Boiler installation", "Boiler servicing", "Breakdowns", "Unvented cylinders", "Water softeners", "Radiators", "Power flushing", "Heat pumps"],
    {"eyebrow": "What we do", "heading": ["High quality work,", "the best materials."],
     "intro": "Specialists in boiler installation, servicing and breakdowns, unvented hot water cylinders, water softeners and plumbing.",
     "items": [
         svc("Boiler installation", "New boilers fitted to a high standard.", "flame"),
         svc("Servicing & breakdowns", "Boiler servicing, repairs and breakdowns.", "wrench"),
         svc("Central heating & radiators", "Heating systems, radiators, power flushing and underfloor heating.", "house", "1618840626133-54463084a141", "Close-up of heating pipework"),
         svc("Hot water & water softeners", "Unvented cylinders, immersion heaters and water softeners installed and maintained.", "drop"),
         svc("Gas safety & appliances", "Gas safety checks, gas cookers and gas fires.", "shield"),
         svc("Heat pumps", "Air source and ground source heat pumps.", "leaf"),
     ]},
    [rev("Phoenix Heating always deliver high quality work efficiently, and are reliable and happy to give advice. On this occasion they serviced the boiler, installed TRVs on the radiators, replaced a leaking tap in the kitchen and also replaced the shower hose in the bathroom… I always use Phoenix and highly recommend them.", "Hertfordshire", who="Tom in Hertfordshire"),
     rev("We moved house and needed the boiler serviced in our new home. I selected Kieran from Which? Trusted Traders and am pleased I did so. He came with a colleague. They were very personable and their work was professional and clean The cost was very reasonable and we would be happy to recommend him and to use him again.", "Greater London", who="Stanley in Greater London"),
     rev("I recently had the pleasure of having a new boiler installed by Kieran and his helper Tom, and I couldn’t be more impressed with their service. After being without heating for over a week, Kieran went above and beyond to ensure the boiler was installed to an exceptionally high standard within just a few days…", "Greater London")],
    [["New boiler", "flame"], ["Service or repair", "wrench"], ["Radiators", "house"], ["Hot water", "drop"], ["Plumbing", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("Phoenix Heating"),
     {"q": "What do you specialise in?", "a": "Boiler installation, servicing and breakdowns, unvented hot water cylinders, water softeners and plumbing."},
     QUOTE_FAQ("07921 360246")],
    "Boiler or heating problem?",
    ["Harrow", "Greater London"],
    ["1618840626133-54463084a141"],
))

# 3. L H Building Services (Bristol) Ltd (no website) ----------------------------
made.append(lead(
    "lh-building-services", "#D98E04",
    {"name": "LH Building Services", "short": "LH", "sub": "Building Services", "logo_icon": "house",
     "trade": "Builders", "town": "Bristol", "county": "South Gloucestershire",
     "phone": "0117 931 9917", "phone_tel": "01179319917", "email": "lhbuildingservices@outlook.com",
     "hours": "Mon–Fri 8am–5pm", "company_line": "LH Building Services (Bristol) Ltd · Company no. 09013717"},
    {"title": "LH Building Services – Builders in Bristol",
     "description": "Bristol based building company covering all aspects of building work: extensions, conversions, conservatories, plastering, patios and driveways."},
    {"eyebrow": "Little Stoke · Bristol · South Gloucestershire", "h1": "Building work,", "h1_accent": "start to finish.",
     "lead": "A Bristol based building company covering all aspects of building work, helping you design and build your perfect project.",
     "img": ("1593012671976-1422185230fb", "Building work on a house extension")},
    ["Which? Trusted Trader", "Bristol based", "All aspects of building", "Free quotations"],
    ["Extensions", "Garage conversions", "Conservatories", "Plastering", "Rendering", "Patios", "Driveways", "Re-pointing"],
    {"eyebrow": "What we do", "heading": ["Design and build", "your perfect project."],
     "intro": "With a wide range of experience, we cover all aspects of building work in Bristol and the surrounding areas.",
     "items": [
         svc("Extensions", "Extensions designed and built.", "house", "1593786267440-550458cc882a", "Brick extension being built"),
         svc("Conversions & new builds", "Garage and home conversions, and new builds.", "hammer"),
         svc("Conservatories", "Conservatory repairs, roof replacements and roof conversions.", "sparkle"),
         svc("Plastering & rendering", "Plastering, skimming, rendering, coving and pebble dashing.", "brush"),
         svc("Patios & driveways", "Driveways, patios and natural stone surfacing.", "car"),
         svc("Brickwork & repairs", "Bricklaying, re-pointing and guttering repairs.", "wrench"),
     ]},
    [rev("We are delighted with the service we received from L H Building Services. Mark took a great deal of time and trouble to go through every aspect of the job and made several useful and practical suggestions. We are glad we took his advice. The quote was reasonable and the workmanship outstanding…", "Bristol City"),
     rev("We were very pleased with the work carried out by Lee and his team. We had a ceiling replaced plastering done and doors replaced. This was carried out professionally keeping us informed throughout the work…", "South Gloucestershire"),
     rev("I would like to thank Lee and his team for a fantastic job of replacing my Porch. Always on time, kept you up to date on what’s was going on and clean and tidy…", "Bristol City")],
    [["Extension", "house"], ["Conversion", "hammer"], ["Conservatory", "sparkle"], ["Plastering", "brush"], ["Patio or driveway", "car"], ["Something else", "other"]],
    [WHICH_FAQ("LH Building Services"),
     {"q": "Do you give free quotes?", "a": "Yes. Contact us for a free quotation."},
     {"q": "Which areas do you cover?", "a": "We’re based in Little Stoke and work across Bristol and the surrounding areas."}],
    "Planning a building project?",
    ["Bristol", "Little Stoke", "South Gloucestershire"],
    ["1593786267440-550458cc882a"],
    free_quotes=True,
))

# 4. Roofgard Ltd (no website) -----------------------------------------------------
made.append(lead(
    "roofgard", "#C0392B",
    {"name": "Roofgard", "short": "Roofgard", "sub": "Roofing", "logo_icon": "roof",
     "trade": "Roofers", "town": "Leamington Spa", "county": "Warwickshire",
     "phone": "01926 346364", "phone_tel": "01926346364", "email": "roofgard@mail.com",
     "hours": "", "company_line": "Roofgard Ltd · Company no. 14965353"},
    {"title": "Roofgard – Roofer in Leamington Spa, Warwickshire",
     "description": "Roof replacements, repairs, flat roofing, lead work, chimneys and roofline work in Leamington Spa and Warwickshire."},
    {"eyebrow": "Radford Semele · Leamington Spa · Warwickshire", "h1": "Roofing work,", "h1_accent": "done properly.",
     "lead": "Roof replacements and repairs, flat roofs, lead work, chimneys and roofline in Leamington Spa and across Warwickshire. We look forward to discussing your roofing needs.",
     "img": ("1633759593085-1eaeb724fc88", "Roofer stripping an old roof")},
    ["Which? Trusted Trader", "Leamington Spa based", "Pitched & flat roofs", "Lead work"],
    ["Roof replacement", "Roof repairs", "Flat roofing", "GRP", "Rubber (EPDM)", "Lead work", "Chimneys", "Fascias & soffits"],
    {"eyebrow": "What we do", "heading": ["Your roof,", "looked after."],
     "intro": "From a single repair to a full re-roof, plus flat roofs, lead work and roofline.",
     "items": [
         svc("Roof replacement", "Old roofs stripped and re-covered.", "roof", "1518736346281-76873166a64a", "Dark grey roof tiles"),
         svc("Roof repairs", "Leaks found and fixed, and repointing.", "wrench"),
         svc("Flat roofing", "GRP fibreglass and rubber (EPDM) flat roofs.", "shield"),
         svc("Lead work & chimneys", "Lead work and chimney repairs.", "hammer"),
         svc("Roof lights & skylights", "Roof lights and skylights fitted.", "sparkle"),
         svc("Guttering, fascias & soffits", "Roofline and guttering so rainwater drains away properly.", "drop"),
     ]},
    [rev("Would absolutely recommend RoofGard. Rich is a credit to his profession his communication and time keeping is excellent. We had a few issues with the roof and upon Rich’s visual inspection he provided us with a video of the work required which was appreciated…", "Warwickshire"),
     rev("Richard quoted for a roof replacement, easy guy to get on with, the works commenced ahead of schedule and were completed in a timely manor. The guys on site just got on with the job, no hassle no dramas.The building inspector came out and praised the quality of the installation…", "Warwickshire"),
     rev("Richard and the team stripped and recovered a large single-storey roof. Team arrived when they said they would, worked hard, and did a quality job. Definitely recommended.", "Warwickshire")],
    [["New roof", "roof"], ["Repair", "wrench"], ["Flat roof", "shield"], ["Lead or chimney", "hammer"], ["Guttering", "drop"], ["Something else", "other"]],
    [WHICH_FAQ("Roofgard"),
     {"q": "Do you do emergency roof repairs?", "a": "Yes. We offer an emergency roofing service. Call us to talk it through."},
     QUOTE_FAQ("01926 346364")],
    "Roof leaking or past its best?",
    ["Leamington Spa", "Radford Semele", "Warwickshire"],
    ["1518736346281-76873166a64a"],
))

# 5. K. Spencer Building & Maintenance Limited (no website) ------------------------
made.append(lead(
    "k-spencer-building", "#2A9D8F",
    {"name": "K Spencer Building & Maintenance", "short": "K Spencer", "sub": "Building & Maintenance", "logo_icon": "hammer",
     "trade": "Builders", "town": "Birmingham", "county": "West Midlands",
     "phone": "07973 713050", "phone_tel": "07973713050", "email": "kspencerbuildingandmaintenance@yahoo.co.uk",
     "hours": "", "company_line": "K. Spencer Building & Maintenance Limited · Company no. 06517070"},
    {"title": "K Spencer Building & Maintenance – Builder in Birmingham",
     "description": "Extensions, loft and garage conversions, plastering, porches, conservatories and brickwork in Birmingham and the West Midlands."},
    {"eyebrow": "Birmingham · West Midlands", "h1": "Building work,", "h1_accent": "done right.",
     "lead": "Extensions, loft and garage conversions, plastering, porches, conservatories and brickwork across Birmingham and the West Midlands.",
     "img": ("1593012672015-4fabc32c67aa", "Extension under construction")},
    ["Which? Trusted Trader", "Birmingham based", "Extensions & conversions", "Building & maintenance"],
    ["Extensions", "Loft conversions", "Garage conversions", "Plastering", "Porches", "Conservatories", "Bricklaying", "Re-pointing"],
    {"eyebrow": "What we do", "heading": ["Building work,", "big or small."],
     "intro": "From house building and extensions to plastering, brickwork and guttering repairs.",
     "items": [
         svc("Extensions", "House extensions, planned and built.", "house", "1593786267440-550458cc882a", "Brick extension being built"),
         svc("Loft & garage conversions", "Lofts and garages turned into useful rooms.", "roof"),
         svc("Plastering", "Plastering and making good.", "brush"),
         svc("Porches & conservatories", "Porches, conservatories and orangeries.", "sparkle"),
         svc("Brickwork", "Bricklaying and re-pointing.", "hammer", "1593012671976-1422185230fb", "Building work on a house extension"),
         svc("Repairs & maintenance", "Guttering repairs and property maintenance.", "wrench"),
     ]},
    [rev("Kevin did some sealing works on the roof, repaired a wooden door, applied sealant to windows and fixed some leaks, removed and replaced base boards on a door and tiled an upstairs balcony. He worked quickly and quietly with no fuss. I cannot recommend Kevin highly enough.", "West Midlands"),
     rev("Kev took out the shower unit in my bathroom and installed a bath. He did a fantastic job and I'm so pleased with the result. He was punctual, friendly and efficient and did over and above the agreed work - always going the extra mile…", "Worcestershire"),
     rev("We have used Kevin twice to fit our kitchen including knocking walls down, plastering, brickwork and plumbing. Did a great job both times. Will definitely use him again for more work. Very clean and tidy and friendly.", "West Midlands", who="BeckyM")],
    [["Extension", "house"], ["Conversion", "roof"], ["Plastering", "brush"], ["Porch", "sparkle"], ["Repair", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("K Spencer Building & Maintenance"),
     {"q": "What kind of work do you take on?", "a": "Extensions, loft and garage conversions, plastering, porches, conservatories, brickwork and general maintenance."},
     QUOTE_FAQ("07973 713050")],
    "Got a building job in mind?",
    ["Birmingham", "West Midlands"],
    ["1593786267440-550458cc882a", "1593012671976-1422185230fb"],
))

# 6. I&A Painting and Decorating Ltd (no website) ----------------------------------
made.append(lead(
    "ia-painting-decorating", "#7B2CBF",
    {"name": "I&A Painting & Decorating", "short": "I&A", "sub": "Painting & Decorating", "logo_icon": "brush",
     "trade": "Painters & decorators", "town": "Welwyn Garden City", "county": "Hertfordshire",
     "phone": "07967 649896", "phone_tel": "07967649896", "email": "igarkov46@yahoo.co.uk",
     "hours": "Mon–Sat 8am–6pm", "company_line": "I&A Painting and Decorating Ltd · Company no. 12192781"},
    {"title": "I&A Painting & Decorating – Decorator in Welwyn Garden City",
     "description": "Interior and exterior painting and decorating in Welwyn Garden City and Hertfordshire. Wallpapering, paint effects, panelling and tiling."},
    {"eyebrow": "Welwyn Garden City · Hertfordshire", "h1": "From one room", "h1_accent": "to the whole house.",
     "lead": "Internal and external painting and decorating, from the smallest room in the house to the entire house. We’ll discuss your vision and how to achieve it.",
     "img": ("1693985120993-e9b203ce7631", "Painter using a roller on a wall")},
    ["Which? Trusted Trader", "Interior & exterior", "Specialist paint effects", "Free quotations"],
    ["Painting", "Decorating", "Wallpapering", "Paint effects", "Beading & panelling", "Tiling", "Floor tiling", "Flooring"],
    {"eyebrow": "What we do", "heading": ["A job", "well done."],
     "intro": "Painting, decorating and much more, with a free quotation for every job.",
     "items": [
         svc("Interior decorating", "Rooms painted and decorated, walls, doors and woodwork.", "brush", "1652829069862-87874e119527", "Close-up of a paint roller"),
         svc("Exterior painting", "Exterior painting and decorating.", "house"),
         svc("Wallpapering", "Wallpaper hung neatly.", "board"),
         svc("Paint effects & panelling", "Specialist paint effects, beading and panelling.", "sparkle"),
         svc("Tiling", "Wall and floor tiling.", "hammer"),
         svc("Flooring", "Laminate, vinyl and wood flooring laid.", "wrench"),
     ]},
    [rev("Ivan recently completed a full decoration of our new home, covering everything from the walls to the doors and woodwork. He is a true professional who takes immense pride in his work, delivering precise results with impressive efficiency…", "Hertfordshire"),
     rev("Thorough, professional painting of the outside of the house over 4 continuous days at a fair price. It now looks great! Ivan was helpful and responsive on site.", "Hertfordshire"),
     rev("Ivan recently completed the full painting and decorating of my property and I couldn’t be happier with the result. I contacted him at very short notice. Despite the tight timeframe, he managed to complete the entire job within five days, which was incredibly impressive…", "Hertfordshire")],
    [["Interior", "brush"], ["Exterior", "house"], ["Wallpaper", "board"], ["Panelling", "sparkle"], ["Tiling or flooring", "hammer"], ["Something else", "other"]],
    [WHICH_FAQ("I&A Painting & Decorating"),
     {"q": "Do you give free quotes?", "a": "Yes. Get in touch to discuss the work and a free quotation will be provided."},
     QUOTE_FAQ("07967 649896")],
    "Ready for a fresh look?",
    ["Welwyn Garden City", "Hertfordshire"],
    ["1652829069862-87874e119527"],
    free_quotes=True,
))

# 7. BT Projects (London) Limited (web address shows a security error) ------------
made.append(lead(
    "bt-projects-london", "#1D7874",
    {"name": "BT Projects", "short": "BT Projects", "sub": "Kitchens & Bathrooms", "logo_icon": "drop",
     "trade": "Kitchen & bathroom fitters", "town": "Barnet", "county": "Greater London",
     "phone": "07426 084786", "phone_tel": "07426084786", "email": "info@btprojectslondon.co.uk",
     "hours": "Mon–Sat 8am–6pm", "company_line": "BT Projects (London) Limited · Company no. 10382691"},
    {"title": "BT Projects – Kitchens & Bathrooms in Barnet, London",
     "description": "Kitchen and bathroom design and installation in Barnet and London, from concept through installation and finishing touches."},
    {"eyebrow": "Barnet · North London", "h1": "Kitchens & bathrooms,", "h1_accent": "concept to finish.",
     "lead": "Experienced kitchen and bathroom designers and installers. Our skilled team take care of everything from concept, through installation and finishing touches.",
     "img": ("1696987007764-7f8b85dd3033", "Bathroom with two sinks and a shower")},
    ["Which? Trusted Trader", "Design & installation", "Kitchens & bathrooms", "Barnet based"],
    ["Bathrooms", "Wet rooms", "Accessible bathrooms", "Kitchens", "Tiling", "Flooring", "Extensions", "Refurbishments"],
    {"eyebrow": "What we do", "heading": ["Every detail", "considered."],
     "intro": "Every aesthetic is considered, with our customers’ expectations at the forefront of everything we do.",
     "items": [
         svc("Bathrooms", "Bathroom design, installation and refurbishment.", "drop", "1638799869566-b17fa794c4de", "Bathroom with bath and walk-in shower"),
         svc("Wet rooms & accessible bathrooms", "Wet rooms and accessible bathrooms and showers.", "shield"),
         svc("Kitchens", "Kitchen installation, refurbishment and tiling.", "sparkle", "1628745277862-bc0b2d68c50c", "Kitchen with white and wood units"),
         svc("Tiling & flooring", "Ceramic tiling, wood, laminate and vinyl flooring.", "board"),
         svc("Building work", "Extensions, loft and garage conversions, plastering and porches.", "house"),
         svc("Property refurbishment", "Full refurbishments, plumbing and home maintenance.", "hammer"),
     ]},
    [rev("BT projects renovated our bathroom and we were very happy with the result. Tudor and team were very easy to communicate with and were very helpful in answering all questions. The bathroom was completed to a high standard and was exactly as we wanted it. I would highly recommend BT projects for bathroom renovation.", "Greater London"),
     rev("From our very first meeting with Tudor Bratu, we had a good feeling about working with him. We were absolutely right, Tudor, Catalin, and their team of craftsmen have been truly excellent… The work started on time, finished on time, and bang on budget.", "Greater London"),
     rev("BT Projects, led by Catalin delivered an exceptional bathroom renovation experience. Catalin and John demonstrated professionalism from the initial measurement visit through to the final installation of a delayed sink unit…", "Greater London")],
    [["Bathroom", "drop"], ["Wet room", "shield"], ["Kitchen", "sparkle"], ["Tiling or flooring", "board"], ["Building work", "house"], ["Something else", "other"]],
    [WHICH_FAQ("BT Projects"),
     {"q": "Do you design as well as fit?", "a": "Yes. We take care of everything from concept, through installation and finishing touches."},
     QUOTE_FAQ("07426 084786")],
    "Planning a new kitchen or bathroom?",
    ["Barnet", "Greater London"],
    ["1638799869566-b17fa794c4de", "1628745277862-bc0b2d68c50c"],
))

# 8. Gas Safe Central Heating Limited ---------------------------------------------
made.append(lead(
    "gas-safe-central-heating", "#0077B6",
    {"name": "Gas Safe Central Heating", "short": "Gas Safe", "sub": "Central Heating", "logo_icon": "flame",
     "trade": "Heating engineers", "town": "Solihull", "county": "West Midlands",
     "phone": "0800 834 773", "phone_tel": "0800834773", "email": "info@gassafecentralheating.com",
     "hours": "Mon–Fri 8am–8pm, Sat–Sun 8am–5pm", "company_line": "Gas Safe Central Heating Limited · Company no. 06929869"},
    {"title": "Gas Safe Central Heating – Boilers & Heating in Solihull & Birmingham",
     "description": "Central heating installations, boiler servicing, breakdowns and gas work across Birmingham, Solihull, the West Midlands and Worcestershire."},
    {"eyebrow": "Knowle · Solihull · Birmingham", "h1": "Central heating,", "h1_accent": "fixed prices.",
     "lead": "An established Midlands company specialising in central heating installations, boiler servicing, breakdowns and gas work, with over 30 years’ experience in the sector.",
     "img": ("1732660513320-a6b489f3fece", "Heating engineer at work")},
    ["Which? Trusted Trader", "Worcester Bosch Gold accredited", "30+ years’ experience", "No hourly charge"],
    ["Boiler installation", "Boiler servicing", "Breakdowns", "Central heating", "Radiators", "Gas safety checks", "Unvented cylinders", "Plumbing"],
    {"eyebrow": "What we do", "heading": ["Fixed prices,", "no hourly charge."],
     "intro": "We talk every customer through all stages of the job, respect your property, and clean up when we’re done.",
     "items": [
         svc("Central heating installations", "New central heating systems and boilers installed.", "flame", "1650551182991-b07558247564", "Heating pipes and valves"),
         svc("Boiler servicing", "Regular boiler servicing.", "wrench"),
         svc("Breakdowns & repairs", "Boiler breakdowns and repairs, with a fixed price repair policy.", "clock"),
         svc("Gas work & safety checks", "Gas installation work and gas safety testing.", "shield"),
         svc("Radiators", "Radiators and central heating upgrades.", "house"),
         svc("Plumbing & hot water", "Plumbing, emergency plumbing and unvented cylinders.", "drop"),
     ]},
    [rev("I have use Gas Safe for many years for boiler installation and servicing. Steve has always provided outstanding service and reacts very quickly if you have a problem. They have just installed our first combi boiler and we are delighted with the installation…", "Warwickshire"),
     rev("I’ve used Gas Safe for several years and always get the best service . Extremely reliable and trustworthy. Wouldn’t use anyone else for I know they will get the job done .", "West Midlands"),
     rev("I have used Gas Safe for well over 10 years for boiler installation and servicing. Steve and his team have always provided top quality customer service, nothing is too much trouble and they always respond promptly when needed…", "Warwickshire")],
    [["New boiler", "flame"], ["Service", "wrench"], ["Breakdown", "clock"], ["Gas safety", "shield"], ["Plumbing", "drop"], ["Something else", "other"]],
    [WHICH_FAQ("Gas Safe Central Heating"),
     {"q": "Do you charge by the hour?", "a": "No. We have a fixed price policy and no hourly charge, and we offer a free, no obligation quote and advice."},
     {"q": "Which areas do you cover?", "a": "Birmingham, Solihull, the West Midlands and Worcestershire, within about 50 miles of Birmingham."}],
    "Boiler playing up?",
    ["Birmingham", "Solihull", "Knowle", "Coventry", "Warwick", "Leamington Spa", "Stratford-upon-Avon", "Worcester"],
    ["1650551182991-b07558247564"],
    free_quotes=True,
))

# 9. Solihull Heating and Bathrooms Limited ----------------------------------------
made.append(lead(
    "solihull-heating-bathrooms", "#E76F51",
    {"name": "Solihull Heating & Bathrooms", "short": "SHB", "sub": "Heating & Bathrooms", "logo_icon": "drop",
     "trade": "Heating & bathrooms", "town": "Solihull", "county": "West Midlands",
     "phone": "0121 371 0437", "phone_tel": "01213710437", "email": "james@shb-ltd.co.uk",
     "hours": "", "company_line": "Solihull Heating and Bathrooms Limited · Company no. 09073192"},
    {"title": "Solihull Heating & Bathrooms – Boilers & Bathrooms in Solihull",
     "description": "Boilers, central heating, plumbing and bathrooms across Solihull, Birmingham, Sutton Coldfield and Lichfield. Gas Safe registered engineers."},
    {"eyebrow": "Solihull · Birmingham · Sutton Coldfield", "h1": "Heating & bathrooms,", "h1_accent": "in safe hands.",
     "lead": "Teams covering Solihull, Birmingham and the south of the Midlands, plus Sutton Coldfield, Lichfield and the north. Over a decade’s experience.",
     "img": ("1638799869566-b17fa794c4de", "Bathroom with bath and walk-in shower")},
    ["Which? Trusted Trader", "Gas Safe registered engineers", "NIC electricians", "Accessible bathrooms"],
    ["Boilers", "Central heating", "Bathrooms", "Wet rooms", "Accessible showers", "Plumbing", "Water softeners", "Unvented cylinders"],
    {"eyebrow": "What we do", "heading": ["Prompt, punctual,", "safe and tidy."],
     "intro": "Repairs and call outs are prompt and punctual, and we work to fixed deadlines and stick to them.",
     "items": [
         svc("Boilers & central heating", "Boilers installed, serviced and repaired, and full heating systems.", "flame", "1732660513320-a6b489f3fece", "Heating engineer at work"),
         svc("Bathrooms", "Bathroom design and refurbishment.", "sparkle", "1696987007764-7f8b85dd3033", "Bathroom with two sinks and a shower"),
         svc("Accessible bathrooms", "Bathrooms adapted for ease of use for disabled people and wheelchair users.", "shield"),
         svc("Plumbing", "Plumbing and emergency plumbing.", "wrench"),
         svc("Hot water & water softeners", "Unvented cylinders and water softeners installed and maintained.", "drop"),
         svc("Gas safety", "Gas safety testing and inspection.", "check"),
     ]},
    [rev("Great work done by the boys from Solihull heating and Bathrooms. They did a brilliant job at replacing my full heating system. They're very polite and their work is to a very high standard. Thanks James and team, again. Highly recommend", "West Midlands", who="Chris Steen"),
     rev("Very impressed - rang in to discuss a leaky boiler issue and they took the time to really discuss all my options and what the problem could be rather than just try and send someone out straight away. I felt valued and admire their professionalism. Would defo recommend!", "West Midlands", who="Tony K"),
     rev("Great time keeping, polite, great job, very tidy. Great to be fitted in one day.", "West Midlands", who="Nicholas B, West Midlands")],
    [["Boiler", "flame"], ["Heating", "house"], ["Bathroom", "sparkle"], ["Accessible bathroom", "shield"], ["Plumbing", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("Solihull Heating & Bathrooms"),
     {"q": "Are your engineers qualified?", "a": "Yes. All our engineers are Gas Safe registered and NVQ qualified, and electrical work is done by our NIC electricians."},
     {"q": "Which areas do you cover?", "a": "Solihull, Birmingham and the south of the Midlands, plus Sutton Coldfield, Lichfield and the north of the region."}],
    "Boiler or bathroom project?",
    ["Solihull", "Birmingham", "Sutton Coldfield", "Lichfield", "West Midlands"],
    ["1732660513320-a6b489f3fece", "1696987007764-7f8b85dd3033"],
    free_quotes=True,
))

print("\n".join(made))
