"""Write engine/data/<slug>.json for the first batch of preview leads."""
import json, pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
U = "https://images.unsplash.com/photo-{}?ixlib=rb-4.1.0&auto=format&fit=crop&w={}&q=80"
PH = {  # photo id -> (photographer, username)
    "1593786267440-550458cc882a": ("Brett Jordan", "brett_jordan"),
    "1593623671658-6b842c7f9697": ("Brett Jordan", "brett_jordan"),
    "1614418583513-8e96d9160333": ("Peter Muscutt", "peterm4988372"),
    "1563993356056-b23a9cd265ad": ("Verstappen Photography", "verstappen_photography"),
    "1732660513320-a6b489f3fece": ("Marc Zeman", "der_zeman"),
    "1650551182991-b07558247564": ("Immo Wegmann", "tinkerman"),
    "1618840626133-54463084a141": ("Peter Herrmann", "tama66"),
    "1584622650111-993a426fbf0a": ("Lotus Design N Print", "lotusdnp"),
    "1638799869566-b17fa794c4de": ("Lotus Design N Print", "lotusdnp"),
    "1696987007764-7f8b85dd3033": ("Clay Banks", "claybanks"),
    "1768486143865-342d8cc12c90": ("Clay Banks", "claybanks"),
    "1754322449185-31f56117ed87": ("Zack Masters", "masters25"),
    "1754322449005-bdc38c631682": ("Zack Masters", "masters25"),
    "1709560723503-538158e48db8": ("Scott Precious", "scottsalchemy"),
    "1659930087003-2d64e33181f7": ("Craft Kitties", "craftkitties"),
    "1547609434-b732edfee020": ("Will Suddreth", "willsudds"),
    "1679797850019-3d0d8659a695": ("Samuel Cruz", "samuelcruz"),
    "1789841417999-67a24a247c90": ("Barney Goodman", "bgoodpic"),
    "1688372198189-de6a51777a81": ("Ali Mkumbwa", "mkumbwajr"),
    "1790671023265-0e2e1ecfdb78": ("Wenzy Wong", "wenzywong"),
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


def rev(text, where):
    return {"text": text, "who": f"Customer in {where}", "label": "Which? review"}


STEPS = [
    {"title": "Get in touch", "text": "Call, or send the quote form with a few details. Photos help."},
    {"title": "We take a look", "text": "We talk it through, look at the job and give you a clear quote."},
    {"title": "Job done properly", "text": "The work is done with care and the site left clean and tidy."},
]


def lead(slug, accent, biz, seo, hero, pills, marquee, services, reviews, jobs, faqs, cta, areas, photos, rev_intro):
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
        "reviews": {"heading": ["What customers", "say about us."], "intro": rev_intro, "items": reviews},
        "quote": {"intro": "Three quick steps and we’ll get back to you.", "jobs": jobs},
        "faqs": faqs,
        "cta": {"heading": cta},
        "areas": areas,
        "credits": credits([hero_img] + photos),
    }
    if slug in ("inspired-restorations", "steves-handyman"):
        d["free_quotes"] = True
    (DATA / f"{slug}.json").write_text(json.dumps(d, indent=2, ensure_ascii=False))
    return slug


WHICH_FAQ = lambda name: {"q": "Can I read more reviews?", "a": f"Yes. {name} is a Which? Trusted Trader, and you can read all our customer reviews on our Which? page."}
QUOTE_FAQ = lambda phone: {"q": "How do I get a quote?", "a": f"Use the quote form on this page or call {phone}. A few photos of the job help us give you an accurate price."}

made = []

