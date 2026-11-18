"""Write engine/data/<slug>.json for batch 2 of preview leads (18 Nov 2026).

Every fact comes from the business's own Which? Trusted Traders page or its own website.
Reviews are real 5-star Which? reviews, word for word (trimmed with … only).
Photos: Unsplash (download_asset called for each one), credited per site.
"""
import json, pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
U = "https://images.unsplash.com/photo-{}?ixlib=rb-4.1.0&auto=format&fit=crop&w={}&q=80"
PH = {  # photo id -> (photographer, username)
    "1732660513320-a6b489f3fece": ("Marc Zeman", "der_zeman"),
    "1584622650111-993a426fbf0a": ("Lotus Design N Print", "lotusdnp"),
    "1650551182991-b07558247564": ("Immo Wegmann", "tinkerman"),
    "1562259949-e8e7689d7828": ("Theme Photos", "themephotos"),
    "1688372198189-de6a51777a81": ("Ali Mkumbwa", "mkumbwajr"),
    "1561297331-a9c00b9c2c44": ("Paul Trienekens", "paultrienekens"),
    "1711098256574-7b497260cdc9": ("Elise Brown", "elise_flauntdigital"),
    "1642541744624-7a2a89545a32": ("Paul Arky", "paularky"),
    "1719324923613-ff0884b031ed": ("Tile Merchant Ireland", "tilemerchant"),
    "1688372199140-cade7ae820fe": ("Ali Mkumbwa", "mkumbwajr"),
    "1628745277862-bc0b2d68c50c": ("Zac Gudakov", "zacgudakov"),
    "1659930087003-2d64e33181f7": ("Craft Kitties", "craftkitties"),
    "1771681278369-e2a5480b8c29": ("Clay Banks", "claybanks"),
    "1618840626133-54463084a141": ("Peter Herrmann", "tama66"),
    "1726589004565-bedfba94d3a2": ("Christer Lässman", "lassman"),
    "1754322449185-31f56117ed87": ("Zack Masters", "masters25"),
    "1709560723503-538158e48db8": ("Scott Precious", "scottsalchemy"),
    "1631300313270-227604e71ea5": ("henry perks", "hjkp"),
    "1593012671976-1422185230fb": ("Brett Jordan", "brett_jordan"),
    "1593786267440-550458cc882a": ("Brett Jordan", "brett_jordan"),
    "1722605090433-41d1183a792d": ("Stephen Owen", "stephenowen23"),
    "1631889993959-41b4e9c6e3c5": ("Backbone", "bkbn"),
    "1593012672015-4fabc32c67aa": ("Brett Jordan", "brett_jordan"),
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

# 1. Prestige Heating & Plumbing Ltd (no website) -------------------------------
made.append(lead(
    "prestige-heating-plumbing", "#E4572E",
    {"name": "Prestige Heating & Plumbing", "short": "Prestige", "sub": "Heating & Plumbing", "logo_icon": "flame",
     "trade": "Plumbers & heating engineers", "town": "Chalfont St Peter", "county": "Buckinghamshire",
     "phone": "07956 370323", "phone_tel": "07956370323", "email": "prestigeltd1995@gmail.com",
     "hours": "Mon–Fri 8:30am–6pm", "company_line": "Prestige Heating & Plumbing Limited · Company no. 03852263"},
    {"title": "Prestige Heating & Plumbing – Plumber in Chalfont St Peter",
     "description": "A small, friendly plumbing and heating team based in Chalfont. Boilers, central heating, bathrooms and repairs across West London and the surrounding counties."},
    {"eyebrow": "Chalfont St Peter · Gerrards Cross · Buckinghamshire", "h1": "Plumbing & heating,", "h1_accent": "done properly.",
     "lead": "A small, friendly team based in Chalfont, looking after boilers, heating and bathrooms across West London and the surrounding counties. Established since 1995.",
     "img": ("1732660513320-a6b489f3fece", "Engineer fitting a heating system")},
    ["Which? Trusted Trader", "Gas Safe registered", "Established 1995", "Chartered Institute of Plumbers member"],
    ["Boilers", "Central heating", "Radiators", "Bathrooms", "Wet rooms", "Unvented cylinders", "Power flushing", "Gas safety"],
    {"eyebrow": "What we do", "heading": ["Good, clear", "communication."],
     "intro": "A small team working with each client, where reliability and tidiness are the backbone of the service.",
     "items": [
         svc("Boilers", "Boiler installation, repairs and servicing.", "flame", "1732660513320-a6b489f3fece", "Engineer working on a heating system"),
         svc("Central heating & radiators", "Heating systems installed and serviced, radiators, power flushing and underfloor heating.", "house"),
         svc("Bathrooms & wet rooms", "Bathroom refurbishment, wet rooms and accessible bathrooms and showers.", "sparkle", "1584622650111-993a426fbf0a", "Modern bathroom with walk-in shower"),
         svc("Hot water", "Unvented cylinders, immersion heaters and water softeners installed and maintained.", "drop", "1650551182991-b07558247564", "Pipes and valves"),
         svc("Gas safety", "Gas safety testing and inspection, gas cookers and gas fires.", "shield"),
         svc("Emergency plumbing", "Leaks, breakdowns and gas emergencies.", "wrench"),
     ]},
    [rev("Spoke with Paul and sent him a couple of photos to show him the set up of the sink. He very quickly emailed me back with a quote which was very reasonably priced so I accepted. He was able to fit the work in the next day, so all is now resolved and to an extremely high standard…", "Buckinghamshire"),
     rev("We asked Paul to look at our electric shower which was malfunctioning. He diagnosed the problem on the Thursday, ordered the part the same day and had it delivered and fitted by the Monday. We were so grateful to have such prompt and efficient service…", "Buckinghamshire"),
     rev("Great service, did the job quickly and efficiently when I had been let down by another plumber. Working through the heat, kept me up to date on issues and fixes. Great job, definitely using them again.", "Buckinghamshire")],
    [["Boiler", "flame"], ["Heating", "house"], ["Bathroom", "sparkle"], ["Hot water", "drop"], ["Leak or repair", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("Prestige Heating & Plumbing"),
     {"q": "Which areas do you cover?", "a": "We’re based in Chalfont St Peter and work across West London and the surrounding counties. If you’re further away, just ask."},
     QUOTE_FAQ("07956 370323")],
    "Boiler or plumbing problem?",
    ["Chalfont St Peter", "Gerrards Cross", "Buckinghamshire", "West London"],
    ["1584622650111-993a426fbf0a", "1650551182991-b07558247564"],
))

# 2. Boxmoor Decorating Ltd (no website) ----------------------------------------
made.append(lead(
    "boxmoor-decorating", "#4F7CFF",
    {"name": "Boxmoor Decorating", "short": "Boxmoor", "sub": "Decorating", "logo_icon": "brush",
     "trade": "Painters & decorators", "town": "Hemel Hempstead", "county": "Hertfordshire",
     "phone": "07746 655184", "phone_tel": "07746655184", "email": "boxmoor-decorating@hotmail.com",
     "hours": "Mon–Fri 7am–5:30pm, Sat 9am–2pm", "company_line": "Boxmoor Decorating Limited · Company no. 12394981"},
    {"title": "Boxmoor Decorating – Painters & Decorators in Hemel Hempstead",
     "description": "Interior and exterior painting and decorating in Hemel Hempstead, covering Herts, Beds, Bucks and North London. Over 23 years’ experience."},
    {"eyebrow": "Hemel Hempstead · Herts · Beds · Bucks", "h1": "Decorating,", "h1_accent": "done with care.",
     "lead": "Interior and exterior painting and decorating for homes and businesses across Herts, Beds, Bucks and North London, with over 23 years’ experience behind every job.",
     "img": ("1562259949-e8e7689d7828", "Paint roller applying blue paint to a wall")},
    ["Which? Trusted Trader", "Herts Trading Standards Approved", "23+ years’ experience", "Free quotes"],
    ["Interior painting", "Exterior painting", "Wallpapering", "Wall murals", "Stain & varnish", "Flooring", "Insurance work"],
    {"eyebrow": "What we do", "heading": ["Quality, reliable,", "clean."],
     "intro": "We take time to understand what each customer wants, then do the job properly and leave your home tidy.",
     "items": [
         svc("Interior decorating", "Walls, ceilings and woodwork painted to a clean finish.", "brush", "1688372198189-de6a51777a81", "Decorator painting a wall with a roller"),
         svc("Exterior painting", "Exterior painting and decorating for homes and businesses.", "house"),
         svc("Wallpapering & murals", "Wallpaper hanging, including busy designs and wall murals.", "board"),
         svc("Dust-free sanding", "Sanding with a Mirka dust extractor system to protect your home.", "sparkle", "1561297331-a9c00b9c2c44", "Sanding a wooden surface"),
         svc("Flooring", "Carpets, wooden flooring and lino supplied and fitted.", "hammer"),
         svc("Finishing touches", "Curtain rails, picture hanging and furniture put back to finish the room.", "wrench"),
     ]},
    [rev("I'm absolutely delighted with the work from Paul and David. The wallpapering (busy design) and bedroom painting have completely transformed the room. The finish is excellent; everything was done with great care and attention to detail, and the result looks fantastic…", "Hertfordshire"),
     rev("Paul, assisted by David, decorated three bedrooms for me. He was great from start to finish - giving advice on the best paints to use and colour matching perfectly. The work was finished to a very high standard and the house left clean and tidy at the end of every day…", "Hertfordshire"),
     rev("Paul was excellent, he did my whole house and the process was completely stress free, the result? Absolute perfection.", "Hertfordshire")],
    [["Interior", "brush"], ["Exterior", "house"], ["Wallpaper", "board"], ["Flooring", "hammer"], ["Small jobs", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("Boxmoor Decorating"),
     {"q": "Do you give free quotes?", "a": "Yes. We offer all customers free, no obligation quotes and consultations."},
     {"q": "Which areas do you cover?", "a": "We’re based in Hemel Hempstead and cover Herts, Beds, Bucks and North London."}],
    "Planning a room makeover?",
    ["Hemel Hempstead", "Hertfordshire", "Bedfordshire", "Buckinghamshire", "North London"],
    ["1688372198189-de6a51777a81", "1561297331-a9c00b9c2c44"],
    free_quotes=True,
))

# 3. MPF Landscapes Ltd (no website) --------------------------------------------
made.append(lead(
    "mpf-landscapes", "#3FA34D",
    {"name": "MPF Landscapes", "short": "MPF", "sub": "Landscapes", "logo_icon": "leaf",
     "trade": "Landscapers", "town": "Bushey", "county": "Hertfordshire",
     "phone": "07931 877875", "phone_tel": "07931877875", "email": "mpflandscapes@outlook.com",
     "hours": "Mon–Sat 7:30am–4:30pm", "company_line": "MPF Landscapes Ltd · Company no. 16198422"},
    {"title": "MPF Landscapes – Landscaper in Bushey, Hertfordshire",
     "description": "Patios, turfing, garden clearance, driveways and landscaping in Bushey and across Hertfordshire."},
    {"eyebrow": "Bushey · Hertfordshire", "h1": "Gardens you’ll", "h1_accent": "want to be in.",
     "lead": "Patios, turf, garden clearance, driveways and landscaping in Bushey and across Hertfordshire, from Scott and his team.",
     "img": ("1711098256574-7b497260cdc9", "Landscaped garden patio with furniture and plants")},
    ["Which? Trusted Trader", "Herts Trading Standards Approved", "Hertfordshire based", "Patios & turfing"],
    ["Patios", "Turfing", "Garden clearance", "Driveways", "Resin bound stone", "Decking", "Drainage", "Garden walls"],
    {"eyebrow": "What we do", "heading": ["From overgrown", "to outdoor room."],
     "intro": "Hard landscaping, turfing and garden work, from a single patio to a full garden makeover.",
     "items": [
         svc("Patios", "New patios and natural stone surfacing.", "sparkle", "1719324923613-ff0884b031ed", "Paved garden patio with table and chairs"),
         svc("Turfing & lawns", "New turf laid, lawns mowed and treated.", "leaf", "1642541744624-7a2a89545a32", "Long green lawn with hedges"),
         svc("Garden clearance", "Overgrown gardens cleared and made ready to use.", "wrench"),
         svc("Driveways & resin", "Driveway installation and resin bound stone surfacing.", "car"),
         svc("Decking & garden structures", "Decking, sheds, shed bases and garden structures.", "house"),
         svc("Drainage & walls", "Garden drainage, garden walling and drystone walling.", "drop"),
     ]},
    [rev("Scott and his team did a fantastic job of our garden patio. His team arrived promptly and worked in a very clean and very professional way. They took away all the soil they had dug out in our garden and laid a good base for the patio…", "Hertfordshire"),
     rev("Scott and his team were brilliant from quote to finish. Scott was able to work within the budget I had and produce high quality work. They were reliable, clean and always friendly with neighbours etc…", "Hertfordshire"),
     rev("Scott and his team did a fantastic job in our garden. Scott came over really quickly and gave us a quote. His team were timely, clean and very professional…", "Greater London")],
    [["Patio", "sparkle"], ["Turf", "leaf"], ["Clearance", "wrench"], ["Driveway", "car"], ["Decking", "house"], ["Something else", "other"]],
    [WHICH_FAQ("MPF Landscapes"),
     {"q": "Which areas do you cover?", "a": "We’re based in Bushey and work across Hertfordshire."},
     QUOTE_FAQ("07931 877875")],
    "Ready to sort out the garden?",
    ["Bushey", "Hertfordshire"],
    ["1719324923613-ff0884b031ed", "1642541744624-7a2a89545a32"],
))

# 4. G J Taylor & Company Ltd (no website) --------------------------------------
made.append(lead(
    "taylor-and-company", "#C8553D",
    {"name": "Taylor & Company", "short": "Taylor & Co", "sub": "Building & Decorating", "logo_icon": "hammer",
     "trade": "Builders", "town": "Toddington", "county": "Bedfordshire",
     "phone": "07831 866857", "phone_tel": "07831866857", "email": "gary.taylor006@hotmail.com",
     "hours": "Mon–Sat 7:30am–6:30pm", "company_line": "G J Taylor & Company Limited · Company no. 10081026"},
    {"title": "Taylor & Company – Builders & Decorators in Toddington, Bedfordshire",
     "description": "Family run building and decorating company in Toddington. Carpentry, plastering, painting and decorating, kitchens and maintenance."},
    {"eyebrow": "Toddington · Bedfordshire", "h1": "Building work,", "h1_accent": "finished properly.",
     "lead": "A family run business carrying out all types of domestic and commercial building, from carpentry and plastering to painting, decorating and kitchen fitting.",
     "img": ("1688372199140-cade7ae820fe", "Decorator painting a wall with a roller")},
    ["Which? Trusted Trader", "Family run", "Domestic & commercial", "Bedfordshire based"],
    ["Carpentry", "Plastering", "Painting & decorating", "Tiling", "Kitchen fitting", "Plumbing", "Electrics", "Maintenance"],
    {"eyebrow": "What we do", "heading": ["Personal service,", "high quality work."],
     "intro": "We take pride in our work and only use other trades who will keep to our standards.",
     "items": [
         svc("Painting & decorating", "Interior and exterior decorating, done with care.", "brush"),
         svc("Carpentry", "Carpentry for domestic and commercial customers.", "hammer", "1659930087003-2d64e33181f7", "Carpenter marking a wooden board"),
         svc("Plastering", "Plastering and making good, ready for decorating.", "board"),
         svc("Kitchen fitting", "Kitchens fitted and finished, including tiling.", "sparkle", "1628745277862-bc0b2d68c50c", "Modern kitchen with white worktop"),
         svc("Plumbing & electrics", "Plumbing and electrical work as part of your project.", "bolt"),
         svc("Maintenance & partitioning", "Property maintenance, partitioning and shop fitting.", "wrench"),
     ]},
    [rev("Gary & his team did another excellent job for us decorating the exterior of our house and doing additional jobs inside… I have no hesitation in recommending this outstanding company for their workmanship and professionalism, as well as their congeniality and adaptability.", "Greater London"),
     rev("Thank you Gary & your team for the hard work you put into decorating our new home. As we wanted our whole house decorated it was hard finding someone to trust but you didn't let us down…", "Hertfordshire", who="Cathy in Hertfordshire"),
     rev("We hired Gary to undertake a full external & internal decoration of the house including remedial building work. He and his team not only did a first class job but also went out of their way to make our lives tolerable during the 6 weeks they were working…", "Greater London")],
    [["Decorating", "brush"], ["Carpentry", "hammer"], ["Plastering", "board"], ["Kitchen", "sparkle"], ["Maintenance", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("Taylor & Company"),
     {"q": "Do you take on commercial work?", "a": "Yes. We carry out all types of domestic and commercial building work."},
     QUOTE_FAQ("07831 866857")],
    "Got a building or decorating job?",
    ["Toddington", "Bedfordshire"],
    ["1659930087003-2d64e33181f7", "1628745277862-bc0b2d68c50c"],
))

# 5. Manor Interiors (Oxfordshire) Ltd ------------------------------------------
made.append(lead(
    "manor-interiors", "#2E86AB",
    {"name": "Manor Interiors", "short": "Manor", "sub": "Interiors", "logo_icon": "drop",
     "trade": "Plumbing & heating", "town": "Cholsey", "county": "Oxfordshire",
     "phone": "07870 257119", "phone_tel": "07870257119", "email": "manor@manor-interiors.com",
     "hours": "Mon–Fri 7:30am–5pm", "company_line": "Manor Interiors (Oxfordshire) Limited · Company no. 11841727"},
    {"title": "Manor Interiors – Plumbing, Heating & Home Improvements in Oxfordshire",
     "description": "Family-run plumbing, heating and home improvement business in Cholsey, Oxfordshire, with over 30 years’ experience."},
    {"eyebrow": "Cholsey · Wallingford · Oxfordshire", "h1": "Plumbing, heating", "h1_accent": "and so much more.",
     "lead": "A family-run plumbing, heating and home improvement business in Oxfordshire, with over 30 years’ experience and every job completed to the highest standards.",
     "img": ("1771681278369-e2a5480b8c29", "Modern bathroom with marble details")},
    ["Which? Trusted Trader", "Family run", "30+ years’ experience", "Oxfordshire based"],
    ["Boilers", "Heating", "Bathrooms", "Kitchens", "Water softeners", "Underfloor heating", "Extensions", "Renewables"],
    {"eyebrow": "What we do", "heading": ["Quality and care", "in every job."],
     "intro": "From a new boiler to a full renovation, one family-run team for plumbing, heating, kitchens, bathrooms and building work.",
     "items": [
         svc("Plumbing & heating", "Boilers installed, repaired and serviced, radiators, underfloor heating and power flushing.", "flame", "1618840626133-54463084a141", "Close-up of metal pipework"),
         svc("Bathrooms & wet rooms", "Bathroom design, installation and tiling, wet rooms and accessible showers.", "sparkle"),
         svc("Kitchens", "Kitchen design, fitting, worktops and tiling.", "board", "1628745277862-bc0b2d68c50c", "Modern kitchen with white worktop"),
         svc("Water softeners & hot water", "Water softeners and unvented cylinders installed and maintained.", "drop"),
         svc("Building work", "Extensions, garage and loft conversions, porches and plastering.", "house"),
         svc("Carpentry & decorating", "Joinery, garden rooms and interior decorating.", "hammer"),
     ]},
    [rev("I've used Manor Interiors for over 10 years and highly recommend them to everyone! They initially installed an oil heating system into my old cottage… They have guided me through all the jargon and simply made the process of renovating stress free… Their quality of work is exceptional.", "Oxfordshire"),
     rev("They removed the wet unit, went and got me a great replacement and installed it for me. All the same day! It was amazing… Very professional and super friendly.", "Oxfordshire")],
    [["Boiler", "flame"], ["Bathroom", "sparkle"], ["Kitchen", "board"], ["Water softener", "drop"], ["Building work", "house"], ["Something else", "other"]],
    [WHICH_FAQ("Manor Interiors"),
     {"q": "Do you do more than plumbing?", "a": "Yes. As well as plumbing and heating, we design and fit kitchens and bathrooms and carry out building work such as extensions and conversions."},
     QUOTE_FAQ("07870 257119")],
    "Planning work on your home?",
    ["Cholsey", "Wallingford", "Oxfordshire"],
    ["1618840626133-54463084a141", "1628745277862-bc0b2d68c50c"],
))

# 6. Avant-Garde Roofing Solutions Ltd ------------------------------------------
made.append(lead(
    "avant-garde-roofing", "#F28C28",
    {"name": "Avant-Garde Roofing Solutions", "short": "Avant-Garde", "sub": "Roofing Solutions", "logo_icon": "roof",
     "trade": "Flat roofing", "town": "Hartwell", "county": "Northamptonshire",
     "phone": "01908 511406", "phone_tel": "01908511406", "email": "paul@avant-garde-roofing.co.uk",
     "hours": "Mon–Fri 8am–7pm", "company_line": "Avant-Garde Roofing Solutions Limited · Company no. 07095012"},
    {"title": "Avant-Garde Roofing Solutions – Flat Roofing in Northamptonshire",
     "description": "Specialist approved installers of flat roof systems for homes and businesses. Fibreglass (GRP), rubber (EPDM), roof repairs and insulation."},
    {"eyebrow": "Hartwell · Northamptonshire", "h1": "Flat roofs,", "h1_accent": "done right.",
     "lead": "Specialist approved installers of proven flat roof systems for homes and businesses: a long term, cost effective answer to flat roofs that keep failing.",
     "img": ("1726589004565-bedfba94d3a2", "Roofer working on a roof")},
    ["Which? Trusted Trader", "Approved installers", "Domestic & commercial", "Flat roof specialists"],
    ["Fibreglass (GRP)", "Rubber (EPDM)", "Felt roofing", "Roof repairs", "Conservatory roofs", "Guttering", "Fascias & soffits", "Insulation"],
    {"eyebrow": "What we do", "heading": ["No more weathering,", "no failing joints."],
     "intro": "Our flat roof systems get rid of the problems that come with traditional flat roof materials.",
     "items": [
         svc("Flat roof replacement", "Old and failing flat roofs stripped out and replaced with a proven system.", "roof"),
         svc("Fibreglass (GRP) roofs", "GRP fibreglass flat roofing.", "sparkle"),
         svc("Rubber roofing (EPDM)", "Flexible rubber roofing membranes.", "shield"),
         svc("Roof repairs", "Leaks found and fixed.", "wrench"),
         svc("Conservatory roof conversions", "Conservatory roofs converted.", "house"),
         svc("Guttering, fascias & soffits", "Roofline work so rainwater drains away properly.", "drop"),
     ]},
    [rev("Excellent service. These guys are incredibly skilled and very professional. Paul responded to our request quite quickly and provided a quote soon after. The team showed up on time and were incredibly efficient… We are so pleased with our new roof. It looks fantastic and most important of all it is watertight. Thank you.", "Cambridgeshire"),
     rev("Clint and Paul are professional & reliable. They and their team are hard working. Paul did a thorough survey of the roof and provided a detailed quotation detailing the works and referencing the correct building regulations… The persistent leak has been fixed and the ceiling is as dry as a bone…", "Hertfordshire"),
     rev("Paul came out on his day off to repair a leak that had nothing to do with any work they had done, and he repaired it, even though it wasn't his responsibility, now that's what I call professionalism, and brilliant customer service.", "Hayes")],
    [["Flat roof", "roof"], ["Fibreglass", "sparkle"], ["Rubber roof", "shield"], ["Repair", "wrench"], ["Conservatory", "house"], ["Something else", "other"]],
    [WHICH_FAQ("Avant-Garde Roofing Solutions"),
     {"q": "Do you work on commercial roofs?", "a": "Yes. Our flat roof systems are designed for both commercial and domestic roofs."},
     QUOTE_FAQ("01908 511406")],
    "Flat roof leaking or failing?",
    ["Hartwell", "Northampton", "Northamptonshire"],
    [],
))

# 7. Ayla Tree Care Ltd -----------------------------------------------------------
made.append(lead(
    "ayla-tree-care", "#7BB661",
    {"name": "Ayla Tree Care", "short": "Ayla", "sub": "Tree Care", "logo_icon": "leaf",
     "trade": "Tree surgeons", "town": "Hemel Hempstead", "county": "Hertfordshire",
     "phone": "07821 589190", "phone_tel": "07821589190", "email": "aylatreecare@gmail.com",
     "hours": "", "company_line": "Ayla Tree Care Ltd · Company no. 10050742"},
    {"title": "Ayla Tree Care – Tree Surgeon in Hemel Hempstead, Hertfordshire",
     "description": "NPTC certified tree surgeons in Hertfordshire. Tree reductions, removals, stump grinding and hedge trimming, with a 24-hour emergency service."},
    {"eyebrow": "Hemel Hempstead · Hertfordshire", "h1": "Professional", "h1_accent": "tree care.",
     "lead": "A friendly and professional tree surgery company based in Hertfordshire, handling commercial and domestic tree work from crown reductions to planting.",
     "img": ("1754322449185-31f56117ed87", "Tree surgeon cutting a branch")},
    ["Which? Trusted Trader", "NPTC certified", "£5m public liability", "24-hour emergency service"],
    ["Tree reductions", "Tree removal", "Thinning", "Pruning", "Stump grinding", "Hedge trimming", "Tree planting"],
    {"eyebrow": "What we do", "heading": ["Experienced,", "qualified, friendly."],
     "intro": "Dismantling, shaping, thinning, planting and pruning, along with stump grinding and removal.",
     "items": [
         svc("Reductions & shaping", "Crown reductions, shaping, thinning and pruning.", "leaf", "1709560723503-538158e48db8", "Tree surgeon working on a tree"),
         svc("Tree removal", "Trees dismantled and removed.", "hammer", "1631300313270-227604e71ea5", "Tree surgeon sitting on a branch"),
         svc("Stump grinding", "Stumps ground out and removed.", "wrench"),
         svc("Hedge trimming", "Hedges cut back and shaped.", "scissors"),
         svc("Tree planting", "New trees planted.", "sparkle"),
         svc("Emergency tree work", "A 24-hour emergency service if needed.", "clock"),
     ]},
    [rev("Marc and his company came to the rescue at short notice, after I had been let down by my previous gardener. They did an excellent job in my garden, which needed lots of hedge cutting and strimming. They worked quickly, left the site tidy, and delivered a friendly and professional service. Highly recommended.", "Hertfordshire"),
     rev("After finding Ayla on Which? Trusted Traders list I was very happy with the work they did on our weeping pear tree, hazelnut tree and on our laurel hedge… Throughout the job they were polite and hard working and we highly recommend their work.", "Buckinghamshire"),
     rev("I can honestly say the work that Ayla has completed for us is top notch. The guys turned up on time every day, were polite, hard working and nothing was too much trouble for them… I can finally see the sky in my garden, we are thrilled with the results.", "Greater London")],
    [["Reduction", "leaf"], ["Removal", "hammer"], ["Stump", "wrench"], ["Hedge", "scissors"], ["Emergency", "clock"], ["Something else", "other"]],
    [WHICH_FAQ("Ayla Tree Care"),
     {"q": "Are you qualified and insured?", "a": "Yes. We’re NPTC certified, qualified to BS3998 and carry £5 million public liability insurance."},
     {"q": "Do you give free estimates?", "a": "Yes. Free estimates and friendly advice. Call us or use the form on this page."}],
    "Got a tree that needs attention?",
    ["Hemel Hempstead", "Hertfordshire"],
    ["1709560723503-538158e48db8", "1631300313270-227604e71ea5"],
    free_quotes=True,
))

# 8. SH Carpentry and Construction Ltd -------------------------------------------
made.append(lead(
    "sh-carpentry-construction", "#E0A458",
    {"name": "SH Carpentry & Construction", "short": "SH", "sub": "Carpentry & Construction", "logo_icon": "hammer",
     "trade": "Builders & carpenters", "town": "Wantage", "county": "Oxfordshire",
     "phone": "07919 486021", "phone_tel": "07919486021", "email": "shane@sh-construction.co.uk",
     "hours": "", "company_line": "SH Carpentry and Construction Limited · Company no. 09280274"},
    {"title": "SH Carpentry & Construction – Builders & Carpenters in Oxfordshire",
     "description": "Carpentry, joinery and general construction across Oxfordshire. Extensions, conversions and renovations, with over fifteen years’ experience."},
    {"eyebrow": "Lyford · Wantage · Oxfordshire", "h1": "Built with care,", "h1_accent": "run properly.",
     "lead": "A professional and reliable carpentry, joinery and general construction company working across Oxfordshire, with over fifteen years’ industry experience behind the business.",
     "img": ("1593012671976-1422185230fb", "Building work on a house extension")},
    ["Which? Trusted Trader", "15+ years’ experience", "Residential & commercial", "Oxfordshire based"],
    ["Extensions", "Renovations", "Garage conversions", "Carpentry", "Joinery", "Plastering", "Conservatories", "Damp proofing"],
    {"eyebrow": "What we do", "heading": ["Organised, clear,", "attention to detail."],
     "intro": "Residential and commercial construction, with a strong focus on organisation, communication and attention to detail.",
     "items": [
         svc("Extensions", "Extensions planned and built, working alongside your architect and designer.", "house", "1593786267440-550458cc882a", "Brick extension being built"),
         svc("Renovations", "Renovations and design and build projects.", "sparkle"),
         svc("Carpentry & joinery", "Carpentry and joinery for homes and commercial projects.", "hammer", "1659930087003-2d64e33181f7", "Carpenter marking a wooden board"),
         svc("Garage conversions", "Garages turned into useful living space.", "board"),
         svc("Plastering", "Plastering and making good.", "brush"),
         svc("Damp & condensation", "Damp proofing, timber preservation and condensation control.", "drop"),
     ]},
    [rev("Shane and his team at SH Carpentry are quality builders. Very professional, very polite and very efficient. Nothing was too much trouble and they were very good at listening to what was wanted and needed. Shane was brilliant in liaising with building control which made the whole process easier…", "Oxfordshire"),
     rev("Shane, Charlotte, and the team were excellent from start to finish. We had a reconfiguration of the downstairs, and the results are fantastic. They made the whole process completely stress-free…", "Oxfordshire"),
     rev("Shane and team did a great job removing a chimney, building up outside wall, fixing and finishing the roof, soffits and facia. They were careful with the awkwardly placed solar panels and worked quickly and efficiently…", "Oxfordshire")],
    [["Extension", "house"], ["Renovation", "sparkle"], ["Carpentry", "hammer"], ["Conversion", "board"], ["Damp", "drop"], ["Something else", "other"]],
    [WHICH_FAQ("SH Carpentry & Construction"),
     {"q": "Do you work with architects?", "a": "Yes. We work with architects, designers, consultants and other construction professionals so your project is well-coordinated and efficiently managed."},
     QUOTE_FAQ("07919 486021")],
    "Planning a building project?",
    ["Wantage", "Lyford", "Oxfordshire"],
    ["1593786267440-550458cc882a", "1659930087003-2d64e33181f7"],
))

# 9. MPH Building Services Ltd ----------------------------------------------------
made.append(lead(
    "mph-building-services", "#8E6CEF",
    {"name": "MPH Building Services", "short": "MPH", "sub": "Building Services", "logo_icon": "board",
     "trade": "Kitchen fitters", "town": "Moggerhanger", "county": "Bedfordshire",
     "phone": "07795 843549", "phone_tel": "07795843549", "email": "matthewph55@gmail.com",
     "hours": "Mon–Sun 7am–7pm", "company_line": "MPH Building Services Limited · Company no. 10043769"},
    {"title": "MPH Building Services – Kitchen Fitter in Bedfordshire",
     "description": "Kitchen fitting, bathrooms, carpentry, tiling and full refurbishments in Bedfordshire, from design to installation."},
    {"eyebrow": "Moggerhanger · Bedford · Bedfordshire", "h1": "Kitchens & bathrooms,", "h1_accent": "start to finish.",
     "lead": "Reliable, friendly, quality refurbishments from design to installation. One company looks after you from start to finish, so there’s no managing different contractors.",
     "img": ("1722605090433-41d1183a792d", "Kitchen with white cabinets and marble worktops")},
    ["Which? Trusted Trader", "15+ years’ experience", "NVQ qualified", "Fully insured"],
    ["Kitchens", "Bathrooms", "Carpentry", "Tiling", "Plastering", "Flooring", "Decorating", "Full refurbishments"],
    {"eyebrow": "What we do", "heading": ["One company,", "no hassle."],
     "intro": "Full refurbishments including kitchen fitting, carpentry, tiling, plastering, decorating, flooring, bathrooms and bedrooms.",
     "items": [
         svc("Kitchen fitting", "Kitchens designed and fitted, from first plan to final finish.", "board"),
         svc("Bathrooms & wet rooms", "Bathroom design and refurbishment, wet rooms and accessible showers.", "drop", "1631889993959-41b4e9c6e3c5", "Bathroom with bath and basin"),
         svc("Carpentry", "All carpentry, including bedrooms.", "hammer", "1659930087003-2d64e33181f7", "Carpenter marking a wooden board"),
         svc("Tiling", "Bathroom, kitchen and floor tiling.", "sparkle"),
         svc("Plastering", "Plastering, skimming, coving, screeding and dry lining.", "brush"),
         svc("Full refurbishments", "Whole-room refurbishments, with one company from start to finish.", "house"),
     ]},
    [rev("Matt from MPH was great from the start, giving advice on the design of the kitchen and recommending affordable but high quality materials etc. He was very aware that we had to live in our home during the renovation… The quality and standard of Matts work is second to none and we couldn’t be happier with the result.", "Hertfordshire"),
     rev("MPH building services fitted our new kitchen and utility room using Howden’s products. We are very happy with Matt’s work and the end result. Matt listened carefully to our requirements and wishes and fitted our kitchen to a high-quality finish with attention to detail and excellent workmanship…", "Cambridgeshire"),
     rev("Matt had already fitted a new kitchen for me a couple of years ago, so I knew that he was multi-skilled and competent as well as being personable and considerate. He helped me with the design, then subsequently helped me to find the fittings and tiles I preferred within my budget…", "Central Bedfordshire")],
    [["Kitchen", "board"], ["Bathroom", "drop"], ["Carpentry", "hammer"], ["Tiling", "sparkle"], ["Refurbishment", "house"], ["Something else", "other"]],
    [WHICH_FAQ("MPH Building Services"),
     {"q": "Do you give free quotes?", "a": "Yes. Quotations are free and prompt."},
     QUOTE_FAQ("07795 843549")],
    "Planning a new kitchen or bathroom?",
    ["Moggerhanger", "Bedford", "Bedfordshire"],
    ["1631889993959-41b4e9c6e3c5", "1659930087003-2d64e33181f7"],
    free_quotes=True,
))

# 10. Alderson Building Company Ltd -----------------------------------------------
made.append(lead(
    "alderson-building", "#D64545",
    {"name": "Alderson Building Company", "short": "Alderson", "sub": "Building Company", "logo_icon": "house",
     "trade": "Builders", "town": "Hemel Hempstead", "county": "Hertfordshire",
     "phone": "07958 272351", "phone_tel": "07958272351", "email": "rayaldersonx@gmail.com",
     "hours": "Mon–Fri 8am–5pm", "company_line": "Alderson Building Company Limited · Company no. 06403779"},
    {"title": "Alderson Building Company – Builders in Hemel Hempstead",
     "description": "Long established, family run builders in Hemel Hempstead. House extensions, loft conversions, refurbishments and landscaping across Hertfordshire."},
    {"eyebrow": "Hemel Hempstead · Hertfordshire", "h1": "Extensions and", "h1_accent": "home renovations.",
     "lead": "A long established, family run building business in Hertfordshire, covering house extensions, loft conversions, home refurbishments and landscaping projects.",
     "img": ("1593786267440-550458cc882a", "Brick extension being built")},
    ["Which? Trusted Trader", "Herts Trading Standards Approved", "Family run", "Long established"],
    ["Extensions", "Loft conversions", "Garage conversions", "Refurbishments", "Kitchens", "Bathrooms", "Patios", "Driveways"],
    {"eyebrow": "What we do", "heading": ["All construction,", "one family team."],
     "intro": "Covering all construction projects, from house extensions and loft conversions to home refurbishments and landscaping.",
     "items": [
         svc("House extensions", "House extensions, planned and built.", "house", "1593012672015-4fabc32c67aa", "Extension under construction"),
         svc("Loft conversions", "Lofts turned into usable rooms.", "roof"),
         svc("Garage conversions", "Garages converted into extra living space.", "hammer"),
         svc("Kitchens & bathrooms", "Kitchen and bathroom refurbishments.", "sparkle", "1722605090433-41d1183a792d", "Kitchen with white cabinets"),
         svc("Refurbishments", "Home refurbishments and plastering.", "brush"),
         svc("Patios, driveways & fencing", "Landscaping projects, patios, driveways and fencing.", "leaf"),
     ]},
    [rev("Roy, Liam, and Ray were fantastic from start to finish. We were extremely impressed with their workmanship and professionalism throughout the entire project. The final cost came in exactly as expected, which we greatly appreciated…", "Hertfordshire"),
     rev("I chose Alderson Building Company as they are a Which Trusted Trader, and they lived up to expectations. Ray, Roy & Liam plus the rest of the team completed our cloakroom and first floor extension to a high standard and within the original estimate and time-frame…", "Hertfordshire"),
     rev("This company has been exceptional they have excellent quality of work. Our quote was accurate. They definitely took pride in their work and worked hard. Very easy to get in contact with and always came back to me…", "Hertfordshire")],
    [["Extension", "house"], ["Loft", "roof"], ["Conversion", "hammer"], ["Kitchen or bathroom", "sparkle"], ["Landscaping", "leaf"], ["Something else", "other"]],
    [WHICH_FAQ("Alderson Building Company"),
     {"q": "Do you give free estimates?", "a": "Yes. Speak to the team to discuss your planned work and arrange a free pricing estimate."},
     QUOTE_FAQ("07958 272351")],
    "Planning an extension or renovation?",
    ["Hemel Hempstead", "Hertfordshire"],
    ["1593012672015-4fabc32c67aa", "1722605090433-41d1183a792d"],
    free_quotes=True,
))

print("\n".join(made))
