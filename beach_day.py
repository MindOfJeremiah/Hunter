# beach_day.py — cross-references SoCal beaches with nearby food, drinks, spots, and budget info.
# Usage:
#   python3 beach_day.py                  → lists all beaches
#   python3 beach_day.py zuma             → full breakdown for Zuma
#   python3 beach_day.py --vibe quiet     → beaches matching a vibe
#   python3 beach_day.py --budget 20      → beaches + food you can do under $20/person

import sys

BEACHES = {
    "seal_beach": {
        "name": "Seal Beach",
        "city": "Seal Beach",
        "vibe": ["small town", "quiet pier", "local", "not touristy", "chill"],
        "parking": "Free street parking on Main St and side streets",
        "fire_pit": False,
        "notes": "15min from Long Beach and feels like a different world. Small town main street, old pier, way less crowded. Good for actually talking and being present. Nobody's performing here.",
        "food_nearby": [
            {"name": "Nick's Deli", "type": "Deli / sandwiches", "price": "$", "distance": "0.2mi", "note": "Cash only, been there forever, solid sandwiches"},
            {"name": "Crema Cafe", "type": "Coffee / breakfast", "price": "$", "distance": "0.1mi", "note": "Good spot to start the day, not a chain, local energy"},
            {"name": "Walt's Wharf", "type": "Seafood", "price": "$$$", "distance": "0.3mi", "note": "Splurge option — fresh fish, good atmosphere, worth it for a special day"},
            {"name": "Bogarts Coffee", "type": "Coffee / smoothies", "price": "$", "distance": "0.4mi", "note": "Chill, local, good acai bowls"},
        ],
        "drinks_nearby": [
            {"name": "Seal Beach Brewing Co.", "type": "Craft brewery", "price": "$$", "distance": "0.3mi", "note": "Right on Main Street. Small batch brews, relaxed patio. Good way to end the beach part of the day."},
            {"name": "Hennessey's Tavern", "type": "Bar", "price": "$$", "distance": "0.2mi", "note": "Classic Seal Beach bar on Main. Nothing fancy, cold drinks, friendly crowd."},
        ],
        "spots_nearby": [
            "Seal Beach Pier — one of the oldest wooden piers in CA, walk to the end at sunset",
            "Main Street — small shops, no chains, just walk it",
            "Surfside Colony beach — gated but the stretch just south is quiet and barely anyone goes",
        ],
        "smoke_spots": [
            "South end past the volleyball courts — beach gets empty fast",
            "Under the pier on the south side — sheltered, low traffic",
            "The jetty rocks at the north end — blocked from the main beach, good view",
        ],
        "budget_per_person": 15,
    },
    "horny_corner": {
        "name": "Horny Corner",
        "city": "Long Beach",
        "vibe": ["private", "quiet", "tucked away", "local secret", "no crowds"],
        "parking": "Free street parking at the dead end of 54th Place — quiet residential dead end, usually just a couple cars if any. No meters, no pay stations. Park and step right onto the beach.",
        "fire_pit": False,
        "notes": "Quiet at the end of 54th Street. No lifeguards to bother, not normally overcrowded, no beach tournaments. Just the water and the sun. Most people don't even know this beach exists. Juneteenth falls on a Friday this year so expect a little more company than usual — but nothing like the main beaches. This one stays under the radar.",
        "food_nearby": [
            {"name": "Brothers Keeper BBQ", "type": "BBQ", "price": "$$", "distance": "1.5mi", "note": "Black-owned Long Beach BBQ by Mo Stewart. Central Texas style with a California twist — oak-smoked brisket, dry-rubbed ribs, sides rooted in his grandmother's cooking. Opened 2026, already a local favorite.", "wait": "sells out by afternoon — go earlier in the day", "black_owned": True},
            {"name": "Potholder Cafe", "type": "Breakfast diner", "price": "$", "distance": "0.8mi", "note": "The Long Beach breakfast spot. Real portions, no frills, been there forever.", "wait": "expect a wait, no reservations — line moves but it moves slow on busy days", "black_owned": False},
            {"name": "Open Sesame", "type": "Lebanese", "price": "$$", "distance": "0.7mi", "note": "2nd Street staple — shawarma, hummus, pita. Different from the usual, genuinely good.", "wait": "usually moves fast", "black_owned": False},
            {"name": "Beachwood BBQ", "type": "BBQ", "price": "$$", "distance": "0.6mi", "note": "Local craft BBQ on 2nd. Good ribs and mac, good vibe, not a chain.", "wait": "can get a wait on weekends", "black_owned": False},
            {"name": "The Ordinarie", "type": "Bar / food", "price": "$$", "distance": "0.7mi", "note": "Good if the day rolls into evening — solid food, local crowd, low-key.", "wait": None, "black_owned": False},
        ],
        "drinks_nearby": [
            {"name": "Congregation Ale House", "type": "Craft beer bar", "price": "$$", "distance": "0.6mi", "note": "Long Beach's best tap list. 40+ drafts, real craft selection, good atmosphere on 2nd Street."},
            {"name": "Beachwood Blendery", "type": "Sour beer bar", "price": "$$", "distance": "0.8mi", "note": "Barrel-aged sours and wild ales. Very different, very good. Standing room, local crowd."},
            {"name": "The Ordinarie", "type": "Bar / food", "price": "$$", "distance": "0.7mi", "note": "Good wine and local beers, no attitude. Already in the food list — but honestly better as a drink spot."},
        ],
        "spots_nearby": [
            "Naples Island canals — 10min walk, walk the bridges at sunset, genuinely beautiful",
            "Belmont Pier — 0.5mi north, good sunset view from the end",
            "2nd Street strip — grab coffee or food without driving, walkable from the parking",
        ],
        "smoke_spots": [
            "Right at the dead end — no foot traffic, no one coming through, just the water in front of you",
            "Walk south along the waterline until the houses end — completely alone out there with a full view of the horizon",
            "The jetty stones just past the water's edge — sit, settle in, and watch the water move",
        ],
        "budget_per_person": 15,
    },
    "junipero": {
        "name": "Junipero Beach",
        "city": "Long Beach",
        "vibe": ["local", "low-key", "no tourists", "east side LB", "easy parking"],
        "parking": "Free street parking on Junipero Ave — usually available",
        "fire_pit": False,
        "notes": "The real Long Beach beach. No pier, no boardwalk circus, just the water and some locals. East side of LB, easy to get to, easy to find a quiet spot.",
        "food_nearby": [
            {"name": "Bake N Broil", "type": "Breakfast diner", "price": "$", "distance": "1.5mi", "note": "Long Beach institution on Atlantic. French toast, real portions, no frills"},
            {"name": "Panxa Cocina", "type": "Latin fusion", "price": "$$", "distance": "2mi", "note": "4th Street corridor, not standard — more refined, good cocktails, worth it"},
            {"name": "Beachwood BBQ", "type": "BBQ / craft beer", "price": "$$", "distance": "2mi", "note": "Local spot, good ribs, craft beer if that's the move"},
        ],
        "drinks_nearby": [
            {"name": "Congregation Ale House", "type": "Craft beer bar", "price": "$$", "distance": "1.5mi", "note": "Best tap list in Long Beach. Worth the short drive up 2nd Street."},
            {"name": "Beachwood BBQ", "type": "BBQ / craft beer", "price": "$$", "distance": "2mi", "note": "Food and drinks in one — solid pours alongside the ribs."},
            {"name": "Panxa Cocina", "type": "Cocktail bar / Latin fusion", "price": "$$", "distance": "2mi", "note": "Good cocktails, refined vibe. Worth it if the day rolls into evening."},
        ],
        "spots_nearby": [
            "2nd Street / Belmont Shore — 10min walk north, shops and food strip",
            "Naples Island canals — 15min walk, romantic canal neighborhood, weirdly beautiful",
            "Alamitos Bay — calm water on the bay side, completely different vibe from the ocean",
        ],
        "smoke_spots": [
            "Walk east past 54th Place — beach population drops off significantly",
            "The bike path heading toward Belmont Shores at dusk — less foot traffic",
            "Parking lot at the dead end of Junipero — usually empty, tucked away",
        ],
        "budget_per_person": 15,
    },
    "belmont_shore": {
        "name": "Belmont Shore",
        "city": "Long Beach",
        "vibe": ["walkable", "2nd Street", "food and beach", "local scene", "day to night"],
        "parking": "Street park off 2nd St side streets — free, just need to walk a couple blocks",
        "fire_pit": False,
        "notes": "Best of both worlds — actual beach plus a whole street of food and shops. 2nd Street is Long Beach's most walkable strip. Good for an all-day thing that flows from beach to dinner without driving.",
        "food_nearby": [
            {"name": "Potholder Cafe", "type": "Breakfast diner", "price": "$", "distance": "1mi", "note": "The Long Beach breakfast spot. Real portions, no frills, been there forever. Line moves fast."},
            {"name": "Open Sesame", "type": "Lebanese", "price": "$$", "distance": "0.3mi", "note": "2nd Street staple — shawarma, hummus, pita. Different from the usual, genuinely good."},
            {"name": "Beachwood BBQ", "type": "BBQ", "price": "$$", "distance": "0.5mi", "note": "Local craft BBQ on 2nd. Good ribs and mac, good vibe, not a chain."},
            {"name": "The Ordinarie", "type": "Bar / food", "price": "$$", "distance": "0.4mi", "note": "Good if the day rolls into evening — solid food, local crowd, low-key."},
        ],
        "drinks_nearby": [
            {"name": "Congregation Ale House", "type": "Craft beer bar", "price": "$$", "distance": "0.4mi", "note": "The 2nd Street anchor. 40+ craft taps, good energy, better-than-average bar food."},
            {"name": "Ballast Point Long Beach", "type": "Craft brewery", "price": "$$", "distance": "0.5mi", "note": "Waterfront views from the patio, solid rotating taps. Good for a golden hour drink."},
            {"name": "Beachwood Blendery", "type": "Sour / wild ales", "price": "$$", "distance": "0.6mi", "note": "Barrel-aged sours, standing room, local cult following. For something more interesting."},
        ],
        "spots_nearby": [
            "Naples Island — rent a gondola or just walk the canals, genuinely beautiful",
            "Belmont Pier — sunset from the end of the pier is the move",
            "2nd Street strip — window shop, grab coffee, no destination needed",
        ],
        "smoke_spots": [
            "East end of the beach past the crowds toward Junipero — thins out after dark",
            "Under the Belmont Pier south side — sheltered, usually clear at night",
            "Granada Beach just north of the pier — quieter pocket, less traffic",
        ],
        "budget_per_person": 18,
    },
    "zuma": {
        "name": "Zuma Beach",
        "city": "Malibu",
        "vibe": ["wide open", "less crowded", "good waves", "chill"],
        "parking": "$3–8/day (lot)",
        "fire_pit": False,
        "notes": "One of the longest beaches in LA. Less touristy than Santa Monica. Good for just existing.",
        "food_nearby": [
            {"name": "Cholada Thai Beach Cuisine", "type": "Thai", "price": "$", "distance": "0.5mi", "note": "Cash only, tiny, worth it"},
            {"name": "Reel Inn", "type": "Seafood / casual", "price": "$$", "distance": "2mi", "note": "Fish tacos on PCH, unpretentious"},
            {"name": "Vintage Grocers Malibu", "type": "Grab & go", "price": "$", "distance": "3mi", "note": "Good deli section, make your own beach snacks"},
        ],
        "drinks_nearby": [
            {"name": "Duke's Malibu", "type": "Beach bar / restaurant", "price": "$$$", "distance": "8mi south", "note": "Ocean-facing bar. Pricey but you're in Malibu — mai tais with a view. Go for drinks, not dinner."},
            {"name": "Moonshadows Malibu", "type": "Bar / lounge", "price": "$$$", "distance": "10mi south on PCH", "note": "Oceanfront deck, good cocktails. Sunset timing is everything here."},
        ],
        "spots_nearby": [
            "Point Dume State Preserve — cliff walk above the ocean, low foot traffic",
            "El Matador Beach — 10min north, rocky coves, feels hidden",
        ],
        "budget_per_person": 25,
    },
    "el_matador": {
        "name": "El Matador State Beach",
        "city": "Malibu",
        "vibe": ["hidden", "rocky", "scenic", "intimate", "less crowded"],
        "parking": "$8/day (small lot — get there early or it's full)",
        "fire_pit": False,
        "notes": "Sea caves, rock formations, feels like a secret. Hike down is short but steep. Worth it.",
        "food_nearby": [
            {"name": "Neptune's Net", "type": "Seafood shack", "price": "$$", "distance": "3mi", "note": "Classic PCH spot, clam chowder, fish and chips, cash-friendly"},
            {"name": "Trancas Market", "type": "Deli / grocery", "price": "$", "distance": "1mi", "note": "Grab sandwiches and snacks before heading down"},
        ],
        "drinks_nearby": [
            {"name": "Moonshadows Malibu", "type": "Bar / lounge", "price": "$$$", "distance": "4mi south", "note": "The closest good bar — oceanfront deck, solid cocktails, built for sunset."},
            {"name": "Duke's Malibu", "type": "Beach bar", "price": "$$$", "distance": "3mi south", "note": "Mai tais, ocean views. Touristy but earned its reputation."},
        ],
        "spots_nearby": [
            "Zuma Beach — 10min south if you want more space to spread out",
            "Leo Carrillo — 15min north, sea caves and tidepools",
        ],
        "budget_per_person": 20,
    },
    "dockweiler": {
        "name": "Dockweiler State Beach",
        "city": "Playa del Rey",
        "vibe": ["fire pits", "local", "sunsets", "laid back", "night vibes"],
        "parking": "$5–12/day",
        "fire_pit": True,
        "notes": "One of the few LA beaches with public fire pits. Planes from LAX fly overhead — loud but lowkey cool at night. Less tourist energy.",
        "food_nearby": [
            {"name": "Dulan's Soul Food Kitchen", "type": "Soul food", "price": "$", "distance": "4mi", "note": "Real food — fried chicken, oxtail, candied yams. Not tourist-y, not basic. Crenshaw institution."},
            {"name": "Hilltop Coffee + Kitchen", "type": "Brunch / coffee", "price": "$$", "distance": "5mi", "note": "Inglewood spot with a vibe. Good for a late morning start before heading to the sand."},
            {"name": "Bludso's BBQ", "type": "BBQ", "price": "$$", "distance": "6mi", "note": "Get it to go and bring it to the beach. Ribs, links, mac. Worth the detour."},
        ],
        "drinks_nearby": [
            {"name": "BYOB — fire pit legal", "type": "Bring your own", "price": "$", "distance": "right here", "note": "Dockweiler allows alcohol in the designated fire pit areas. Grab a bottle on the way and make it part of the fire."},
            {"name": "Naja's Place", "type": "Bar", "price": "$", "distance": "6mi south (Redondo)", "note": "70+ taps, no pretension, cash crowd. The real one if you want variety after the beach."},
            {"name": "King Harbor Brewing", "type": "Craft brewery", "price": "$$", "distance": "7mi south (Redondo)", "note": "Waterfront patio, good selection. Better if you're ending the day with a drive south."},
        ],
        "smoke_spots": [
            "Walk north past parking lot 3 — the beach thins out fast, no lifeguards, more space",
            "The grass strip between the lots and PCH — low foot traffic, good wind cover from the dunes",
            "South end near the jetty — far from the families, good view",
        ],
        "spots_nearby": [
            "Ballona Wetlands — bike path along the water, calm",
            "Manhattan Beach Pier — 10min south, cleaner vibe if you want to walk",
        ],
        "budget_per_person": 18,
    },
    "venice": {
        "name": "Venice Beach",
        "city": "Venice / LA",
        "vibe": ["energy", "people watching", "boardwalk", "weird and fun", "busy"],
        "parking": "$15–25/day (overpriced lots) — street parking in the neighborhoods saves money",
        "fire_pit": False,
        "notes": "Loud, chaotic, entertaining. Not for a quiet day but great if you want stimulation. Skate park, muscle beach, murals everywhere.",
        "food_nearby": [
            {"name": "Gjusta", "type": "Bakery / deli", "price": "$$", "distance": "0.5mi", "note": "Expensive but the sandwiches are legitimately great — split one"},
            {"name": "Tacos Por Favor", "type": "Tacos", "price": "$", "distance": "1mi", "note": "Cheap, fast, legit — Santa Monica adjacent"},
            {"name": "Abbot Kinney food trucks", "type": "Various", "price": "$–$$", "distance": "0.3mi", "note": "Hit or miss by day, usually something good on weekends"},
        ],
        "drinks_nearby": [
            {"name": "The Brig", "type": "Bar", "price": "$$", "distance": "0.3mi (Abbot Kinney)", "note": "Legit Venice bar. Low-lit, no gimmick, actual neighborhood crowd. Not a tourist spot."},
            {"name": "Townhouse & Del Monte Speakeasy", "type": "Bar / speakeasy", "price": "$$", "distance": "0.5mi", "note": "Venice institution. Upstairs is a dive bar, downstairs is a speakeasy basement. Cheap drinks, right vibe."},
            {"name": "West Washington Ale House", "type": "Craft beer bar", "price": "$$", "distance": "0.8mi", "note": "40+ taps, low-key, walkable from the beach strip."},
        ],
        "spots_nearby": [
            "Abbot Kinney Blvd — walkable, good window shopping and coffee",
            "Venice Canals — 5min walk from the beach, quiet residential canals, completely different vibe",
            "Santa Monica Pier — 2mi north, tourist-y but iconic",
        ],
        "budget_per_person": 22,
    },
    "leo_carrillo": {
        "name": "Leo Carrillo State Park",
        "city": "Malibu (north)",
        "vibe": ["sea caves", "tidepools", "camping", "nature", "remote feeling"],
        "parking": "$12/day",
        "fire_pit": False,
        "notes": "Sea caves you can actually walk into. Tidepools. Feels far from the city even though it's not. Good for an adventure day.",
        "food_nearby": [
            {"name": "Neptune's Net", "type": "Seafood shack", "price": "$$", "distance": "1mi", "note": "Right on PCH, motorcycles and beach people, good vibe"},
            {"name": "Trancas Market", "type": "Deli", "price": "$", "distance": "8mi", "note": "Stock up before you get there — nothing closer"},
        ],
        "drinks_nearby": [
            {"name": "Neptune's Net", "type": "Bar / seafood shack", "price": "$$", "distance": "1mi", "note": "Cold beer at the window. PCH biker crowd, good energy. More of a beer-with-chowder situation."},
            {"name": "Stock up before you go", "type": "Tip", "price": "$", "distance": "Malibu on the way", "note": "There's genuinely not much out here. Grab wine or canned drinks in Malibu before heading up PCH."},
        ],
        "spots_nearby": [
            "Nicholas Flat Trail — hike above the park with ocean views",
            "El Matador — 15min south for a different kind of cove beach",
        ],
        "budget_per_person": 20,
    },
    "manhattan": {
        "name": "Manhattan Beach",
        "city": "Manhattan Beach",
        "vibe": ["clean", "walkable", "pier", "mellow", "local feel"],
        "parking": "Street parking is free but competitive — aim for neighborhoods east of the strand",
        "fire_pit": False,
        "notes": "Quieter than Venice, cleaner than Santa Monica. Good pier. Nice for a walk and food combo.",
        "food_nearby": [
            {"name": "Fishing with Dynamite", "type": "Seafood", "price": "$$$", "distance": "0.2mi", "note": "Splurge spot — skip if budget is tight"},
            {"name": "Uncle Bill's Pancake House", "type": "Breakfast", "price": "$", "distance": "0.3mi", "note": "Classic diner, good prices, go before the beach"},
            {"name": "Hermosa Beach taco trucks", "type": "Tacos", "price": "$", "distance": "1mi south", "note": "Walk or drive down to Hermosa for cheaper eats"},
        ],
        "drinks_nearby": [
            {"name": "Manhattan Beach Brewing Co.", "type": "Craft brewery", "price": "$$", "distance": "0.4mi", "note": "Walking distance. Local brewery, patio seating, good rotating taps."},
            {"name": "Strand House", "type": "Rooftop bar", "price": "$$$", "distance": "0.2mi", "note": "Pricey but the rooftop view of the strand at golden hour is worth one drink. Make it count."},
        ],
        "spots_nearby": [
            "The Strand — paved path from Manhattan to Redondo, good for a walk",
            "Hermosa Beach — 1mi south, more relaxed, cheaper food scene",
        ],
        "budget_per_person": 20,
    },
}