# 1. Hammond Construction ------------------------------------------------------
made.append(lead(
    "hammond-construction", "#F2B33D",
    {"name": "Hammond Construction", "short": "Hammond", "sub": "Construction", "logo_icon": "house",
     "trade": "Builders", "town": "High Wycombe", "county": "Buckinghamshire",
     "phone": "01494 483924", "phone_tel": "01494483924", "email": "office@hammond-construction.co.uk",
     "hours": "Mon–Fri 8am–6pm", "company_line": "Hammond Construction (Oxford) Limited · Company no. 06426524"},
    {"title": "Hammond Construction – Builders in Buckinghamshire & Oxfordshire",
     "description": "Family owned building, refurbishment and electrical services. Extensions, conversions, kitchens and bathrooms."},
    {"eyebrow": "Building · Refurbishment · Electrical", "h1": "Homes built", "h1_accent": "with care.",
     "lead": "Hammond Construction is a family owned building, refurbishment and electrical services company. Extensions, conversions, kitchens and bathrooms, with all the trades under one roof.",
     "img": ("1593786267440-550458cc882a", "House extension being built in brick")},
    ["Which? Trusted Trader", "FMB members", "NICEIC approved", "FENSA registered"],
    ["Extensions", "Garage conversions", "Loft conversions", "Kitchens", "Bathrooms", "Electrics", "Refurbishments"],
    {"eyebrow": "What we do", "heading": ["Every trade,", "one team."],
     "intro": "From a new extension to a full refurbishment, we plan the job with you and see it through to the finish.",
     "items": [
         svc("Extensions", "Single and two storey extensions, planned and built from the ground up.", "house", "1593623671658-6b842c7f9697", "Extension under construction with steel beams", "Popular"),
         svc("Kitchens", "Kitchen design and installation, including worktops and tiling.", "sparkle", "1768486143865-342d8cc12c90", "Modern kitchen with pendant lights"),
         svc("Bathrooms & wet rooms", "Bathroom refits, en-suites, wet rooms and accessible showers.", "drop", "1584622650111-993a426fbf0a", "Modern bathroom with walk-in shower"),
         svc("Conversions", "Garage and loft conversions that add space without moving.", "hammer"),
         svc("Electrical work", "Rewires, fuse boards, testing and EV charging points.", "bolt"),
         svc("Heating", "Boiler installs, servicing, radiators and underfloor heating.", "flame"),
     ]},
    [rev("Hammonds carried out a significant renovation at the rear of our house to open-plan the lounge, kitchen, and dining area.", "Buckinghamshire"),
     rev("Wouldn’t hesitate to recommend Hammonds. We first used them for a small job (garage conversion) a few years ago and this time had a lot of work done including a rear extension and windows replaced.", "Buckinghamshire"),
     rev("We have had a 2 storey side extension and other extensive improvements on the old part of our house and garden/driveway. James and his team have been exceptional from start to finish.", "Oxfordshire")],
    [["Extension", "house"], ["Conversion", "hammer"], ["Kitchen", "sparkle"], ["Bathroom", "drop"], ["Electrics", "bolt"], ["Something else", "other"]],
    [WHICH_FAQ("Hammond Construction"),
     {"q": "Do you do the electrics too?", "a": "Yes. We’re NICEIC approved electrical contractors, so we can take care of the electrics as part of your project."},
     QUOTE_FAQ("01494 483924")],
    "Planning an extension or renovation?",
    ["High Wycombe", "Buckinghamshire", "Oxfordshire"],
    ["1593623671658-6b842c7f9697", "1768486143865-342d8cc12c90", "1584622650111-993a426fbf0a"],
    "Real reviews from customers on Which? Trusted Traders.",
))

# 2. Mike Carroll Ltd -----------------------------------------------------------
made.append(lead(
    "mike-carroll-roofing", "#E8613C",
    {"name": "Mike Carroll Roofing", "short": "Mike Carroll", "sub": "Roofing & Building", "logo_icon": "roof",
     "trade": "Roofers", "town": "Stoke Mandeville", "county": "Buckinghamshire",
     "phone": "01296 612699", "phone_tel": "01296612699", "email": "mikecarrollroofing@gmail.com",
     "hours": "", "company_line": "Mike Carroll Limited · Company no. 08779906"},
    {"title": "Mike Carroll Roofing – Roofers in Buckinghamshire",
     "description": "Family run roofing business in Stoke Mandeville. Roofs, fascias, soffits, guttering and flat roofs across Buckinghamshire."},
    {"eyebrow": "Aylesbury · High Wycombe · Buckinghamshire", "h1": "Roofs built", "h1_accent": "to last.",
     "lead": "A family run roofing business in Stoke Mandeville, looking after roofs, fascias, soffits and guttering across Buckinghamshire for over thirty years.",
     "img": ("1614418583513-8e96d9160333", "Close-up of clay roof tiles")},
    ["Which? Trusted Trader", "Family run", "30+ years’ experience", "Buckinghamshire based"],
    ["Roof repairs", "New roofs", "Flat roofs", "Fascias", "Soffits", "Guttering", "Cladding"],
    {"eyebrow": "What we do", "heading": ["From one tile", "to a whole roof."],
     "intro": "Repairs, replacements and roofline work, done by a family team that has been at it for over thirty years.",
     "items": [
         svc("Roof repairs & replacement", "Slipped or cracked tiles fixed, or a full new roof when it’s time.", "roof", "1563993356056-b23a9cd265ad", "Tiled roof against a blue sky", "Most asked for"),
         svc("Fascias, soffits & guttering", "Replacement roofline that looks smart and keeps water away.", "drop"),
         svc("Flat & rubber roofs", "EPDM rubber flat roofs for extensions, porches and garages.", "board"),
         svc("Lead work & skylights", "Lead flashing, Velux windows and roof lights.", "sparkle"),
         svc("Cladding", "External cladding replaced and repaired.", "house", "1593786267440-550458cc882a", "House exterior during building work"),
         svc("Conservatory roofs", "Conservatory roof repairs and conversions.", "shield"),
     ]},
    [rev("Recently had a house porch rebuilt and the flat roof on a small extension replaced. Mike provided a detailed quote with options depending on what they found as the work progressed.", "Buckinghamshire"),
     rev("Mike's team replaced my facias, soffits and guttering, they arrived on time and did a great job, it all looks brilliant, they cleaned up before they left…", "Buckinghamshire"),
     rev("We have two large roofs, old buildings with old tiles. Gales and tree bough impact had left us with cracked and slipped tiles. Mike's team did a super job.", "Buckinghamshire")],
    [["Roof repair", "roof"], ["New roof", "house"], ["Flat roof", "board"], ["Guttering", "drop"], ["Fascias & soffits", "shield"], ["Something else", "other"]],
    [WHICH_FAQ("Mike Carroll Roofing"),
     {"q": "Which areas do you cover?", "a": "We work across Buckinghamshire, including Aylesbury, Amersham, Beaconsfield, Buckingham, High Wycombe, Hemel Hempstead, Leighton Buzzard and Milton Keynes."},
     QUOTE_FAQ("01296 612699")],
    "Got a roof that needs looking at?",
    ["Aylesbury", "Amersham", "Beaconsfield", "Buckingham", "High Wycombe", "Hemel Hempstead", "Leighton Buzzard", "Milton Keynes"],
    ["1563993356056-b23a9cd265ad", "1593786267440-550458cc882a"],
    "Real reviews from customers on Which? Trusted Traders.",
))

