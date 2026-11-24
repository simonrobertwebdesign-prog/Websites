"""Write engine/data/<slug>.json for batch 6 of preview leads (24 Nov 2026).

9 new leads from the scheduled evening run.
Every fact comes from the business's own Which? Trusted Traders page or its own website.
Reviews are real 5-star Which? reviews, word for word (trimmed with … only).
Photos: Unsplash (download_asset called for each one), credited per site.
"""
import json, pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
U = "https://images.unsplash.com/photo-{}?ixlib=rb-4.1.0&auto=format&fit=crop&w={}&q=80"
PH = {  # photo id -> (photographer, username)
    "1657730391002-bf55ff069a80": ("Thomas Kinto", "thomaskinto"),
    "1585952749437-d3bc7940958a": ("Andre Ouellet", "ledoc"),
    "1583095117095-adaeabc401ab": ("Etienne Girardet", "etiennegirardet"),
    "1628745277862-bc0b2d68c50c": ("Zac Gudakov", "zacgudakov"),
    "1592506119503-c0b18879bd5a": ("Lotus Design N Print", "lotusdnp"),
    "1576446470246-499c738d1c8e": ("Mark Kats", "bulava92"),
    "1655300283247-6b1924b1d152": ("Watt A Lot", "wattalot"),
    "1786515284601-f9ac47d0758a": ("Aron Schmitz", "as95"),
    "1660330589693-99889d60181e": ("Raze Solar", "razesolar"),
    "1584622650111-993a426fbf0a": ("Lotus Design N Print", "lotusdnp"),
    "1650551182991-b07558247564": ("Immo Wegmann", "tinkerman"),
    "1732660513320-a6b489f3fece": ("Marc Zeman", "der_zeman"),
    "1766507680004-1c71007aefe5": ("dcbel", "privategrid"),
    "1621905251189-08b45d6a269e": ("Emmanuel Ikwuegbu", "emmages"),
    "1761472823286-9f6093ed6663": ("Lara John", "lara_j"),
    "1754322449005-bdc38c631682": ("Zack Masters", "masters25"),
    "1561063206-c8fc36bac012": ("Malachi Brooks", "mebrooks01"),
    "1686596668278-9c2e84490887": ("Artur Łuczka", "artur_luczka"),
    "1635335874521-7987db781153": ("mostafa mahmoudi", "mostafa_mahmoudi24"),
    "1553873002-785d775854c9": ("Hobi industri", "hobiindustri"),
    "1621905251918-48416bd8575a": ("Emmanuel Ikwuegbu", "emmages"),
    "1688372199140-cade7ae820fe": ("Ali Mkumbwa", "mkumbwajr"),
    "1620626011761-996317b8d101": ("Steven Ungermann", "steveungermann"),
    "1599619585752-c3edb42a414c": ("Karl Solano", "karlsolano"),
    "1754321860056-ca7254d5e7ac": ("Zack Masters", "masters25"),
    "1631300313270-227604e71ea5": ("henry perks", "hjkp"),
    "1524369609384-10ce89e42d14": ("Aditya Saxena", "adityaries"),
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

# 1. Mark Newell Tree Care Ltd (Bidford-on-Avon, Stratford-upon-Avon) ------------
made.append(lead(
    "mark-newell-tree-care", "#3F6B3A",
    {"name": "Mark Newell Tree Care", "short": "Mark Newell", "sub": "Tree Care", "logo_icon": "leaf",
     "trade": "Tree surgeon", "town": "Bidford-on-Avon", "county": "Warwickshire",
     "phone": "01789 774091", "phone_tel": "01789774091", "email": "enquiries@marknewelltreecare.co.uk",
     "hours": "", "company_line": "Mark Newell Tree Care Ltd · Company no. 09258803"},
    {"title": "Mark Newell Tree Care – Tree Surgeon in Stratford-upon-Avon & Warwickshire",
     "description": "Fully qualified and insured tree surgeon based in Stratford-upon-Avon, covering Warwickshire, Worcestershire and the Cotswolds. Felling, reductions, pruning, stump grinding and more."},
    {"eyebrow": "Stratford-upon-Avon · Warwickshire · Cotswolds", "h1": "Professional tree care", "h1_accent": "at its best.",
     "lead": "Mark Newell is a fully qualified and insured tree surgeon with a national diploma in tree management and arboriculture. All work undertaken is fully insured and meets British Standard 3998 requirements.",
     "img": ("1657730391002-bf55ff069a80", "Tree surgeon climbing a tree with ropes")},
    ["Which? Trusted Trader", "National Diploma in Arboriculture", "Fully insured", "Work to BS 3998"],
    ["Felling", "Section felling", "Reductions", "Thinning", "Pruning", "Pollarding", "Stump grinding", "Cable bracing", "Tree planting", "Deadwood removal", "Hedge cutting"],
    {"eyebrow": "What we do", "heading": ["Every aspect", "of tree care."],
     "intro": "From work in private gardens to site clearance, whether it is a hedge that needs trimming or a tree that requires felling, there is no job too big.",
     "items": [
         svc("Tree felling", "Felling and section felling, from private gardens to site clearance.", "leaf", "1585952749437-d3bc7940958a", "Tree surgeon working on a high branch"),
         svc("Reductions & thinning", "Tree reductions, thinning and lifting.", "sparkle"),
         svc("Pruning & pollarding", "Pruning, pollarding and deadwood removal.", "leaf"),
         svc("Stump grinding", "Stump grinding to clear the ground after a tree comes down.", "wrench", "1583095117095-adaeabc401ab", "Stack of freshly cut logs"),
         svc("Hedges & planting", "Hedge cutting and tree planting.", "house"),
         svc("Emergency call outs", "Emergency call outs, plus cable bracing.", "shield"),
     ]},
    [rev("Superb job by Mark and his assistant in sorting out a number of our trees. They clearly care very much about trees and their care. Mark gives truthful advice about what to do and not to do, isn’t looking for work to make money, but to do the right thing by trees and his customers. … Highly highly recommended.", "Warwickshire"),
     rev("This is the fifth time I have used Mark Newell Tree Care and that in itself is testament to how reliably good he is. He is very experienced: we are in a conservation area and he takes care of all the permissions and paperwork etc. He is also very clear about costs and schedules. … Highly recommended.", "Warwickshire"),
     rev("Mark and his team did a superb job at our house. … Mark took care of everything from applying for conservation permission to work on the trees, to carrying out the work over two days and to tidying everything. The trees look great and the garden was left spotless. Thank you.", "Warwickshire")],
    [["Tree felling", "leaf"], ["Reduction or pruning", "sparkle"], ["Stump grinding", "wrench"], ["Hedge cutting", "house"], ["Emergency", "shield"], ["Something else", "other"]],
    [WHICH_FAQ("Mark Newell Tree Care"),
     {"q": "Are you qualified and insured?", "a": "Yes. Mark is a fully qualified and insured tree surgeon with a national diploma in tree management and arboriculture, and all work meets British Standard 3998 requirements."},
     {"q": "Which areas do you cover?", "a": "We're based in Stratford-upon-Avon and cover a large area across Warwickshire, Worcestershire and the Cotswolds."},
     {"q": "Who do you work for?", "a": "Private customers, large building companies, gardeners and landscape gardeners, estate agents, property management companies, chartered surveyors and corporate businesses."},
     {"q": "How do I get a quote?", "a": "Use the quote form on this page or call 01789 774091 to arrange a free no obligation quote."}],
    "Got a tree that needs attention?",
    ["Stratford-upon-Avon", "Bidford-on-Avon", "Warwickshire", "Worcestershire", "The Cotswolds"],
    ["1585952749437-d3bc7940958a", "1583095117095-adaeabc401ab"],
    free_quotes=True,
))

# 2. MJP Kitchens and Electrical Ltd (Holyport, Maidenhead) -----------------------
made.append(lead(
    "mjp-kitchens-electrical", "#2F5D8A",
    {"name": "MJP Kitchens & Electrical", "short": "MJP", "sub": "Kitchens & Electrical", "logo_icon": "bolt",
     "trade": "Electrician & kitchen fitter", "town": "Holyport", "county": "Berkshire",
     "phone": "07760 126436", "phone_tel": "07760126436", "email": "info@kitchensandelectrical.com",
     "hours": "", "company_line": "MJP Kitchens and Electrical Ltd · Company no. 08124597"},
    {"title": "MJP Kitchens & Electrical – Electrician & Kitchen Fitter in Maidenhead, Berkshire",
     "description": "A dual trade company: fully qualified electrician and kitchen fitter. Rewiring, fuse boards, lighting, testing and kitchen installations. NAPIT and Trustmark registered."},
    {"eyebrow": "Holyport · Maidenhead · Berkshire", "h1": "Kitchens and electrics,", "h1_accent": "from one team.",
     "lead": "We are a professional Kitchen Installation and Electrical Services company with over 16 years of experience in the Kitchen and Electrical Trade.",
     "img": ("1628745277862-bc0b2d68c50c", "Bright kitchen with wooden worktops")},
    ["Which? Trusted Trader", "NAPIT registered", "Trustmark registered", "Over 16 years’ experience"],
    ["Kitchen installation", "Kitchen refurbishment", "Worktops", "Rewiring", "Fuse boards", "Electric showers", "LED lighting", "Outdoor lighting", "Electrical testing", "Emergency lighting"],
    {"eyebrow": "What we do", "heading": ["Two trades,", "one team."],
     "intro": "We are a dual trade company. Any electrical work is undertaken by a fully qualified electrician, and we can also supply and fit modern and contemporary kitchens.",
     "items": [
         svc("Kitchen installation", "Our qualified fitter has extensive experience installing all types of kitchens to a very high standard, from top of the range units to less expensive suppliers.", "house", "1592506119503-c0b18879bd5a", "Kitchen cabinets and worktop"),
         svc("Refurbishment & worktops", "Kitchen refurbishment, kitchen worktops and granite worktops.", "board"),
         svc("Rewiring & fuse boards", "We can wire any room of the house, and our electrical services always match Part P regulations.", "bolt", "1576446470246-499c738d1c8e", "Circuit breakers in a fuse board"),
         svc("Faults & emergencies", "We can help with almost any electrical fault or problem you have, and we offer an emergency service too.", "shield"),
         svc("Lighting", "LED lighting and upgrades, outdoor lighting, and security and emergency lighting.", "bulb"),
         svc("Testing & showers", "Electrical testing, electric showers and outdoor electrical wiring.", "wrench"),
     ]},
    [rev("Mat and team carried out a total kitchen refit at our property. Absolutely thrilled with the results , fantastic skilled workmanship and lovely to have around our home . would highly recommend and trust", "Berkshire"),
     rev("Mat responded very quickly out of hours to my message regarding an electrical circuit failure. He tried very hard to diagnose the fault over the phone and arrived as promised the next working day to fix. He was thoroughly honest and efficient, solving the issue quickly and without any fuss. … I have no hesitation in recommending him and he will now be top of my list of tradesmen to call!", "Berkshire"),
     rev("Mat and Callum were both amazing! They are both really kind and friendly and we loved having them over to fit our kitchen. They are both outstanding in the services they offer. We faced a few problems and they were not phased and came up with solutions. We absolutely love our kitchen. I would not hesitate to recommend them to anyone!", "Berkshire")],
    [["Kitchen fitting", "house"], ["Rewiring", "bolt"], ["Fuse board", "shield"], ["Lighting", "bulb"], ["Electrical fault", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("MJP Kitchens & Electrical"),
     {"q": "Are you registered?", "a": "Yes. Our electrical services always match Part P regulations and we are NAPIT and Trustmark registered."},
     {"q": "Do you offer an emergency service?", "a": "Yes. We offer an emergency service for electrical faults, and our turnaround time is usually very fast."},
     {"q": "Can you do the kitchen and the electrics?", "a": "Yes. We are a dual trade company, so we can fit your kitchen and do the electrical work too."},
     QUOTE_FAQ("07760 126436")],
    "Planning a new kitchen or electrical work?",
    ["Holyport", "Maidenhead", "Berkshire"],
    ["1592506119503-c0b18879bd5a", "1576446470246-499c738d1c8e"],
))

# 3. Techfor Energy Limited (Guildford) ------------------------------------------
made.append(lead(
    "techfor-energy", "#B86B00",
    {"name": "Techfor Energy", "short": "Techfor", "sub": "Energy", "logo_icon": "sparkle",
     "trade": "Solar PV installer", "town": "Guildford", "county": "Surrey",
     "phone": "0800 888 6544", "phone_tel": "08008886544", "email": "glenn.ashby@techforenergy.co.uk",
     "hours": "Mon–Fri 9am–6pm", "company_line": "Techfor Energy Limited · Company no. 07015685"},
    {"title": "Techfor Energy – Solar Panel & Battery Installers in Guildford, Surrey",
     "description": "Solar PV, battery storage and ground-based systems for homes and businesses. SunPower Authorised Dealer, Enphase micro inverters, and free, no obligation online surveys."},
    {"eyebrow": "Guildford · Surrey", "h1": "Solar power,", "h1_accent": "designed for you.",
     "lead": "Solar PV and battery storage for residential and commercial properties. As a SunPower Authorised Dealer we can design systems using the market leading panel from the USA, which is over 20% efficient.",
     "img": ("1655300283247-6b1924b1d152", "Solar panels set into a house roof")},
    ["Which? Trusted Trader", "SunPower Authorised Dealer", "Enphase micro inverters", "Free online surveys"],
    ["Solar PV", "Battery storage", "Ground-based systems", "SunPower panels", "Enphase micro inverters", "Solar thermal", "Solar water heating", "Solar panel maintenance", "Home energy analysis"],
    {"eyebrow": "What we do", "heading": ["Generate more,", "use less from the grid."],
     "intro": "We offer free, no obligation on-line surveys and expert advice on energy saving as well as generation.",
     "items": [
         svc("Solar PV", "Solar panel systems for residential and commercial properties, designed around the market leading SunPower panel.", "sparkle", "1786515284601-f9ac47d0758a", "Solar panels on a roof"),
         svc("Battery storage", "Battery energy storage alongside your solar panels.", "bolt"),
         svc("Ground-based systems", "Ground-based solar systems on residential and commercial properties.", "leaf"),
         svc("Micro inverters", "We specialise in Enphase micro inverters.", "wrench", "1660330589693-99889d60181e", "Electrician working on an electrical panel"),
         svc("Solar thermal", "Solar thermal and solar water heating.", "flame"),
         svc("Energy advice", "Home energy analysis and expert advice on energy saving as well as generation.", "search"),
     ]},
    [rev("Techfor Energy did a ground installation of solar panels and a bank of 3 batteries. Glenn did a thorough survey and suggested the optimal positioning of the equipment. … The installation was done very professionally and carefully and the guys on site were brilliant.", "", who="Which? customer"),
     rev("The members of Glenn's Techfor Energy team are all professional, efficient, and nice to have around. They installed solar panels and a battery, all of which are already producing sufficient power for our household use, so our 'grid dependency' is negligible; rather we are exporting power to the grid! … I am extremely satisfied with the work carried out.", "Berkshire"),
     rev("Couldn’t be happier with the experience of Techfor Energy’s installation of Tesla batteries following their prior installation of solar panels. Glenn and his team were knowledgeable and responsive when specifying the system and the work itself was carried out promptly, professionally and with no fuss. …", "Surrey")],
    [["Solar panels", "sparkle"], ["Battery storage", "bolt"], ["Solar + battery", "house"], ["Ground-based system", "leaf"], ["Maintenance", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("Techfor Energy"),
     {"q": "Do you offer surveys?", "a": "Yes. We offer free, no obligation on-line surveys and expert advice on energy saving as well as generation."},
     {"q": "Which panels do you use?", "a": "As a SunPower Authorised Dealer we can design systems using the market leading panel from the USA, which is over 20% efficient. We also specialise in Enphase micro inverters."},
     {"q": "Do you work on commercial properties?", "a": "Yes. We install systems, including ground-based systems, on residential and commercial properties."},
     QUOTE_FAQ("0800 888 6544")],
    "Thinking about solar?",
    ["Guildford", "Surrey"],
    ["1786515284601-f9ac47d0758a", "1660330589693-99889d60181e"],
))

# 4. Hertford Plumbers Limited (Ware) --------------------------------------------
made.append(lead(
    "hertford-plumbers", "#1F6F8B",
    {"name": "Hertford Plumbers", "short": "Hertford Plumbers", "sub": "Plumbing & Heating", "logo_icon": "drop",
     "trade": "Plumbers & heating engineers", "town": "Ware", "county": "Hertfordshire",
     "phone": "07721 727514", "phone_tel": "07721727514", "email": "hertfordplumbersltd@outlook.com",
     "hours": "", "company_line": "Hertford Plumbers Limited · Company no. 09196662"},
    {"title": "Hertford Plumbers – Plumbing & Heating in Hertfordshire, Essex & London",
     "description": "A family company providing all aspects of plumbing and heating: boilers, air source heat pumps, underfloor heating, bathrooms and wet rooms. Worcester accredited installer."},
    {"eyebrow": "Ware · Hertfordshire · Essex · London", "h1": "Plumbing & heating,", "h1_accent": "every part of it.",
     "lead": "Hertford Plumbers Ltd is a family company providing all aspects of plumbing and heating, from boiler installations, breakdowns and services to bathroom and wet-room installations.",
     "img": ("1584622650111-993a426fbf0a", "Modern bathroom with a walk-in shower")},
    ["Which? Trusted Trader", "Family company", "Worcester accredited installer", "Fully insured"],
    ["Boiler installations", "Boiler repairs", "Boiler servicing", "Air source heat pumps", "Underfloor heating", "Bathrooms", "Wet rooms", "Landlord gas safety certificates", "Central heating flushes", "Unvented cylinders"],
    {"eyebrow": "What we do", "heading": ["Heating, plumbing", "and bathrooms."],
     "intro": "We will design, supply and fit full heating systems, including Air Source Heat Pumps and underfloor heating.",
     "items": [
         svc("Boiler installations", "We are a Worcester accredited installer for boilers, recommending these products to all our existing and potential customers.", "flame", "1650551182991-b07558247564", "Heating pipes and valves"),
         svc("Boiler repairs & servicing", "Boiler breakdowns and repairs, boiler services, and landlord gas safety certificates.", "wrench"),
         svc("Heat pumps & underfloor heating", "We design, supply and fit full heating systems, including Air Source Heat Pumps and underfloor heating.", "house", "1732660513320-a6b489f3fece", "Underfloor heating pipes being fitted"),
         svc("Bathrooms & wet rooms", "All aspects of bathroom and wet-room installations, including accessible bathrooms and showers.", "drop"),
         svc("Central heating flushes", "Central heating flushes for your system.", "sparkle"),
         svc("Cylinders & risk assessments", "Unvented cylinder installation and maintenance, and legionnaire's risk assessment.", "shield"),
     ]},
    [rev("We recently had extensive renovation work carried out by Hertford Plumbers, including our hallway, downstairs WC and cloakroom, and we are absolutely delighted with the results. John, Rob and the team have done a fantastic job. The quality of their workmanship, professionalism and attention to detail have been excellent throughout. …", "Hertfordshire"),
     rev("Very old Stuart Turner pressure boosting pump failed last week depriving me of bath/shower. Called Rob at Hertford Plumbers who advised on replacement and costs and ordered it. Arrived with them late Friday, and installed by Mark by lunchtime Monday. And it's quieter than the old one! Very happy!", "Hertfordshire"),
     rev("John and Rob completely refurbished my bathroom and cloakroom, and I am delighted with the results. They were always polite, friendly, and considerate. Good communication, and they always arrived when they said they would. Good attention to detail and clean and tidy. Highly recommended.", "Hertfordshire")],
    [["Boiler", "flame"], ["Heat pump", "leaf"], ["Underfloor heating", "house"], ["Bathroom or wet room", "drop"], ["Repair", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("Hertford Plumbers"),
     {"q": "Which areas do you cover?", "a": "We provide plumbing and heating services in Hertfordshire, Essex and the London area."},
     {"q": "Do you fit heat pumps?", "a": "Yes. We will design, supply and fit full heating systems, including Air Source Heat Pumps and underfloor heating."},
     {"q": "Are you insured?", "a": "Yes, we are fully insured."},
     {"q": "How do I get a quote?", "a": "Use the quote form on this page or call 07721 727514. We are happy to provide free estimates."}],
    "Need a plumber or heating engineer?",
    ["Ware", "Hertfordshire", "Essex", "London"],
    ["1650551182991-b07558247564", "1732660513320-a6b489f3fece"],
    free_quotes=True,
))

# 5. S B H Electrical Ltd (Chertsey) ---------------------------------------------
made.append(lead(
    "sbh-electrical", "#2E7D5B",
    {"name": "SBH Electrical", "short": "SBH", "sub": "Electrical", "logo_icon": "bolt",
     "trade": "Electrician", "town": "Chertsey", "county": "Surrey",
     "phone": "07779 615107", "phone_tel": "07779615107", "email": "sbhelectrical@outlook.com",
     "hours": "", "company_line": "S B H Electrical Ltd · Company no. 06437638"},
    {"title": "SBH Electrical – Electrician in Chertsey, Surrey",
     "description": "Electrical installations, repairs, testing, EV charging points, solar panels, battery storage, heat pumps, ventilation and air conditioning in Chertsey and Surrey."},
    {"eyebrow": "Chertsey · Surrey", "h1": "The right solution,", "h1_accent": "big or small.",
     "lead": "We love finding the right solution for every situation big or small, from electrical repairs and rewiring to EV charging points, solar panels and air source heat pumps.",
     "img": ("1766507680004-1c71007aefe5", "Electric car charger mounted on a wall")},
    ["Which? Trusted Trader", "Installations & repairs", "EV charging points", "Renewable energy"],
    ["Electrical installations", "Electrical repairs", "Rewiring", "Fuse boards", "Electric showers", "Landlord safety certificates", "EV charging points", "Solar panels", "Battery storage", "Air source heat pumps", "Ventilation", "Air conditioning"],
    {"eyebrow": "What we do", "heading": ["Wiring, charging", "and renewables."],
     "intro": "Electrical work, EV charging points and renewable energy for your home. Call to discuss your needs.",
     "items": [
         svc("Installations & repairs", "Electrical installations and repairs, emergency call outs, outdoor wiring and electric showers.", "bolt", "1621905251189-08b45d6a269e", "Electrician at work"),
         svc("Rewiring & fuse boards", "Rewiring and fuse board work.", "wrench"),
         svc("Testing & certificates", "Electrical testing services and landlord safety certificates.", "check"),
         svc("EV charging points", "Electric vehicle charging points.", "car"),
         svc("Solar & battery storage", "Solar panels, solar panel maintenance and battery storage.", "sparkle", "1761472823286-9f6093ed6663", "Houses with solar panels on their roofs"),
         svc("Heat pumps, ventilation & AC", "Air and ground source heat pumps, ventilation systems and air conditioning.", "leaf"),
     ]},
    [rev("Very happy with the work that Stuart did for me, I had no knowledge on ev chargers but Stuart made the whole process very easy and professional.", "Surrey"),
     rev("Stuart was a true professional and a pleasure to have in my home. He sorted out my ventilation problem and went to great lengths to source a replacement. My two year old ventilation problem has been resolved. No need for a humidifier 😊", "Greater London"),
     rev("Very happy with the service I received from Stuart (SBH Electrical). He came out very quickly on a Saturday when I was worried about a faulty light fitting. He was courteous and very easy to talk to and reassured me. He made sure everything was safe before leaving (even checked the gas leads as an extra). Highly recommend.", "Surrey")],
    [["Electrical repair", "bolt"], ["Rewiring", "wrench"], ["EV charger", "car"], ["Solar or battery", "sparkle"], ["Heat pump or AC", "leaf"], ["Something else", "other"]],
    [WHICH_FAQ("SBH Electrical"),
     {"q": "Do you install EV chargers?", "a": "Yes. We install electric vehicle charging points."},
     {"q": "Do you do renewable energy?", "a": "Yes. We install solar panels and battery storage, and air and ground source heat pumps."},
     {"q": "Can you do landlord safety certificates?", "a": "Yes. We carry out electrical testing and landlord safety certificates."},
     QUOTE_FAQ("07779 615107")],
    "Need an electrician?",
    ["Chertsey", "Surrey"],
    ["1621905251189-08b45d6a269e", "1761472823286-9f6093ed6663"],
))

# 6. Burnley's Tree Services Ltd (Stevenage) --------------------------------------
made.append(lead(
    "burnleys-tree-services", "#5A7D2A",
    {"name": "Burnley's Tree Services", "short": "Burnley's", "sub": "Tree Services", "logo_icon": "leaf",
     "trade": "Tree surgeons", "town": "Stevenage", "county": "Hertfordshire",
     "phone": "07852 169278", "phone_tel": "07852169278", "email": "simon@burnleystreeservices.co.uk",
     "hours": "", "company_line": "Burnley's Tree Services Ltd · Company no. 13730285"},
    {"title": "Burnley's Tree Services – Tree Surgeons in Hertfordshire, Bedfordshire & North London",
     "description": "Qualified and insured tree surgeons with over 10 years' experience. Reductions, trimming, rigging, tree removal, stump removal and replanting, all to BS3998."},
    {"eyebrow": "Stevenage · Hertfordshire · Bedfordshire · North London", "h1": "Tree surgery,", "h1_accent": "to the highest standard.",
     "lead": "We are an arboricultural services company based in Hertfordshire with over 10 years experience in the Arb industry, qualified and insured to carry out all aspects of tree surgery.",
     "img": ("1754322449005-bdc38c631682", "Tree surgeon working high in a tree")},
    ["Which? Trusted Trader", "Over 10 years’ experience", "Qualified & insured", "Work to BS3998"],
    ["Tree reductions", "Trimming", "Rigging", "Tree removal", "Tree thinning", "Stump grinding", "Stump removal", "Replanting", "Tree planting", "OPM removal"],
    {"eyebrow": "What we do", "heading": ["All aspects", "of tree surgery."],
     "intro": "We pride ourselves on completing all aspects of work to the highest standard and put customer satisfaction at the heart of what we do.",
     "items": [
         svc("Reductions & trimming", "From small tree reductions and trimming upwards.", "leaf", "1561063206-c8fc36bac012", "Climbing rope and carabiner for tree work"),
         svc("Rigging & removal", "Rigging techniques to lower trees down safely, and full tree removal.", "shield"),
         svc("Tree thinning", "Tree thinning, carried out to BS3998 industry standards.", "sparkle"),
         svc("Stump removal", "Full stump removal and stump grinding.", "wrench", "1686596668278-9c2e84490887", "Stack of cut logs"),
         svc("Planting & replanting", "Tree planting and replanting.", "leaf"),
         svc("OPM removal", "OPM removal.", "search"),
     ]},
    [rev("Simon and his team arrived early, all of them were lovely. Cut down 2 conifers and cleared everything and kept the area clean. I would recommend them very highly. I have them coming back later in the year to prune another big tree for me.", "Luton"),
     rev("Simon and his team came when promised to fell to ground level a dead acacia tree in our back garden and grind out the stump. They did the job professionally with all the right safety equipment, avoided damaging nearby trees and shrubs, removed the remains of the tree and left the garden very tidy. …", "Hertfordshire"),
     rev("Simon and his team were very polite and did a great job at trimming down a large hedge at the side of our house and pruning back a large lilac tree in our garden. We were very pleased with the work done, and how well they tidied up afterwards. We will definitely be using them again in the future.", "Hertfordshire")],
    [["Tree reduction", "leaf"], ["Tree removal", "shield"], ["Stump grinding", "wrench"], ["Hedge trimming", "sparkle"], ["Planting", "house"], ["Something else", "other"]],
    [WHICH_FAQ("Burnley's Tree Services"),
     {"q": "Are you qualified and insured?", "a": "Yes. We are qualified and insured to carry out all aspects of tree surgery, and all our work is carried out to BS3998 industry standards."},
     {"q": "Which areas do you cover?", "a": "We are based in North Hertfordshire but cover a large area including Bedfordshire, North London, and surrounding areas."},
     {"q": "Can you work to my schedule?", "a": "We will always do our utmost to work to your schedule."},
     {"q": "How do I get a quote?", "a": "Use the quote form on this page or call 07852 169278 for a free no obligation quotation."}],
    "Got a tree that needs work?",
    ["Stevenage", "North Hertfordshire", "Bedfordshire", "North London"],
    ["1561063206-c8fc36bac012", "1686596668278-9c2e84490887"],
    free_quotes=True,
))

# 7. SMD Electrical Services Limited (Byfleet, West Byfleet) -----------------------
made.append(lead(
    "smd-electrical", "#3949AB",
    {"name": "SMD Electrical Services", "short": "SMD", "sub": "Electrical Services", "logo_icon": "bolt",
     "trade": "Electrician", "town": "West Byfleet", "county": "Surrey",
     "phone": "07815 478674", "phone_tel": "07815478674", "email": "info@smdelectricalservices.co.uk",
     "hours": "", "company_line": "SMD Electrical Services Limited · Company no. 05421263"},
    {"title": "SMD Electrical Services – NICEIC Approved Electrician in Byfleet, Surrey",
     "description": "NICEIC Approved local electrician providing electrical installation, maintenance, inspection and testing throughout Surrey, for homes and businesses."},
    {"eyebrow": "Byfleet · West Byfleet · Surrey", "h1": "Electrical work,", "h1_accent": "done thoroughly.",
     "lead": "SMD Electrical Services Ltd provides all types of electrical installation work, maintenance, inspection and testing services throughout Surrey and surrounding areas. NICEIC Approved and happy to take on the smallest to the largest job.",
     "img": ("1635335874521-7987db781153", "Neatly wired fuse box")},
    ["Which? Trusted Trader", "NICEIC Approved", "Which? Local Business of the Year 2010", "CRB checked"],
    ["Installations", "Rewiring", "Fuse boards", "Inspection & testing", "Landlord certificates", "Fault finding", "LED lighting", "Emergency lighting", "EV charge points", "Smart homes", "Extractor fans", "Outdoor wiring"],
    {"eyebrow": "What we do", "heading": ["Every type of", "electrical job."],
     "intro": "Operating in the domestic and commercial markets, we pride ourselves on providing a reliable, experienced, conscientious and thorough service.",
     "items": [
         svc("Installations & rewiring", "Electrical installations, rewiring, fuse boards and outdoor electrical wiring.", "bolt", "1621905251918-48416bd8575a", "Electrician holding his tools"),
         svc("Inspection & testing", "Inspection and testing, with NICEIC Safety Certificates and landlord safety certificates where required.", "check", "1553873002-785d775854c9", "Electrical test meter"),
         svc("Fault finding & repairs", "Fault finding, electrical repairs and emergency call outs.", "wrench"),
         svc("Lighting", "LED lighting and upgrades, outdoor lighting, and emergency lighting with annual testing.", "bulb"),
         svc("Smart homes", "Home automation, automated home audio and security.", "house"),
         svc("EV, ventilation & fans", "Electric car charge points, ventilation systems and extractor fans.", "car"),
     ]},
    [rev("Steve replaced my consumer unit and completed thorough testing and compliance of our home and outbuilding circuits. … Steve is dependable and works to a high standard. He kept me updated with progress, cleaned up each day and has a simple pricing structure. I found SMD Electrical Services' details on the Which? Trusted Trader Site and highly recommend them.", "Surrey"),
     rev("Initially called Steve to replace a light and he pointed out an electrical problem. Over 3 visits he rectified all our electrical problems. He always arrived on time and explained his work and why he was doing it. Would recommend.", "Surrey"),
     rev("Steve undertook extensive electrical work when we moved house. The house needed new fuse boards, new sockets, new lights in the bathroom, garage rewired, fire/smoke alarms fitted. … He explained what needed to be done and why. We are very happy with the work completed and feel a lot safer knowing that an expert has tested everything. … I can highly recommend Steve.", "Surrey")],
    [["Rewiring", "bolt"], ["Fuse board", "shield"], ["Testing", "check"], ["Lighting", "bulb"], ["Fault", "wrench"], ["Something else", "other"]],
    [WHICH_FAQ("SMD Electrical Services"),
     {"q": "Are you NICEIC approved?", "a": "Yes. We are NICEIC Approved and provide documentation and NICEIC Safety Certificates where required."},
     {"q": "Do you take on small jobs?", "a": "Yes. We're happy to take on the smallest to the largest job."},
     {"q": "Which areas do you cover?", "a": "Surrey and surrounding areas."},
     QUOTE_FAQ("07815 478674")],
    "Need an electrician?",
    ["Byfleet", "West Byfleet", "Surrey"],
    ["1621905251918-48416bd8575a", "1553873002-785d775854c9"],
))

# 8. H Plus Global Ltd (Feltham) --------------------------------------------------
made.append(lead(
    "h-plus-global", "#B04A2F",
    {"name": "H Plus Global", "short": "H Plus", "sub": "Building & Decorating", "logo_icon": "house",
     "trade": "Builders & decorators", "town": "Feltham", "county": "Middlesex",
     "phone": "07720 377205", "phone_tel": "07720377205", "email": "tom.urbanski@hplus.global",
     "hours": "Mon–Sat 8am–8pm", "company_line": "H Plus Global Ltd · Company no. 08478071"},
    {"title": "H Plus Global – Builders, Decorators & Home Improvements in Feltham, Middlesex",
     "description": "Building work, interior and exterior decorating, kitchens, bathrooms, roofing and doors in Feltham and Middlesex."},
    {"eyebrow": "Feltham · Middlesex", "h1": "Building, decorating", "h1_accent": "and repairs.",
     "lead": "Building work, interior and exterior decorating, kitchens, bathrooms, roofing and doors, all from one team.",
     "img": ("1688372199140-cade7ae820fe", "Decorator painting a wall with a roller")},
    ["Which? Trusted Trader", "Builders & decorators", "Kitchens & bathrooms", "Roofing & doors"],
    ["Extensions", "Loft conversions", "Garage conversions", "Plastering", "Interior decorating", "Exterior decorating", "Wallpapering", "Kitchens", "Bathrooms", "Wet rooms", "Flat roofing", "Guttering", "Doors"],
    {"eyebrow": "What we do", "heading": ["One team for", "your home."],
     "intro": "Building work, decorating, kitchens, bathrooms, roofing and doors.",
     "items": [
         svc("Building work", "Extensions, loft conversions, garage conversions, porches, conservatories and plastering.", "hammer"),
         svc("Decorating", "Interior and exterior decorating, wallpapering, exterior house painting, rendering and wall coating.", "brush", "1599619585752-c3edb42a414c", "Paint roller in a tray of white paint"),
         svc("Kitchens", "Kitchen design, installation and refurbishment, worktops and kitchen tiling.", "house"),
         svc("Bathrooms", "Bathroom design, installation and refurbishment, bathroom tiling and wet rooms.", "drop", "1620626011761-996317b8d101", "Bathroom with a freestanding bath"),
         svc("Roofing", "Flat roofing, rubber (EPDM) and GRP roofing, lead work, guttering, fascias and soffits.", "roof"),
         svc("Doors", "Front doors, French doors, patio, bi-fold, composite, timber, uPVC and aluminium doors.", "shield"),
     ]},
    [rev("As well as a full redecoration there was damage repairs required from a roof leak which were handled brilliantly. Tom was very helpful. It’s easy to recommend this company as they provided an excellent service.", "Surrey"),
     rev("My kitchen had been exhibiting damp in multiple places over many years and I couldn't seem to fix the problem. Tom and his team surveyed and diagnosed the problem and set to work on the external problem (which was structural) and then fixed the internal problem which was cosmetic. An excellent job. His team is so professional and polite and I'd strongly recommend them to anyone.", "Greater London"),
     rev("Leaks, leaks and more leaks over many years. Tom and his team fixed this chronic challenge in a very short period of time and also repainted the kitchen as well so I got even more benefit than I signed up for. The team were lovely, hard working and very skilled. The kitchen is now a joy to be in come rain or shine. Thanks Guys!!", "Greater London")],
    [["Building work", "hammer"], ["Decorating", "brush"], ["Kitchen", "house"], ["Bathroom", "drop"], ["Roofing", "roof"], ["Something else", "other"]],
    [WHICH_FAQ("H Plus Global"),
     {"q": "What kind of work do you do?", "a": "Building work, interior and exterior decorating, kitchens, bathrooms, roofing and doors."},
     {"q": "When are you open?", "a": "Monday to Saturday, 8am to 8pm."},
     QUOTE_FAQ("07720 377205")],
    "Planning work on your home?",
    ["Feltham", "Middlesex"],
    ["1599619585752-c3edb42a414c", "1620626011761-996317b8d101"],
))

# 9. Stump Master Tree Services Ltd (Waterlooville) -------------------------------
made.append(lead(
    "stump-master-tree-services", "#6B4F2A",
    {"name": "Stump Master Tree Services", "short": "Stump Master", "sub": "Tree Services", "logo_icon": "leaf",
     "trade": "Tree surgeons", "town": "Waterlooville", "county": "Hampshire",
     "phone": "07890 261347", "phone_tel": "07890261347", "email": "smts22@outlook.com",
     "hours": "Mon–Sat 8am–6pm", "company_line": "Stump Master Tree Services Ltd · Company no. 14047231"},
    {"title": "Stump Master Tree Services – Tree Surgeons in Waterlooville, Hampshire",
     "description": "A family-run tree surgery business based in Hampshire, covering Hampshire, West Sussex and Surrey for domestic and commercial clients. Fully insured."},
    {"eyebrow": "Waterlooville · Hampshire · West Sussex · Surrey", "h1": "Family-run", "h1_accent": "tree surgery.",
     "lead": "We are a family-run tree surgery business based in Hampshire, providing professional tree care services across Hampshire, West Sussex and Surrey for both domestic and commercial clients.",
     "img": ("1754321860056-ca7254d5e7ac", "Tree surgeon cutting a tree with a chainsaw")},
    ["Which? Trusted Trader", "Family-run", "Fully insured", "Help with TPO applications"],
    ["Tree felling", "Tree removal", "Stump grinding", "Stump removal", "Crown reductions", "Crown lifting", "Tree shaping", "Pruning", "Hedge cutting", "Shrub shaping", "Garden clearance"],
    {"eyebrow": "What we do", "heading": ["Trees, stumps", "and hedges."],
     "intro": "We take pride in delivering reliable, high-quality workmanship and are fully insured for your peace of mind.",
     "items": [
         svc("Tree felling & removal", "Tree felling and removal for domestic and commercial clients.", "leaf", "1631300313270-227604e71ea5", "Tree surgeon working on a branch"),
         svc("Stump grinding & removal", "Stump grinding and stump removal.", "wrench", "1524369609384-10ce89e42d14", "Cut tree logs"),
         svc("Crown reductions & lifting", "Crown reductions and crown lifting.", "sparkle"),
         svc("Shaping & pruning", "Tree shaping and pruning.", "leaf"),
         svc("Hedges & shrubs", "Hedge and shrub cutting, trimming and shaping, and all aspects of tree and hedge maintenance.", "house"),
         svc("TPO applications", "We can assist with Tree Preservation Order (TPO) applications and provide expert advice where required.", "shield"),
     ]},
    [rev("We had two trees felled, the stumps removed and a hedge reduced in height. Chris and the team arrived promptly at the time and date agreed. They worked very hard using appropriate safety equipment. The care of the garden and the tidy up after the work was impressive. We were delighted with the outcome as was our neighbour who has now recruited them for some work in their garden!", "Hampshire"),
     rev("We have used Chris three times now, and each time he has been fantastic. He’s taken a tree out and ground the stump down, also on two more occasions to grind out roots from other tree issues. … Very reasonable prices and great service, I’d definitely recommend and would use again if needed.", "Hampshire"),
     rev("Used for reducing crowns and cutting back lots of overgrown hedges. Friendly and efficient service. Very competitive quote, flexible during work. Cleared up nicely too. Will definitely use again.", "West Sussex")],
    [["Tree felling", "leaf"], ["Stump grinding", "wrench"], ["Crown reduction", "sparkle"], ["Hedge cutting", "house"], ["TPO advice", "shield"], ["Something else", "other"]],
    [WHICH_FAQ("Stump Master Tree Services"),
     {"q": "Which areas do you cover?", "a": "We're based in Hampshire and cover Hampshire, West Sussex and Surrey, for both domestic and commercial clients."},
     {"q": "Are you insured?", "a": "Yes, we are fully insured for your peace of mind."},
     {"q": "Can you help with Tree Preservation Orders?", "a": "Yes. We can assist with Tree Preservation Order (TPO) applications and provide expert advice where required."},
     {"q": "How do I get a quote?", "a": "Use the quote form on this page or call 07890 261347 for a free, no-obligation quotation."}],
    "Got a tree or stump to deal with?",
    ["Waterlooville", "Hampshire", "West Sussex", "Surrey"],
    ["1631300313270-227604e71ea5", "1524369609384-10ce89e42d14"],
    free_quotes=True,
))

print("\n".join(made))