VIBES = {
    "quiet":    ["zuma", "el_matador", "leo_carrillo"],
    "hidden":   ["el_matador", "leo_carrillo"],
    "fire pit": ["dockweiler"],
    "fire":     ["dockweiler"],
    "energy":   ["venice"],
    "food":     ["venice", "manhattan", "dockweiler"],
    "nature":   ["leo_carrillo", "el_matador", "zuma"],
    "sunset":   ["dockweiler", "zuma", "el_matador"],
    "cheap":    ["dockweiler", "zuma", "manhattan"],
    "caves":    ["el_matador", "leo_carrillo"],
    "local":    ["dockweiler", "manhattan"],
}


def print_beach(key):
    b = BEACHES[key]
    print(f"\n{'='*55}")
    print(f"  {b['name']}  —  {b['city']}")
    print(f"{'='*55}")
    print(f"  Vibe:     {', '.join(b['vibe'])}")
    print(f"  Parking:  {b['parking']}")
    print(f"  Fire pit: {'yes' if b['fire_pit'] else 'no'}")
    print(f"  Budget:   ~${b['budget_per_person']}/person (food + parking)")
    print(f"\n  {b['notes']}")

    print(f"\n  FOOD NEARBY")
    for f in b["food_nearby"]:
        print(f"    {f['price']} {f['name']} ({f['type']}) — {f['distance']}")
        print(f"       {f['note']}")

    print(f"\n  DRINKS NEARBY")
    for d in b.get("drinks_nearby", []):
        print(f"    {d['price']} {d['name']} ({d['type']}) — {d['distance']}")
        print(f"       {d['note']}")

    print(f"\n  SPOTS / THINGS NEARBY")
    for s in b["spots_nearby"]:
        print(f"    • {s}")
    print()