# 3. R&S Plumbing & Gas Services Ltd -------------------------------------------
made.append(lead(
    "rs-plumbing-gas", "#3FA9F5",
    {"name": "R&S Plumbing & Gas Services", "short": "R&S", "sub": "Plumbing & Gas", "logo_icon": "drop",
     "trade": "Plumbers", "town": "Cheltenham", "county": "Gloucestershire",
     "phone": "07968 715861", "phone_tel": "07968715861", "email": "randsplumbing@live.co.uk",
     "hours": "", "company_line": "R & S Plumbing & Gas Services Limited · Company no. 08694950"},
    {"title": "R&S Plumbing & Gas Services – Plumber in Cheltenham",
     "description": "Cheltenham based plumbing, heating and gas services covering all of Gloucestershire."},
    {"eyebrow": "Cheltenham · Gloucestershire", "h1": "Plumbing you", "h1_accent": "can rely on.",
     "lead": "Cheltenham based plumbing and gas services, covering all of Gloucestershire. High quality work, reliable service and a fair price.",
     "img": ("1732660513320-a6b489f3fece", "Engineer fitting a heating system")},
    ["Which? Trusted Trader", "Cheltenham based", "All of Gloucestershire", "No job too small"],
    ["Boilers", "Central heating", "Radiators", "Gas safety", "Cylinders", "Plumbing repairs"],
    {"eyebrow": "What we do", "heading": ["From a leaky tap", "to a new boiler."],
     "intro": "All the plumbing and gas services you need in your home, from regular servicing to full installations.",
     "items": [
         svc("Boiler installs & repairs", "New boilers fitted, broken ones repaired and yearly servicing.", "flame", "1650551182991-b07558247564", "Heating pipes and valves", "Most asked for"),
         svc("Central heating", "Heating systems installed and serviced, radiators added or replaced.", "house"),
         svc("Gas safety checks", "Gas safety testing and inspection for homes and landlords.", "shield"),
         svc("Unvented cylinders", "Unvented hot water cylinder installation and maintenance.", "drop", "1618840626133-54463084a141", "Close-up of metal pipework"),
         svc("Gas cookers", "Gas cooker installation and safe connection.", "cup"),
         svc("General plumbing", "Leaks, valves, showers and toilets. No job too small.", "wrench"),
     ]},
    [rev("Russ came out very quickly on a Saturday to an emergency repair at my elderly Mum's. Work was minor in the end and his charge reflected this. An honest guy who cares about his work.", "Gloucestershire"),
     rev("Had a new boiler and pipework fitted by R&S and from initial inspection to quote to supply and fit the service by Russ and his team was exceptional. Professional, courteous and quality work completed on schedule.", "Gloucestershire"),
     rev("We had Russ come to a new property we recently purchased, we wanted an additional radiator fitting, another replacing & some new valves fitted to others.", "Gloucestershire")],
    [["Boiler", "flame"], ["Heating", "house"], ["Gas safety", "shield"], ["Leak or repair", "wrench"], ["Hot water", "drop"], ["Something else", "other"]],
    [WHICH_FAQ("R&S Plumbing & Gas Services"),
     {"q": "Do you cover my area?", "a": "We’re based in Cheltenham and cover all of Gloucestershire, and we travel further afield when asked."},
     QUOTE_FAQ("07968 715861")],
    "Need a plumber in Cheltenham?",
    ["Cheltenham", "Gloucester", "Tewkesbury", "Stroud", "Cirencester", "Gloucestershire"],
    ["1650551182991-b07558247564", "1618840626133-54463084a141"],
    "Real reviews from customers on Which? Trusted Traders.",
))

