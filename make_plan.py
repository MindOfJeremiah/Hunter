# make_plan.py — generates a beach day plan page with an interactive beach picker.
# Usage:
#   python3 make_plan.py belmont_shore --for Kelli --note "you deserve a beautiful day"

import sys, os, webbrowser, json
from beach_day import BEACHES

# Long Beach beaches shown first, rest after
BEACH_ORDER = ["seal_beach", "belmont_shore", "junipero", "dockweiler", "el_matador", "zuma", "leo_carrillo", "manhattan", "venice"]

def generate(default_key, for_name=None, note=None):
    name_display = for_name if for_name else "today"
    note_html = f'<p class="intention-note">&#x201C;{note}&#x201D;</p>' if note else ""

    ordered = [k for k in BEACH_ORDER if k in BEACHES] + [k for k in BEACHES if k not in BEACH_ORDER]
    beaches_js = json.dumps({k: BEACHES[k] for k in ordered}, ensure_ascii=False)

    picker_cards = ""
    for key in ordered:
        b = BEACHES[key]
        fp = '<span class="bp-fire">🔥</span>' if b["fire_pit"] else ""
        vibes = " · ".join(b["vibe"][:2])
        lb_tag = ' <span class="bp-local">local</span>' if key in ("seal_beach", "belmont_shore", "junipero") else ""
        picker_cards += f"""
        <div class="bp-card" data-key="{key}" onclick="selectBeach('{key}')">
          <div class="bp-top">{fp}<span class="bp-name">{b['name']}</span>{lb_tag}</div>
          <div class="bp-city">{b['city']}</div>
          <div class="bp-vibe">{vibes}</div>
          <div class="bp-budget">~${b['budget_per_person']}/person</div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>a day for {name_display}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garant:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=Sacramento&family=Lato:wght@300;400&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --forest:      #1A3A2F;
      --forest-mid:  #2D5445;
      --forest-light:#4A7A68;
      --gold:        #C9973A;
      --gold-light:  #E8C97A;
      --blush:       #F0C8D4;
      --rose:        #D95F7A;
      --cream:       #F7F2E8;
      --warm-white:  #FDFAF5;
      --ink:         #1C1410;
      --muted:       #9A8878;
      --divider:     #E5D8C8;
    }}

    body {{
      font-family: 'Lato', -apple-system, sans-serif;
      font-weight: 300;
      background: var(--cream);
      color: var(--ink);
      min-height: 100vh;
      overflow-x: hidden;
    }}

    /* ── HERO ── */
    .hero {{
      min-height: 100svh;
      background: var(--forest);
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 80px 32px 120px;
      overflow: hidden;
    }}

    .hero::before {{
      content: '';
      position: absolute;
      inset: 0;
      background:
        radial-gradient(ellipse 90% 60% at 10% 100%, rgba(217,95,122,0.38) 0%, transparent 55%),
        radial-gradient(ellipse 55% 45% at 90% 5%,  rgba(201,151,58,0.32) 0%, transparent 50%),
        radial-gradient(ellipse 40% 30% at 50% 2%,  rgba(240,200,212,0.12) 0%, transparent 45%);
      pointer-events: none;
    }}

    /* SVG flower decorations */
    .hero-flower {{
      position: absolute;
      pointer-events: none;
      opacity: 0.18;
    }}
    .hf1 {{ width: 110px; top: 6%; left: -18px; transform: rotate(-20deg); }}
    .hf2 {{ width: 80px;  top: 4%; right: -10px; transform: rotate(30deg); opacity: 0.14; }}
    .hf3 {{ width: 60px;  bottom: 12%; left: 4%; transform: rotate(15deg); opacity: 0.12; }}
    .hf4 {{ width: 90px;  bottom: 8%; right: -8px; transform: rotate(-10deg); opacity: 0.15; }}

    /* Stars */
    .star {{
      position: absolute;
      color: var(--gold);
      animation: twinkle ease-in-out infinite;
      pointer-events: none;
    }}
    @keyframes twinkle {{
      0%,100% {{ opacity: 0.18; transform: scale(0.85); }}
      50%      {{ opacity: 0.65; transform: scale(1.1); }}
    }}

    /* Petal fall */
    .petals {{ position: absolute; inset: 0; pointer-events: none; overflow: hidden; }}
    .petal {{
      position: absolute;
      top: -20px;
      background: rgba(240,200,212,0.65);
      border-radius: 50% 0 50% 0;
      animation: petalfall linear infinite;
    }}
    .petal:nth-child(1) {{ left:7%;  width:7px;  height:13px; animation-duration:10s; animation-delay:0s; }}
    .petal:nth-child(2) {{ left:19%; width:10px; height:18px; animation-duration:14s; animation-delay:-3s;  background:rgba(217,95,122,0.45); }}
    .petal:nth-child(3) {{ left:36%; width:6px;  height:11px; animation-duration:11s; animation-delay:-7s; }}
    .petal:nth-child(4) {{ left:52%; width:9px;  height:16px; animation-duration:16s; animation-delay:-2s;  background:rgba(201,151,58,0.35); border-radius:0 50% 0 50%; }}
    .petal:nth-child(5) {{ left:67%; width:8px;  height:14px; animation-duration:10s; animation-delay:-5s; }}
    .petal:nth-child(6) {{ left:80%; width:11px; height:19px; animation-duration:15s; animation-delay:-9s;  background:rgba(217,95,122,0.38); }}
    .petal:nth-child(7) {{ left:92%; width:7px;  height:12px; animation-duration:12s; animation-delay:-1s; }}
    .petal:nth-child(8) {{ left:45%; width:9px;  height:15px; animation-duration:17s; animation-delay:-6s;  background:rgba(240,200,212,0.5); border-radius:0 50% 0 50%; }}
    @keyframes petalfall {{
      0%   {{ transform:translateY(-20px) rotate(0deg);   opacity:0; }}
      8%   {{ opacity:0.8; }}
      88%  {{ opacity:0.25; }}
      100% {{ transform:translateY(105vh) rotate(700deg); opacity:0; }}
    }}

    .hero-content {{
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}

    .hero-label {{
      font-size: 10px;
      letter-spacing: 0.35em;
      text-transform: uppercase;
      color: var(--gold-light);
      margin-bottom: 28px;
      font-weight: 300;
    }}

    .hero-for {{
      font-family: 'Lato', sans-serif;
      font-weight: 300;
      font-size: 13px;
      letter-spacing: 0.12em;
      color: rgba(255,255,255,0.45);
      margin-bottom: 2px;
    }}

    .hero-name {{
      font-family: 'Sacramento', cursive;
      font-size: clamp(72px, 18vw, 108px);
      color: #fff;
      line-height: 1;
      margin-bottom: 28px;
      text-shadow: 0 6px 40px rgba(217,95,122,0.55), 0 2px 8px rgba(0,0,0,0.3);
    }}

    .hero-beach-name {{
      font-family: 'Cormorant Garant', serif;
      font-style: italic;
      font-weight: 300;
      font-size: clamp(22px, 5vw, 32px);
      color: rgba(255,255,255,0.82);
      letter-spacing: 0.04em;
      margin-bottom: 6px;
      transition: opacity 0.25s;
    }}

    .hero-city {{
      font-size: 11px;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: rgba(255,255,255,0.35);
      margin-bottom: 22px;
    }}

    .hero-vibes {{
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      justify-content: center;
    }}

    .vibe-chip {{
      font-size: 11px;
      font-weight: 300;
      padding: 4px 13px;
      border: 1px solid rgba(255,255,255,0.18);
      color: rgba(255,255,255,0.6);
      letter-spacing: 0.04em;
    }}

    .fp-chip {{
      font-size: 11px;
      font-weight: 300;
      padding: 4px 13px;
      border: 1px solid rgba(201,151,58,0.38);
      color: var(--gold-light);
    }}

    .scroll-hint {{
      position: absolute;
      bottom: 36px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      animation: floatdown 2.2s ease-in-out infinite;
    }}
    .scroll-hint span {{
      font-size: 10px;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: rgba(255,255,255,0.38);
      font-weight: 300;
    }}
    .scroll-hint::after {{
      content: '';
      width: 1px;
      height: 40px;
      background: linear-gradient(to bottom, rgba(255,255,255,0.35), transparent);
    }}
    @keyframes floatdown {{
      0%,100% {{ transform: translateX(-50%) translateY(0); }}
      50%      {{ transform: translateX(-50%) translateY(8px); }}
    }}

    /* ── BEACH PICKER (dark, continues hero) ── */
    .picker-wrap {{
      background: var(--forest);
      padding: 30px 0 32px;
      border-top: 1px solid rgba(255,255,255,0.06);
    }}

    .picker-heading {{
      font-family: 'Cormorant Garant', serif;
      font-style: italic;
      font-weight: 300;
      font-size: 20px;
      color: rgba(255,255,255,0.6);
      padding: 0 24px;
      margin-bottom: 14px;
    }}

    .picker-scroll {{
      display: flex;
      gap: 10px;
      overflow-x: auto;
      padding: 2px 24px 6px;
      scroll-snap-type: x mandatory;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }}
    .picker-scroll::-webkit-scrollbar {{ display: none; }}

    .bp-card {{
      flex-shrink: 0;
      width: 155px;
      background: rgba(255,255,255,0.06);
      border-radius: 4px;
      padding: 14px 16px;
      border: 1px solid rgba(255,255,255,0.08);
      cursor: pointer;
      scroll-snap-align: start;
      transition: all 0.2s;
      user-select: none;
    }}
    .bp-card:active {{ transform: scale(0.97); }}
    .bp-card.selected {{
      background: rgba(255,255,255,0.13);
      border-color: rgba(240,200,212,0.45);
    }}

    .bp-top {{ display:flex; align-items:center; gap:4px; margin-bottom:3px; }}
    .bp-name {{
      font-family: 'Cormorant Garant', serif;
      font-weight: 400;
      font-size: 15px;
      color: rgba(255,255,255,0.82);
      line-height: 1.2;
    }}
    .bp-card.selected .bp-name {{ color: #fff; }}
    .bp-fire {{ font-size: 11px; }}
    .bp-local {{
      font-size: 9px;
      padding: 1px 6px;
      background: rgba(201,151,58,0.2);
      color: var(--gold-light);
      border: 1px solid rgba(201,151,58,0.28);
      margin-left: 3px;
    }}
    .bp-city  {{ font-size:11px; color:rgba(255,255,255,0.3); letter-spacing:0.06em; margin-bottom:5px; }}
    .bp-vibe  {{ font-size:11px; color:rgba(255,255,255,0.42); line-height:1.4; margin-bottom:6px; }}
    .bp-budget {{ font-size:11px; color:var(--gold-light); opacity:0.75; }}

    /* ── MAIN CONTENT ── */
    .main-content {{ background: var(--cream); padding-bottom: 80px; }}

    .content-inner {{
      max-width: 600px;
      margin: 0 auto;
      padding: 0 24px;
    }}

    /* Dividers */
    .divider {{
      display: flex;
      align-items: center;
      gap: 14px;
      margin: 40px 0 26px;
    }}
    .divider-line {{ flex:1; height:1px; background:var(--divider); }}
    .divider-mark {{ font-size:11px; color:var(--gold); opacity:0.7; }}

    /* Section headings */
    .section-title {{
      font-family: 'Cormorant Garant', serif;
      font-style: italic;
      font-weight: 300;
      font-size: 30px;
      color: var(--forest);
      margin-bottom: 18px;
      line-height: 1.15;
    }}

    /* Intention / blurb */
    .intention {{
      background: var(--warm-white);
      border-left: 3px solid var(--rose);
      padding: 26px 24px;
      margin-top: 38px;
    }}

    .intention-note {{
      font-family: 'Cormorant Garant', serif;
      font-style: italic;
      font-weight: 300;
      font-size: 21px;
      color: var(--forest);
      line-height: 1.6;
      margin-bottom: 14px;
    }}

    .beach-blurb {{
      font-size: 15px;
      color: #5A4A3A;
      line-height: 1.78;
      font-weight: 300;
      transition: opacity 0.2s;
    }}

    /* Meetup */
    .meetup {{
      margin-top: 14px;
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 18px 22px;
      background: var(--forest);
    }}

    .meetup-icon {{ font-size: 20px; flex-shrink: 0; }}

    .meetup-label {{
      font-size: 9px;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: rgba(255,255,255,0.35);
      margin-bottom: 4px;
    }}

    .meetup-time {{
      font-family: 'Cormorant Garant', serif;
      font-style: italic;
      font-size: 24px;
      font-weight: 300;
      color: rgba(255,255,255,0.88);
      border: none;
      background: none;
      outline: none;
      width: 100%;
      padding: 0;
    }}
    .meetup-time::placeholder {{ color: rgba(255,255,255,0.22); }}

    /* Pack list */
    .pack-list {{ list-style: none; display: flex; flex-direction: column; gap: 5px; }}

    .pack-item {{
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 14px 16px;
      background: var(--warm-white);
      cursor: pointer;
      transition: all 0.18s;
      font-size: 14px;
      font-weight: 300;
      color: #4A3A2A;
      user-select: none;
      border: 1px solid transparent;
      border-radius: 2px;
    }}

    .pack-item.checked {{
      background: rgba(45,84,69,0.07);
      border-color: rgba(45,84,69,0.13);
    }}
    .pack-item.checked span:last-child {{
      text-decoration: line-through;
      color: var(--muted);
    }}

    .check-box {{
      width: 20px;
      height: 20px;
      border-radius: 50%;
      border: 1.5px solid #D8C8B8;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.18s;
      font-size: 11px;
    }}
    .pack-item.checked .check-box {{
      background: var(--forest-mid);
      border-color: var(--forest-mid);
      color: #fff;
    }}
    .pack-item.checked .check-box::after {{ content: '✓'; }}

    /* Food — editorial list */
    .food-list {{
      border: 1px solid var(--divider);
      border-radius: 2px;
      overflow: hidden;
    }}

    .food-card {{
      background: var(--warm-white);
      padding: 18px 20px;
      cursor: pointer;
      transition: background 0.18s;
      border-left: 3px solid transparent;
      border-bottom: 1px solid var(--divider);
    }}
    .food-card:last-child {{ border-bottom: none; }}
    .food-card:active {{ background: #F5EEE4; }}
    .food-card.picked {{
      background: rgba(26,58,47,0.05);
      border-left-color: var(--forest-mid);
    }}

    .food-top {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 3px;
    }}

    .food-name {{
      font-family: 'Cormorant Garant', serif;
      font-weight: 400;
      font-size: 20px;
      color: var(--ink);
      flex: 1;
      line-height: 1.2;
    }}
    .food-card.picked .food-name {{ color: var(--forest); }}

    .price-tag {{
      font-size: 11px;
      color: var(--muted);
      font-weight: 300;
      margin-left: 10px;
    }}

    .food-meta {{
      font-size: 12px;
      color: var(--muted);
      letter-spacing: 0.03em;
      margin-bottom: 6px;
    }}

    .food-note {{
      font-size: 13px;
      color: #6A5848;
      line-height: 1.55;
      font-weight: 300;
    }}

    .pick-label   {{ font-size:12px; color:#C8B8A8; margin-top:9px; font-style:italic; }}
    .picked-label {{ font-size:12px; color:var(--forest-mid); font-style:italic; margin-top:9px; display:none; }}
    .food-card.picked .pick-label   {{ display:none; }}
    .food-card.picked .picked-label {{ display:block; }}

    /* Spot items */
    .spot-item {{
      display: flex;
      align-items: flex-start;
      gap: 14px;
      padding: 14px 16px;
      background: var(--warm-white);
      border-radius: 2px;
      margin-bottom: 5px;
      cursor: pointer;
      transition: all 0.18s;
      font-size: 14px;
      font-weight: 300;
      color: #4A3A2A;
      line-height: 1.55;
      user-select: none;
      border: 1px solid transparent;
    }}
    .spot-item.done {{
      background: rgba(45,84,69,0.07);
      border-color: rgba(45,84,69,0.13);
    }}
    .spot-item.done span:last-child {{
      text-decoration: line-through;
      color: var(--muted);
    }}
    .spot-item .check-box {{ margin-top: 2px; flex-shrink: 0; }}
    .spot-item.done .check-box {{ background:var(--forest-mid); border-color:var(--forest-mid); color:#fff; }}
    .spot-item.done .check-box::after {{ content:'✓'; }}

    /* Parking */
    .parking-card {{
      padding: 20px 22px;
      background: var(--warm-white);
      border-left: 3px solid var(--gold);
      font-size: 14px;
      font-weight: 300;
      color: #5A4A3A;
      line-height: 1.68;
      border-radius: 2px;
    }}

    /* Golden hour — cinematic */
    .golden {{
      background: #0B1A12;
      padding: 52px 32px;
      position: relative;
      overflow: hidden;
      text-align: center;
      border-radius: 2px;
    }}

    .golden::before {{
      content: '';
      position: absolute;
      inset: 0;
      background:
        radial-gradient(ellipse 70% 55% at 50% 105%, rgba(217,95,122,0.32) 0%, transparent 55%),
        radial-gradient(ellipse 45% 40% at 85% 15%,  rgba(201,151,58,0.22) 0%, transparent 50%),
        radial-gradient(ellipse 35% 30% at 15% 20%,  rgba(201,151,58,0.16) 0%, transparent 50%);
      pointer-events: none;
    }}

    .g-star {{
      position: absolute;
      color: rgba(232,201,122,0.55);
      animation: twinkle ease-in-out infinite;
      pointer-events: none;
    }}

    .golden-inner {{ position: relative; z-index: 1; }}

    .golden-script {{
      font-family: 'Sacramento', cursive;
      font-size: clamp(44px, 12vw, 64px);
      color: var(--gold-light);
      line-height: 1;
      margin-bottom: 22px;
      text-shadow: 0 4px 24px rgba(201,151,58,0.45);
    }}

    .golden-text {{
      font-family: 'Cormorant Garant', serif;
      font-style: italic;
      font-weight: 300;
      font-size: clamp(17px, 4vw, 22px);
      color: rgba(255,255,255,0.82);
      line-height: 1.7;
      max-width: 380px;
      margin: 0 auto;
    }}

    /* Notes */
    .notes-area {{
      width: 100%;
      min-height: 130px;
      background: var(--warm-white);
      border: 1px solid var(--divider);
      border-radius: 2px;
      padding: 18px 18px;
      font-family: 'Lato', sans-serif;
      font-weight: 300;
      font-size: 14px;
      color: var(--ink);
      resize: vertical;
      outline: none;
      transition: border-color 0.2s;
      line-height: 1.78;
    }}
    .notes-area:focus {{ border-color: rgba(26,58,47,0.28); }}
    .notes-area::placeholder {{ color: #C4B4A4; }}

    /* Footer */
    .footer {{
      text-align: center;
      padding: 52px 20px 32px;
      color: #B8A898;
      font-size: 11px;
      font-weight: 300;
      letter-spacing: 0.12em;
    }}
    .footer-line {{ width: 48px; height: 1px; background:var(--divider); margin:0 auto 18px; }}
  </style>
</head>
<body>

<!-- HERO -->
<div class="hero">

  <!-- Decorative SVG flowers -->
  <svg class="hero-flower hf1" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(60,60)">
      <ellipse rx="10" ry="28" fill="rgba(240,200,212,0.7)" transform="rotate(0)"/>
      <ellipse rx="10" ry="28" fill="rgba(240,200,212,0.7)" transform="rotate(45)"/>
      <ellipse rx="10" ry="28" fill="rgba(217,95,122,0.6)"  transform="rotate(90)"/>
      <ellipse rx="10" ry="28" fill="rgba(217,95,122,0.6)"  transform="rotate(135)"/>
      <circle r="12" fill="rgba(201,151,58,0.8)"/>
      <circle r="5"  fill="rgba(255,230,150,0.9)"/>
    </g>
  </svg>

  <svg class="hero-flower hf2" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(60,60)">
      <ellipse rx="9" ry="26" fill="rgba(240,200,212,0.65)" transform="rotate(30)"/>
      <ellipse rx="9" ry="26" fill="rgba(217,95,122,0.55)"  transform="rotate(90)"/>
      <ellipse rx="9" ry="26" fill="rgba(240,200,212,0.65)" transform="rotate(150)"/>
      <ellipse rx="9" ry="26" fill="rgba(217,95,122,0.55)"  transform="rotate(210)"/>
      <ellipse rx="9" ry="26" fill="rgba(240,200,212,0.65)" transform="rotate(270)"/>
      <ellipse rx="9" ry="26" fill="rgba(217,95,122,0.55)"  transform="rotate(330)"/>
      <circle r="11" fill="rgba(201,151,58,0.75)"/>
      <circle r="4"  fill="rgba(255,230,150,0.9)"/>
    </g>
  </svg>

  <svg class="hero-flower hf3" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(60,60)">
      <ellipse rx="8" ry="22" fill="rgba(240,200,212,0.6)" transform="rotate(0)"/>
      <ellipse rx="8" ry="22" fill="rgba(217,95,122,0.5)"  transform="rotate(72)"/>
      <ellipse rx="8" ry="22" fill="rgba(240,200,212,0.6)" transform="rotate(144)"/>
      <ellipse rx="8" ry="22" fill="rgba(217,95,122,0.5)"  transform="rotate(216)"/>
      <ellipse rx="8" ry="22" fill="rgba(240,200,212,0.6)" transform="rotate(288)"/>
      <circle r="10" fill="rgba(201,151,58,0.7)"/>
    </g>
  </svg>

  <svg class="hero-flower hf4" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(60,60)">
      <ellipse rx="10" ry="28" fill="rgba(240,200,212,0.65)" transform="rotate(0)"/>
      <ellipse rx="10" ry="28" fill="rgba(240,200,212,0.65)" transform="rotate(45)"/>
      <ellipse rx="10" ry="28" fill="rgba(217,95,122,0.55)"  transform="rotate(90)"/>
      <ellipse rx="10" ry="28" fill="rgba(217,95,122,0.55)"  transform="rotate(135)"/>
      <circle r="12" fill="rgba(201,151,58,0.75)"/>
      <circle r="5"  fill="rgba(255,230,150,0.9)"/>
    </g>
  </svg>

  <!-- Stars scattered -->
  <span class="star" style="top:11%;left:7%;font-size:10px;animation-delay:0s;animation-duration:3s;">✦</span>
  <span class="star" style="top:7%;left:80%;font-size:9px;animation-delay:-1.4s;animation-duration:4.2s;">✦</span>
  <span class="star" style="top:28%;left:93%;font-size:7px;animation-delay:-0.8s;animation-duration:3.6s;">✦</span>
  <span class="star" style="top:68%;left:4%;font-size:8px;animation-delay:-2.2s;animation-duration:5s;">✦</span>
  <span class="star" style="top:52%;left:90%;font-size:6px;animation-delay:-0.9s;animation-duration:4.8s;">✦</span>
  <span class="star" style="top:38%;left:12%;font-size:7px;animation-delay:-3.1s;animation-duration:3.3s;">✦</span>
  <span class="star" style="top:83%;left:78%;font-size:8px;animation-delay:-0.5s;animation-duration:5.5s;">✦</span>
  <span class="star" style="top:20%;left:48%;font-size:6px;animation-delay:-2.7s;animation-duration:4s;opacity:0.2;">✦</span>

  <!-- Petals -->
  <div class="petals">
    <div class="petal"></div><div class="petal"></div><div class="petal"></div>
    <div class="petal"></div><div class="petal"></div><div class="petal"></div>
    <div class="petal"></div><div class="petal"></div>
  </div>

  <div class="hero-content">
    <div class="hero-label">✦ juneteenth 2026 ✦</div>
    <div class="hero-for">a day for</div>
    <div class="hero-name">{name_display}</div>
    <div class="hero-beach-name" id="hero-beach">...</div>
    <div class="hero-city" id="hero-city"></div>
    <div class="hero-vibes" id="hero-vibes"></div>
  </div>

  <div class="scroll-hint"><span>choose your beach</span></div>
</div>

<!-- BEACH PICKER -->
<div class="picker-wrap">
  <div class="picker-heading">where do you want to go?</div>
  <div class="picker-scroll" id="picker-scroll">
    {picker_cards}
  </div>
</div>

<!-- MAIN CONTENT -->
<div class="main-content">
  <div class="content-inner">

    <div class="intention">
      {note_html}
      <div class="beach-blurb" id="beach-blurb"></div>
    </div>

    <div class="meetup">
      <div class="meetup-icon">🌅</div>
      <div style="flex:1">
        <div class="meetup-label">leaving around</div>
        <input class="meetup-time" id="meetup" type="text" placeholder="what time..." oninput="saveGlobal('meetup',this.value)">
      </div>
    </div>

    <div class="divider"><div class="divider-line"></div><span class="divider-mark">✦</span><div class="divider-line"></div></div>
    <div class="section-title">bring this</div>
    <ul class="pack-list">
      <li class="pack-item" data-id="sunscreen" onclick="togglePack(this)"><span class="check-box"></span><span>sunscreen</span></li>
      <li class="pack-item" data-id="towels"    onclick="togglePack(this)"><span class="check-box"></span><span>towels</span></li>
      <li class="pack-item" data-id="water"     onclick="togglePack(this)"><span class="check-box"></span><span>water bottles</span></li>
      <li class="pack-item" data-id="snacks"    onclick="togglePack(this)"><span class="check-box"></span><span>snacks</span></li>
      <li class="pack-item" data-id="speaker"   onclick="togglePack(this)"><span class="check-box"></span><span>speaker</span></li>
      <li class="pack-item" data-id="blanket"   onclick="togglePack(this)"><span class="check-box"></span><span>blanket</span></li>
      <li class="pack-item" data-id="charger"   onclick="togglePack(this)"><span class="check-box"></span><span>portable charger</span></li>
      <li class="pack-item" data-id="cash"      onclick="togglePack(this)"><span class="check-box"></span><span>cash (for food)</span></li>
      <li class="pack-item" data-id="change"    onclick="togglePack(this)"><span class="check-box"></span><span>change of clothes</span></li>
      <li class="pack-item" id="pack-lighter" style="display:none" data-id="lighter" onclick="togglePack(this)"><span class="check-box"></span><span>lighter</span></li>
    </ul>

    <div class="divider"><div class="divider-line"></div><span class="divider-mark">✦</span><div class="divider-line"></div></div>
    <div class="section-title">eat well</div>
    <div class="food-list" id="food-list"></div>

    <div class="divider"><div class="divider-line"></div><span class="divider-mark">✦</span><div class="divider-line"></div></div>
    <div class="section-title">while you're there</div>
    <ul class="pack-list" id="spots-list"></ul>

    <div class="divider"><div class="divider-line"></div><span class="divider-mark">✦</span><div class="divider-line"></div></div>
    <div class="section-title">find your quiet</div>
    <ul class="pack-list" id="smoke-list"></ul>

    <div class="divider"><div class="divider-line"></div><span class="divider-mark">✦</span><div class="divider-line"></div></div>
    <div class="golden">
      <span class="g-star" style="top:14%;left:9%;font-size:8px;animation-delay:0s;animation-duration:3s;">✦</span>
      <span class="g-star" style="top:18%;left:87%;font-size:7px;animation-delay:-1.2s;animation-duration:4s;">✦</span>
      <span class="g-star" style="top:72%;left:7%;font-size:6px;animation-delay:-2.1s;animation-duration:3.8s;">✦</span>
      <span class="g-star" style="top:68%;left:90%;font-size:7px;animation-delay:-0.6s;animation-duration:5s;">✦</span>
      <span class="g-star" style="top:42%;left:4%;font-size:5px;animation-delay:-1.7s;animation-duration:4.2s;">✦</span>
      <span class="g-star" style="top:38%;left:94%;font-size:5px;animation-delay:-2.8s;animation-duration:3.2s;">✦</span>
      <span class="g-star" style="top:52%;left:50%;font-size:5px;animation-delay:-3s;animation-duration:6s;opacity:0.28;">✦</span>
      <div class="golden-inner">
        <div class="golden-script">golden hour</div>
        <div class="golden-text">when the sun starts dropping, find somewhere quieter. just the two of you. you'll know when.</div>
      </div>
    </div>

    <div class="divider"><div class="divider-line"></div><span class="divider-mark">✦</span><div class="divider-line"></div></div>
    <div class="section-title">parking</div>
    <div class="parking-card" id="parking-card"></div>

    <div class="divider"><div class="divider-line"></div><span class="divider-mark">✦</span><div class="divider-line"></div></div>
    <div class="section-title">your notes</div>
    <textarea class="notes-area" id="notes" placeholder="write anything down..." oninput="saveGlobal('notes',this.value)"></textarea>

  </div>
</div>

<div class="footer">
  <div class="footer-line"></div>
  made with love · juneteenth 2026
</div>

<script>
const BEACHES = {beaches_js};
const DEFAULT = "{default_key}";
const GLOBAL_KEY = "beach_day_global";
const PRICE_LABEL = {{"$":"budget-friendly","$$":"mid","$$$":"splurge"}};

function saveGlobal(field, val) {{
  const d = JSON.parse(localStorage.getItem(GLOBAL_KEY) || '{{}}');
  d[field] = val;
  localStorage.setItem(GLOBAL_KEY, JSON.stringify(d));
}}

function beachKey(key) {{ return 'beach_' + key; }}

function saveBeach(key, field, val) {{
  const d = JSON.parse(localStorage.getItem(beachKey(key)) || '{{}}');
  d[field] = val;
  localStorage.setItem(beachKey(key), JSON.stringify(d));
}}

function loadBeach(key) {{
  return JSON.parse(localStorage.getItem(beachKey(key)) || '{{}}');
}}

let currentBeach = null;

function selectBeach(key) {{
  if (!BEACHES[key]) return;
  currentBeach = key;
  saveGlobal('selected', key);

  document.querySelectorAll('.bp-card').forEach(c => c.classList.toggle('selected', c.dataset.key === key));

  const b = BEACHES[key];

  document.getElementById('hero-beach').textContent = b.name;
  document.getElementById('hero-city').textContent   = b.city;

  const vc = document.getElementById('hero-vibes');
  vc.innerHTML = b.vibe.map(v => `<span class="vibe-chip">${{v}}</span>`).join('') +
    (b.fire_pit ? '<span class="fp-chip">🔥 fire pits</span>' : '');

  document.getElementById('beach-blurb').textContent = b.notes;

  document.getElementById('pack-lighter').style.display = b.fire_pit ? '' : 'none';

  const fd = loadBeach(key);

  const fl = document.getElementById('food-list');
  fl.innerHTML = b.food_nearby.map((f, i) => {{
    const id = 'food' + i;
    const picked = fd.food === id ? 'picked' : '';
    const label = PRICE_LABEL[f.price] || f.price;
    return `<div class="food-card ${{picked}}" data-id="${{id}}" onclick="pickFood(this)">
      <div class="food-top"><span class="food-name">${{f.name}}</span><span class="price-tag">${{label}}</span></div>
      <div class="food-meta">${{f.type}} · ${{f.distance}}</div>
      <div class="food-note">${{f.note}}</div>
      <div class="pick-label">tap to choose this one</div>
      <div class="picked-label">✓ this is the pick</div>
    </div>`;
  }}).join('');

  const sl = document.getElementById('spots-list');
  sl.innerHTML = (b.spots_nearby || []).map((s, i) => {{
    const id = 'spot' + i;
    const done = (fd.spots || []).includes(id) ? 'done' : '';
    return `<li class="spot-item ${{done}}" data-id="${{id}}" onclick="toggleSpot(this)"><span class="check-box"></span><span>${{s}}</span></li>`;
  }}).join('');

  const smk = document.getElementById('smoke-list');
  smk.innerHTML = (b.smoke_spots || []).map((s, i) => {{
    const id = 'smoke' + i;
    const done = (fd.spots || []).includes(id) ? 'done' : '';
    return `<li class="spot-item ${{done}}" data-id="${{id}}" onclick="toggleSpot(this)"><span class="check-box"></span><span>${{s}}</span></li>`;
  }}).join('');

  document.getElementById('parking-card').innerHTML =
    b.parking + `<br><small style="color:#B8A888;margin-top:5px;display:block">~$${{b.budget_per_person}}/person estimated</small>`;

  const gd = JSON.parse(localStorage.getItem(GLOBAL_KEY) || '{{}}');
  document.querySelectorAll('.pack-item').forEach(el => {{
    el.classList.toggle('checked', (gd.packed || []).includes(el.dataset.id));
  }});
}}

function togglePack(el) {{
  el.classList.toggle('checked');
  const checked = [...document.querySelectorAll('.pack-item.checked')].map(e => e.dataset.id);
  saveGlobal('packed', checked);
}}

function toggleSpot(el) {{
  el.classList.toggle('done');
  const done = [...document.querySelectorAll('.spot-item.done')].map(e => e.dataset.id);
  saveBeach(currentBeach, 'spots', done);
}}

function pickFood(el) {{
  document.querySelectorAll('.food-card').forEach(c => c.classList.remove('picked'));
  el.classList.add('picked');
  saveBeach(currentBeach, 'food', el.dataset.id);
}}

const gd = JSON.parse(localStorage.getItem(GLOBAL_KEY) || '{{}}');
if (gd.meetup) document.getElementById('meetup').value = gd.meetup;
if (gd.notes)  document.getElementById('notes').value  = gd.notes;
selectBeach(gd.selected || DEFAULT);

setTimeout(() => {{
  const sel = document.querySelector('.bp-card.selected');
  if (sel) sel.scrollIntoView({{behavior:'smooth', block:'nearest', inline:'center'}});
}}, 100);
</script>
</body>
</html>"""

    return html.replace('{beaches_js}', beaches_js).replace('"{default_key}"', f'"{default_key}"')


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 make_plan.py <beach> [--for Name] [--note 'message']")
        return

    beach_key = args[0].lower().replace("-", "_")
    if beach_key not in BEACHES:
        print(f"Unknown beach. Try: {', '.join(BEACHES.keys())}")
        return

    for_name = note = None
    i = 1
    while i < len(args):
        if args[i] == "--for" and i + 1 < len(args):
            for_name = args[i+1]; i += 2
        elif args[i] == "--note" and i + 1 < len(args):
            note = args[i+1]; i += 2
        else:
            i += 1

    html = generate(beach_key, for_name, note)
    fname = f"plan_{beach_key}.html"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved → {fname}")
    webbrowser.open(f"file://{os.path.abspath(fname)}")

if __name__ == "__main__":
    main()