def list_all():
    print("\nSoCal beaches in the database:\n")
    for key, b in BEACHES.items():
        fp = " [fire pits]" if b["fire_pit"] else ""
        print(f"  {key:<15} {b['name']}, {b['city']}{fp}")
        print(f"               ~${b['budget_per_person']}/person  |  {', '.join(b['vibe'][:3])}")
    print(f"\nUsage:  python3 beach_day.py <beach_name>")
    print(f"        python3 beach_day.py --vibe quiet")
    print(f"        python3 beach_day.py --budget 20\n")


def main():
    args = sys.argv[1:]

    if not args:
        list_all()
        return

    if args[0] == "--vibe" and len(args) > 1:
        vibe = " ".join(args[1:]).lower()
        matches = VIBES.get(vibe, [])
        if not matches:
            print(f"\nNo matches for vibe '{vibe}'. Try: {', '.join(VIBES.keys())}\n")
        else:
            print(f"\nBeaches matching '{vibe}':")
            for key in matches:
                print_beach(key)
        return

    if args[0] == "--budget" and len(args) > 1:
        try:
            cap = int(args[1])
        except ValueError:
            print("Budget should be a number, e.g. --budget 20")
            return
        matches = [k for k, b in BEACHES.items() if b["budget_per_person"] <= cap]
        if not matches:
            print(f"\nNothing under ${cap}/person. Lowest is ${min(b['budget_per_person'] for b in BEACHES.values())}.\n")
        else:
            print(f"\nBeaches under ${cap}/person:")
            for key in matches:
                print_beach(key)
        return

    key = args[0].lower().replace("-", "_")
    if key not in BEACHES:
        print(f"\nUnknown beach '{key}'. Available: {', '.join(BEACHES.keys())}\n")
        return
    print_beach(key)


if __name__ == "__main__":
    main()