# 4. Steve's Handyman Services Ltd ---------------------------------------------
made.append(lead(
    "steves-handyman", "#F5C542",
    {"name": "Steve’s Handyman Services", "short": "Steve’s", "sub": "Handyman Services", "logo_icon": "wrench",
     "trade": "Handyman", "town": "Milton Keynes", "county": "Buckinghamshire",
     "phone": "07376 010188", "phone_tel": "07376010188", "email": "steveshms@outlook.com",
     "hours": "", "company_line": "Steve’s Handyman Services Ltd · Company no. 13033394"},
    {"title": "Steve’s Handyman Services – Handyman in Milton Keynes",
     "description": "Handyman, decorating and home repairs across Milton Keynes, Buckinghamshire, Bedfordshire and Northamptonshire. No job too small."},
    {"eyebrow": "Milton Keynes · Buckingham · Northampton", "h1": "No job", "h1_accent": "too small.",
     "lead": "Handyman, decorating and home repairs across Milton Keynes and the surrounding area, from a friendly, family team that’s fully insured and DBS checked.",
     "img": ("1789841417999-67a24a247c90", "Person painting a wall with a roller")},
    ["Which? Trusted Trader", "Fully insured", "DBS checked", "Free quotes"],
    ["Decorating", "Repairs", "Fencing", "Flat pack", "Appliances", "Odd jobs"],
    {"eyebrow": "What we do", "heading": ["All the jobs", "on your list."],
     "intro": "Interior, exterior and garden jobs, big or small. Tell us what needs doing and we’ll sort it.",
     "items": [
         svc("Painting & decorating", "Inside and out, from one room to the front of the house.", "brush", "1688372198189-de6a51777a81", "Decorator painting a wall", "Popular"),
         svc("Home repairs", "The small jobs that keep getting put off, done properly.", "wrench"),
         svc("Fences & garden", "Fence posts and panels fixed, and garden maintenance.", "leaf", "1547609434-b732edfee020", "Tradesman sawing timber"),
         svc("Flat pack assembly", "Furniture built and fixed in place so it stays put.", "hammer"),
         svc("Appliance installs", "Cookers, hoods and other appliances fitted.", "bolt"),
         svc("Wallpapering", "Neat wallpapering for feature walls and whole rooms.", "sparkle"),
     ]},
    [rev("Steve was recommended to us - he fitted a safety rail on our front steps. He responded promptly, gave a quote, and then scheduled the work very quickly and efficiently.", "Milton Keynes"),
     rev("Steve and Matt re-fixed 8 fenceposts which had been very wobbly. They used concrete fence repair posts and the fences are solid and no longer sway in the breeze.", "Milton Keynes"),
     rev("Contacted Steve after seeing some good reviews on Google and Which and found he was very approachable to doing all sorts of jobs no job too small…", "Milton Keynes")],
    [["Decorating", "brush"], ["Repair", "wrench"], ["Fencing", "leaf"], ["Flat pack", "hammer"], ["Appliance", "bolt"], ["Something else", "other"]],
    [WHICH_FAQ("Steve’s Handyman Services"),
     {"q": "Is any job too small?", "a": "No. From a single fence panel to decorating a whole house, we’re happy to help."},
     QUOTE_FAQ("07376 010188")],
    "Got a list of jobs that need doing?",
    ["Milton Keynes", "Bletchley", "Stony Stratford", "Deanshanger", "Buckingham", "Aylesbury", "Northampton", "Bicester"],
    ["1688372198189-de6a51777a81", "1547609434-b732edfee020"],
    "Real reviews from customers on Which? Trusted Traders.",
))

