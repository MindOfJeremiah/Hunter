# make_plan.py — generates a cute shareable beach day plan page for someone to open.
# Usage:
#   python3 make_plan.py dockweiler
#   python3 make_plan.py dockweiler --for Kelli
#   python3 make_plan.py dockweiler --for Kelli --note "just trust me on this one"

import sys
import os
import webbrowser
from beach_day import BEACHES

PRICE_LABEL = {"$": "cheap", "$$": "mid", "$$$": "splurge"}

def generate(beach_key, for_name=None, note=None):
    b = BEACHES[beach_key]

    greeting = f"a day for {for_name} 🤍" if for_name else "beach day plan"
    note_html = f'<p class="note">"{note}"</p>' if note else ""
    fire_badge = '<span class="badge fire">🔥 fire pits</span>' if b["fire_pit"] else ""

    food_items = ""
    for f in b["food_nearby"]:
        label = PRICE_LABEL.get(f["price"], f["price"])
        food_items += f"""
        <div class="card">
          <div class="card-top">
            <span class="name">{f['name']}</span>
            <span class="tag">{label}</span>
          </div>
          <div class="sub">{f['type']} · {f['distance']}</div>
          <div class="detail">{f['note']}</div>
        </div>"""

    spot_items = ""
    for s in b["spots_nearby"]:
        spot_items += f'<li>{s}</li>'

    vibes = " · ".join(b["vibe"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{b['name']}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #fdf6f0;
      color: #2d2d2d;
      padding: 24px 16px 48px;
      max-width: 480px;
      margin: 0 auto;
    }}
    .greeting {{
      font-size: 13px;
      color: #999;
      text-transform: lowercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }}
    h1 {{
      font-size: 28px;
      font-weight: 700;
      line-height: 1.2;
      margin-bottom: 4px;
    }}
    .city {{
      font-size: 14px;
      color: #888;
      margin-bottom: 12px;
    }}
    .note {{
      font-style: italic;
      color: #b07a5a;
      font-size: 14px;
      margin: 10px 0 16px;
    }}
    .badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 16px;
    }}
    .badge {{
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 99px;
      background: #ede8e3;
      color: #555;
    }}
    .badge.fire {{ background: #fde8d8; color: #c0622a; }}
    .badge.budget {{ background: #e8f0e8; color: #3a6b3a; }}
    .vibe-line {{
      font-size: 13px;
      color: #888;
      margin-bottom: 20px;
      font-style: italic;
    }}
    .blurb {{
      font-size: 15px;
      line-height: 1.6;
      color: #444;
      margin-bottom: 28px;
      padding: 16px;
      background: #fff;
      border-radius: 12px;
      border-left: 3px solid #e8c9b0;
    }}
    h2 {{
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #aaa;
      margin-bottom: 12px;
    }}
    .section {{ margin-bottom: 28px; }}
    .card {{
      background: #fff;
      border-radius: 12px;
      padding: 14px 16px;
      margin-bottom: 10px;
    }}
    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 3px;
    }}
    .card .name {{ font-weight: 600; font-size: 15px; }}
    .card .tag {{
      font-size: 11px;
      color: #999;
      background: #f2f2f2;
      padding: 2px 8px;
      border-radius: 99px;
    }}
    .card .sub {{ font-size: 12px; color: #aaa; margin-bottom: 4px; }}
    .card .detail {{ font-size: 13px; color: #666; }}
    .spots-list {{
      list-style: none;
      background: #fff;
      border-radius: 12px;
      overflow: hidden;
    }}
    .spots-list li {{
      padding: 13px 16px;
      font-size: 14px;
      color: #444;
      border-bottom: 1px solid #f5f5f5;
      line-height: 1.4;
    }}
    .spots-list li:last-child {{ border-bottom: none; }}
    .parking-box {{
      background: #fff;
      border-radius: 12px;
      padding: 14px 16px;
      font-size: 14px;
      color: #555;
    }}
    .footer {{
      margin-top: 40px;
      text-align: center;
      font-size: 12px;
      color: #ccc;
    }}
  </style>
</head>
<body>
  <div class="greeting">{greeting}</div>
  <h1>{b['name']}</h1>
  <div class="city">{b['city']}</div>
  {note_html}
  <div class="badges">
    {fire_badge}
    <span class="badge budget">~${b['budget_per_person']}/person</span>
  </div>
  <div class="vibe-line">{vibes}</div>

  <div class="blurb">{b['notes']}</div>

  <div class="section">
    <h2>Food nearby</h2>
    {food_items}
  </div>

  <div class="section">
    <h2>Also worth knowing</h2>
    <ul class="spots-list">
      {spot_items}
    </ul>
  </div>

  <div class="section">
    <h2>Parking</h2>
    <div class="parking-box">{b['parking']}</div>
  </div>

  <div class="footer">made with love</div>
</body>
</html>"""
    return html


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 make_plan.py <beach> [--for Name] [--note 'message']")
        print("       python3 make_plan.py dockweiler --for Kelli --note 'just trust me'")
        return

    beach_key = args[0].lower().replace("-", "_")
    if beach_key not in BEACHES:
        from beach_day import BEACHES as B
        print(f"Unknown beach. Try: {', '.join(B.keys())}")
        return

    for_name = None
    note = None
    i = 1
    while i < len(args):
        if args[i] == "--for" and i + 1 < len(args):
            for_name = args[i + 1]; i += 2
        elif args[i] == "--note" and i + 1 < len(args):
            note = args[i + 1]; i += 2
        else:
            i += 1

    html = generate(beach_key, for_name, note)
    fname = f"plan_{beach_key}.html"
    with open(fname, "w") as f:
        f.write(html)

    print(f"Saved → {fname}")
    webbrowser.open(f"file://{os.path.abspath(fname)}")


if __name__ == "__main__":
    main()
