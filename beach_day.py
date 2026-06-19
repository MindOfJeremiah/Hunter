# beach_day.py — cross-references SoCal beaches with nearby food, spots, and budget info.
# Usage:
#   python3 beach_day.py                  → lists all beaches
#   python3 beach_day.py zuma             → full breakdown for Zuma
#   python3 beach_day.py --vibe quiet     → beaches matching a vibe
#   python3 beach_day.py --budget 20      → beaches + food you can do under $20/person

import sys

BEACHES = {
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
            {"name": "In-N-Out (Lincoln Blvd)", "type": "Burgers", "price": "$", "distance": "2mi", "note": "Double-double is $6, you know what it is"},
            {"name": "Tito's Tacos", "type": "Tacos", "price": "$", "distance": "3mi", "note": "Westside institution, crispy tacos, always a line but moves fast"},
            {"name": "Whole Foods (Playa Vista)", "type": "Grab & go", "price": "$$", "distance": "2mi", "note": "Hot bar by weight if you want to sit down and eat real food"},
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
            {"name": "Tacos Por Favor", "type": "Tacos", "price": "$", "distance": "1mi", "note": "Cheap, fast, legit Mexican — Santa Monica adjacent"},
            {"name": "La Cabaña", "type": "Mexican", "price": "$", "distance": "1mi", "note": "Margaritas and chips, solid prices for the area"},
            {"name": "Abbot Kinney food trucks", "type": "Various", "price": "$–$$", "distance": "0.3mi", "note": "Hit or miss by day, usually something good on weekends"},
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

    key = args[0].lower().replace(" ", "_").replace("-", "_")
    if key in BEACHES:
        print_beach(key)
    else:
        print(f"\nBeach '{args[0]}' not in database. Known beaches:")
        list_all()


if __name__ == "__main__":
    main()