# 5. Inspired Restorations (Oxford) Ltd ----------------------------------------
made.append(lead(
    "inspired-restorations", "#C9A27C",
    {"name": "Inspired Restorations", "short": "Inspired", "sub": "Restorations", "logo_icon": "sparkle",
     "trade": "Kitchens & bathrooms", "town": "Oxford", "county": "Oxfordshire",
     "phone": "07920 519188", "phone_tel": "07920519188", "email": "inspired-restorations@hotmail.co.uk",
     "hours": "Mon–Fri 8am–7pm, Sat 9am–5pm", "company_line": "Inspired Restorations Oxford Limited · Company no. 08762577"},
    {"title": "Inspired Restorations – Kitchens, Bathrooms & Renovations in Oxford",
     "description": "Property renovations, kitchens and bathrooms in Oxfordshire. Design help, project management and free no-obligation quotes."},
    {"eyebrow": "Kitchens · Bathrooms · Renovations", "h1": "Rooms you’ll", "h1_accent": "love using.",
     "lead": "Renovations, kitchens and bathrooms across Oxfordshire, from the first design ideas to the final tile. A small business with a personal, friendly service.",
     "img": ("1638799869566-b17fa794c4de", "Bright bathroom with a freestanding bath and walk-in shower")},
    ["Which? Trusted Trader", "Free, no-obligation quotes", "Design help", "Project managed"],
    ["Bathrooms", "En-suites", "Wet rooms", "Kitchens", "Tiling", "Renovations"],
    {"eyebrow": "What we do", "heading": ["Designed, fitted", "and finished."],
     "intro": "We coordinate skilled tradesmen for plastering, electrics, plumbing, tiling and carpentry, so your project is hassle-free.",
     "items": [
         svc("Bathroom renovations", "Full bathroom refits, taken back to brick if needed.", "drop", "1696987007764-7f8b85dd3033", "Modern bathroom with two basins", "Most asked for"),
         svc("Kitchens", "Kitchen design, installation and refurbishment, including granite worktops.", "sparkle", "1768486143865-342d8cc12c90", "Modern kitchen with pendant lights"),
         svc("En-suites & wet rooms", "New en-suites and wet rooms that make the most of the space.", "house", "1584622650111-993a426fbf0a", "Walk-in shower and vanity unit"),
         svc("Accessible bathrooms", "Accessible bathrooms and showers designed around you.", "shield"),
         svc("Tiling & flooring", "Tiling and flooring done neatly and finished properly.", "board"),
         svc("Full renovations", "Complete project management from planning to finish.", "hammer"),
     ]},
    [rev("I asked David at Inspired Restorations to design and deliver significant revamps to a tired kitchen and en-suite bathroom. I am extremely pleased with how it has turned out. The standard of the finished work is superb.", "Oxfordshire"),
     rev("We asked Inspired Restorations to create an internal en-suite and could not be happier with the results.", "Oxfordshire"),
     rev("We needed a full bathroom renovation after a leak caused water damage, and were very anxious about the prospect given past experiences with multiple different contractors and builders.", "Oxfordshire")],
    [["Bathroom", "drop"], ["Kitchen", "sparkle"], ["En-suite", "house"], ["Tiling", "board"], ["Renovation", "hammer"], ["Something else", "other"]],
    [WHICH_FAQ("Inspired Restorations"),
     {"q": "Can you help with the design?", "a": "Yes. We offer design help and impartial advice, so if you don’t know where to start, we can help you make the most of your space."},
     {"q": "Are quotes free?", "a": "Yes. Quotes are free and there’s no obligation."}],
    "Ready to plan your new bathroom or kitchen?",
    ["Oxford", "Oxfordshire"],
    ["1696987007764-7f8b85dd3033", "1768486143865-342d8cc12c90", "1584622650111-993a426fbf0a"],
    "Real reviews from customers on Which? Trusted Traders.",
))

# 6. Arbor Tree Specialists Ltd -------------------------------------------------
made.append(lead(
    "arbor-tree-specialists", "#7BC86C",
    {"name": "Arbor Tree Specialists", "short": "Arbor", "sub": "Tree Specialists", "logo_icon": "leaf",
     "trade": "Tree surgeons", "town": "Oxford", "county": "Oxfordshire",
     "phone": "07702 189233", "phone_tel": "07702189233", "email": "tim@arbortrees.co.uk",
     "hours": "", "company_line": "Arbor Tree Specialists Ltd · Company no. 10943780"},
    {"title": "Arbor Tree Specialists – Tree Surgeons in Oxford & Oxfordshire",
     "description": "Tree surgery and tree surveys across Oxfordshire. NPTC certified arborists, trading since 2010."},
    {"eyebrow": "Tree surgery · Tree surveys · Oxfordshire", "h1": "Expert care", "h1_accent": "for your trees.",
     "lead": "Tree surgery and tree surveys across Oxfordshire, led by Tim O’Connor, who holds the Level 4 Diploma in Arboriculture. Trading since 2010.",
     "img": ("1754322449185-31f56117ed87", "Arborist cutting a branch high in a tree")},
    ["Which? Trusted Trader", "NPTC certified team", "Trading since 2010", "Tree surveys"],
    ["Reductions", "Pruning", "Felling", "Stump grinding", "Hedges", "Planting", "Surveys"],
    {"eyebrow": "What we do", "heading": ["From hedges", "to veteran trees."],
     "intro": "From domestic garden trees and hedges to parkland and community planting, with a professional, forward-thinking approach.",
     "items": [
         svc("Crown reductions & pruning", "Trees reduced, thinned and shaped to keep them healthy.", "leaf", "1709560723503-538158e48db8", "Tree surgeon at work in a tree", "Most asked for"),
         svc("Tree removal & felling", "Safe removal, even in tight spaces.", "shield", "1754322449005-bdc38c631682", "Arborist roping down from a tree"),
         svc("Stump grinding", "Stumps ground out so you can use the space again.", "search"),
         svc("Hedge cutting", "Hedges cut back and reshaped.", "scissors"),
         svc("Tree planting", "The right tree in the right place.", "drop"),
         svc("Tree surveys", "Tree surveys large or small, from a qualified arboriculturist.", "board"),
     ]},
    [rev("Tim was asked to reduce a very large tree, two smaller trees, an overgrown lilac and reshape a long rambling hedge. He and his team did an excellent job.", "Oxfordshire"),
     rev("We were very pleased with the overall quality of the service we received from Arbor trees recently to reduce, prune and shape our two mature garden trees.", "Oxfordshire"),
     rev("This is the second job Arbor Tree Services have done for us. The first job was a tricky big job, taking down a sizeable partially rotten Ash with a very small drop space…", "Oxfordshire")],
    [["Reduce or prune", "leaf"], ["Remove a tree", "shield"], ["Stump", "search"], ["Hedge", "scissors"], ["Tree survey", "board"], ["Something else", "other"]],
    [WHICH_FAQ("Arbor Tree Specialists"),
     {"q": "Are your arborists qualified?", "a": "Yes. Every arborist we employ holds the necessary NPTC certificates and work-specific first aid qualifications."},
     {"q": "Do you do tree surveys?", "a": "Yes. Tim carries the Level 4 Diploma in Arboriculture and carries out tree surveys, large or small."}],
    "Got a tree that needs attention?",
    ["Oxford", "Wheatley", "Wolvercote", "Oxfordshire"],
    ["1709560723503-538158e48db8", "1754322449005-bdc38c631682"],
    "Real reviews from customers on Which? Trusted Traders.",
))

# 7. RAW Plumbing & Heating Ltd -------------------------------------------------
made.append(lead(
    "raw-plumbing-heating", "#4FC3F7",
    {"name": "RAW Plumbing & Heating", "short": "RAW", "sub": "Plumbing & Heating", "logo_icon": "flame",
     "trade": "Plumbers", "town": "Crowthorne", "county": "Berkshire",
     "phone": "01344 776751", "phone_tel": "01344776751", "email": "rawplumbing@me.com",
     "hours": "Mon–Fri 8.30am–5.30pm", "company_line": "RAW Plumbing and Heating Ltd · Company no. 09692738"},
    {"title": "RAW Plumbing & Heating – Plumbers in Crowthorne, Berkshire",
     "description": "Family run plumbing and heating in Crowthorne. Boilers, heating controls, underfloor heating and unvented hot water."},
    {"eyebrow": "Crowthorne · Berkshire · Surrey", "h1": "Heating sorted,", "h1_accent": "fast.",
     "lead": "A family run plumbing and heating business in Crowthorne. Roy and Elliott do the work and Lisa runs the office, covering everything from a dripping tap to a complete heating system.",
     "img": ("1732660513320-a6b489f3fece", "Engineer installing underfloor heating")},
    ["Which? Trusted Trader", "Family run", "On Checkatrade since 2009", "Crowthorne based"],
    ["Boilers", "Heating controls", "Underfloor heating", "Hot water", "Leaks", "New builds"],
    {"eyebrow": "What we do", "heading": ["From a dripping tap", "to a full install."],
     "intro": "Boiler replacements, heating control upgrades, underfloor heating and unvented hot water, plus new build installs from design to fit.",
     "items": [
         svc("Boiler replacement", "New boilers fitted, with heating controls upgraded at the same time.", "flame", "1650551182991-b07558247564", "Heating pipes and valves", "Most asked for"),
         svc("Underfloor heating", "Wet underfloor heating designed and installed.", "house", "1618840626133-54463084a141", "Close-up of heating pipework"),
         svc("Unvented hot water", "Unvented pressurised hot water systems fitted and maintained.", "drop"),
         svc("Radiators & central heating", "Central heating installed and serviced, radiators replaced.", "board"),
         svc("Leaks & repairs", "Leaks found and fixed, taps and pumps replaced.", "wrench"),
         svc("New build installs", "Plumbing and heating for new builds, from design to installation.", "hammer"),
     ]},
    [rev("I have used RAW plumbing on several occasions, usually an emergency and despite being fully booked they have always managed to fit a visit in to rectify the problem very quickly.", "Berkshire"),
     rev("Very pleased with the Service provided by RAW Plumbing to fix a leak, from the first phone call to the office to the Plumber fixing the problem. Kept me informed of the problem plus very clean and tidy as well.", "Surrey"),
     rev("Great communication and options from Lisa in the office and an efficient and clean service from Scott on the day.", "Berkshire")],
    [["Boiler", "flame"], ["Underfloor heating", "house"], ["Hot water", "drop"], ["Leak or repair", "wrench"], ["New build", "hammer"], ["Something else", "other"]],
    [WHICH_FAQ("RAW Plumbing & Heating"),
     {"q": "Who will I speak to?", "a": "Lisa runs our office, taking calls and booking in jobs, so you’ll always speak to someone who knows the diary."},
     QUOTE_FAQ("01344 776751")],
    "Need a plumber or heating engineer?",
    ["Crowthorne", "Berkshire", "Surrey"],
    ["1650551182991-b07558247564", "1618840626133-54463084a141"],
    "Real reviews from customers on Which? Trusted Traders.",
))

# 8. Key Choice Builders Ltd ----------------------------------------------------
made.append(lead(
    "key-choice-builders", "#FF8A3D",
    {"name": "Key Choice Builders", "short": "Key Choice", "sub": "Builders", "logo_icon": "house",
     "trade": "Builders", "town": "Crowthorne", "county": "Berkshire",
     "phone": "07984 434396", "phone_tel": "07984434396", "email": "keychoice@sky.com",
     "hours": "", "company_line": "Key Choice Builders Limited · Company no. 08948820"},
    {"title": "Key Choice Builders – Builders in Crowthorne, Berkshire",
     "description": "Family run builders in Crowthorne with over 20 years’ experience in extensions, refurbishments and repairs."},
    {"eyebrow": "Extensions · Refurbishments · Repairs", "h1": "Extensions", "h1_accent": "done right.",
     "lead": "A family run building company in Crowthorne with over 20 years’ experience in extensions, refurbishments and repair and maintenance work.",
     "img": ("1593786267440-550458cc882a", "Brick house extension being built")},
    ["Which? Trusted Trader", "Family run", "20+ years’ experience", "Crowthorne based"],
    ["Extensions", "Refurbishments", "Garden offices", "Cladding", "Repairs", "Maintenance"],
    {"eyebrow": "What we do", "heading": ["Built with care,", "kept on schedule."],
     "intro": "A customer-based service that’s trustworthy, dependable, clean and tidy.",
     "items": [
         svc("Extensions", "Rear, side and kitchen extensions, from foundations to finish.", "house", "1593623671658-6b842c7f9697", "Extension under construction with steel beams", "Most asked for"),
         svc("Refurbishments", "Whole-house refurbishments and restorations.", "hammer", "1768486143865-342d8cc12c90", "Finished modern kitchen"),
         svc("Garden offices", "Unused garden space turned into a modern office.", "leaf"),
         svc("Cladding & dormers", "Old timber and tiles replaced with low-maintenance cladding.", "roof"),
         svc("Repairs & maintenance", "Repair and maintenance work for homes and contracts.", "wrench"),
         svc("Project management", "One team managing the whole job, start to finish.", "board"),
     ]},
    [rev("Key Choice have built a new extension on piled foundations for us, comprising an extended bedroom, new ensuite bathroom, new utility room and outdoor patio. We are very pleased with the result.", "Berkshire"),
     rev("Working with Key Choice builders was a great experience. Gareth and his team are very responsive and always keep you in the loop.", "Berkshire"),
     rev("We needed an extension to the rear of our property to increase the size of our kitchen and create a working from home area by replacing an existing conservatory. We contacted Gareth having been impressed by previous reviews.", "Berkshire")],
    [["Extension", "house"], ["Refurbishment", "hammer"], ["Garden office", "leaf"], ["Cladding", "roof"], ["Repair", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("Key Choice Builders"),
     {"q": "How long have you been building?", "a": "Over 20 years. We’re a family run business with a strong base of clients around the local area."},
     QUOTE_FAQ("07984 434396")],
    "Planning an extension or refurbishment?",
    ["Crowthorne", "Berkshire"],
    ["1593623671658-6b842c7f9697", "1768486143865-342d8cc12c90"],
    "Real reviews from customers on Which? Trusted Traders.",
))

# 9. Waterpark Heating Ltd -----------------------------------------------------
made.append(lead(
    "waterpark-heating", "#2EC4B6",
    {"name": "Waterpark Heating", "short": "Waterpark", "sub": "Heating", "logo_icon": "flame",
     "trade": "Heating engineers", "town": "Oxford", "county": "Oxfordshire",
     "phone": "01865 639880", "phone_tel": "01865639880", "email": "waterparkheating@gmail.com",
     "hours": "Mon–Sun, 24 hours", "company_line": "Waterpark Heating Limited · Company no. 14152022"},
    {"title": "Waterpark Heating – Plumbing & Heating in Oxford",
     "description": "Family operated plumbing and heating in Oxford. Boilers, heating systems, gas safety and repairs from an engineer with three decades in the trade."},
    {"eyebrow": "Oxford · Oxfordshire", "h1": "Warm homes,", "h1_accent": "honest advice.",
     "lead": "Plumbing and heating in Oxford from Pete, who started in the trade at 15 and has spent three decades on everything from simple repairs to complex heating systems.",
     "img": ("1650551182991-b07558247564", "Heating pipes and valves")},
    ["Which? Trusted Trader", "30 years in the trade", "Family operated", "Oxford based"],
    ["Boilers", "Heating", "Gas safety", "Hot water", "Leaks", "Repairs"],
    {"eyebrow": "What we do", "heading": ["When the heating stops,", "we’re on it."],
     "intro": "When your heating or hot water stops working, you need someone you can rely on. Professional, friendly and dependable.",
     "items": [
         svc("Boilers", "Boiler installation, repairs and servicing.", "flame", "1732660513320-a6b489f3fece", "Engineer working on a heating system", "Most asked for"),
         svc("Heating systems", "Heating systems, radiators and underfloor heating.", "house"),
         svc("Gas safety", "Gas safety testing and inspection, including landlord checks.", "shield"),
         svc("Hot water", "Unvented cylinders, immersion heaters and water heaters.", "drop", "1618840626133-54463084a141", "Close-up of metal pipework"),
         svc("Leaks & plumbing", "Leak detection and general plumbing repairs.", "wrench"),
         svc("Gas cookers & fires", "Gas cookers and fires installed, repaired and serviced.", "cup"),
     ]},
    [rev("I would highly recommend Pete at Waterpark Heating. He came and carried out several general plumbing repairs at my property very efficiently. He is personable, knowledgeable and clearly takes pride in his work.", "Oxfordshire"),
     rev("Pete explained everything including the costs. He guided us every step of the way, and made sure we were happy throughout.", "Oxfordshire"),
     rev("Helpful, knowledgeable, informative, fair, reliable, conscientious, cheerful disposition and the job was done!", "Oxfordshire")],
    [["Boiler", "flame"], ["Heating", "house"], ["Gas safety", "shield"], ["Hot water", "drop"], ["Leak or repair", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("Waterpark Heating"),
     {"q": "Who’s behind Waterpark Heating?", "a": "Pete, who started his career at 15 and has spent three decades working in plumbing and heating."},
     QUOTE_FAQ("01865 639880")],
    "Heating or hot water playing up?",
    ["Oxford", "Oxfordshire"],
    ["1732660513320-a6b489f3fece", "1618840626133-54463084a141"],
    "Real reviews from customers on Which? Trusted Traders.",
))

# 10. Jamie Rickell Carpentry Limited ------------------------------------------
made.append(lead(
    "jamie-rickell-carpentry", "#D9A066",
    {"name": "Jamie Rickell Carpentry", "short": "Jamie Rickell", "sub": "Carpentry", "logo_icon": "hammer",
     "trade": "Carpenters", "town": "Milton Keynes", "county": "Buckinghamshire",
     "phone": "07446 894385", "phone_tel": "07446894385", "email": "jamie.t.rickell@gmail.com",
     "hours": "Mon–Fri 8am–5pm", "company_line": "Jamie Rickell Carpentry Limited · Company no. 10837995"},
    {"title": "Jamie Rickell Carpentry – Carpenter in Milton Keynes",
     "description": "Bespoke carpentry in Milton Keynes: fitted wardrobes, media walls, panelling, decking and garden structures."},
    {"eyebrow": "Milton Keynes · Buckinghamshire · Bedfordshire", "h1": "Carpentry,", "h1_accent": "made to measure.",
     "lead": "Bespoke carpentry in Milton Keynes, from fitted wardrobes and media walls to decking and garden structures, with 15 years’ experience behind every job.",
     "img": ("1659930087003-2d64e33181f7", "Carpenter marking a wooden board")},
    ["Which? Trusted Trader", "15 years’ experience", "Made to measure", "Milton Keynes based"],
    ["Wardrobes", "Media walls", "Panelling", "Decking", "Pergolas", "Garden rooms"],
    {"eyebrow": "What we do", "heading": ["Built to fit", "your space."],
     "intro": "Custom furniture, cabinetry, renovations and outdoor structures, with real attention to detail.",
     "items": [
         svc("Fitted wardrobes", "Built-in wardrobes and bedroom storage made for the room.", "board", "1679797850019-3d0d8659a695", "Carpenter working on a piece of wood", "Most asked for"),
         svc("Media walls & panelling", "Feature walls, acoustic panels and lighting built in.", "sparkle"),
         svc("Decking & pergolas", "Decks, pergolas and gates for the garden.", "leaf", "1790671023265-0e2e1ecfdb78", "Garden lit up in the evening"),
         svc("Garden rooms & cabins", "Log cabins, summer houses and garden structures.", "house"),
         svc("Windows & frames", "Rotten window frames replaced and fitted properly.", "hammer", "1547609434-b732edfee020", "Carpenter sawing timber"),
         svc("Kitchens & utility rooms", "Rooms reconfigured, boxed in and finished neatly.", "wrench"),
     ]},
    [rev("Jamie has done such a lot of work at my property and is responsible for transforming and updating an outdated conservatory and kitchen into a space which is lovely to spend time in and functional and well designed.", "Central Bedfordshire"),
     rev("Jamie did a fantastic job on our acoustic wall with feature lighting we are very pleased with the job, communication and experience from start to finish.", "Milton Keynes"),
     rev("Jamie worked alongside Ardwark electrician and plumber to reconfigure our utility room, boxing in the heat pump cylinder and pipes while keeping it all accessible.", "Milton Keynes")],
    [["Wardrobes", "board"], ["Media wall", "sparkle"], ["Decking", "leaf"], ["Garden room", "house"], ["Windows", "hammer"], ["Something else", "other"]],
    [WHICH_FAQ("Jamie Rickell Carpentry"),
     {"q": "Can you make something bespoke?", "a": "Yes. Custom furniture and cabinetry is what we do, designed around your space and your style."},
     QUOTE_FAQ("07446 894385")],
    "Got a carpentry project in mind?",
    ["Milton Keynes", "Buckinghamshire", "Central Bedfordshire"],
    ["1679797850019-3d0d8659a695", "1790671023265-0e2e1ecfdb78", "1547609434-b732edfee020"],
    "Real reviews from customers on Which? Trusted Traders.",
))

print("\n".join(made))
