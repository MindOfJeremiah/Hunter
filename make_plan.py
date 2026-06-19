# make_plan.py — generates a beach day plan page with an interactive beach picker.
# Usage:
#   python3 make_plan.py belmont_shore --for Kelli --note "you deserve a beautiful day"

import sys, os, webbrowser, json
from beach_day import BEACHES

# Long Beach beaches shown first, rest after
BEACH_ORDER = ["seal_beach", "belmont_shore", "junipero", "dockweiler", "el_matador", "zuma", "leo_carrillo", "manhattan", "venice"]

def generate(default_key, for_name=None, note=None):
    name_display = for_name if for_name else "today"
    note_html = f'<div class="intention-note">&#x201C;{note}&#x201D;</div>' if note else ""

    # Embed all beach data as JS — only beaches that exist in BEACHES
    ordered = [k for k in BEACH_ORDER if k in BEACHES] + [k for k in BEACHES if k not in BEACH_ORDER]
    beaches_js = json.dumps({k: BEACHES[k] for k in ordered}, ensure_ascii=False)

    # Build picker cards HTML
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
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --pink: #E8638C; --pink-light: #FFB6D9; --rose: #D4456B;
      --crimson: #8B1A38; --gold: #D4A843; --cream: #FFF8F0;
      --text: #2A1220; --muted: #A07080;
    }}
    body {{ font-family: 'DM Sans', -apple-system, sans-serif; background: var(--cream); color: var(--text); min-height: 100vh; overflow-x: hidden; }}

    /* HERO */
    .hero {{ position: relative; min-height: 300px; background: linear-gradient(160deg,#5C1030 0%,#8B1A38 18%,#C04070 38%,#E8638C 58%,#F4A0C0 78%,#FFD6E8 100%); overflow: hidden; display: flex; flex-direction: column; justify-content: flex-end; padding: 28px 28px 32px; }}
    .hero::before {{ content: '✦'; position: absolute; top: 20px; right: 24px; font-size: 60px; color: rgba(212,168,67,0.22); animation: pulse 4s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ opacity:.22; transform:scale(1); }} 50% {{ opacity:.38; transform:scale(1.08); }} }}
    .clouds {{ position: absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; }}
    .cloud {{ position: absolute; background: rgba(255,255,255,0.18); border-radius: 60px; animation: drift linear infinite; }}
    .cloud::before,.cloud::after {{ content:''; position:absolute; background:inherit; border-radius:50%; }}
    .c1 {{ width:120px; height:36px; top:15%; animation-duration:28s; }}
    .c1::before {{ width:56px; height:56px; top:-28px; left:18px; }}
    .c1::after  {{ width:40px; height:40px; top:-20px; left:55px; }}
    .c2 {{ width:80px; height:26px; top:38%; animation-duration:38s; animation-delay:-12s; opacity:.7; }}
    .c2::before {{ width:38px; height:38px; top:-20px; left:12px; }}
    .c2::after  {{ width:28px; height:28px; top:-14px; left:38px; }}
    .c3 {{ width:150px; height:42px; top:8%; animation-duration:50s; animation-delay:-25s; opacity:.5; }}
    .c3::before {{ width:66px; height:66px; top:-36px; left:20px; }}
    .c3::after  {{ width:48px; height:48px; top:-24px; left:76px; }}
    @keyframes drift {{ from {{ transform:translateX(-220px); }} to {{ transform:translateX(calc(100vw + 220px)); }} }}
    .petals {{ position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; overflow:hidden; }}
    .petal {{ position:absolute; animation:fall linear infinite; opacity:.75; }}
    .p1 {{ left:8%;  font-size:13px; animation-duration:9s; }}
    .p2 {{ left:22%; font-size:19px; animation-duration:13s; animation-delay:-3s; }}
    .p3 {{ left:40%; font-size:11px; animation-duration:11s; animation-delay:-6s; }}
    .p4 {{ left:60%; font-size:17px; animation-duration:15s; animation-delay:-1s; }}
    .p5 {{ left:75%; font-size:15px; animation-duration:10s; animation-delay:-8s; }}
    .p6 {{ left:90%; font-size:13px; animation-duration:14s; animation-delay:-4s; }}
    .p7 {{ left:50%; font-size:21px; animation-duration:12s; animation-delay:-9s; }}
    .p8 {{ left:32%; font-size:11px; animation-duration:16s; animation-delay:-2s; }}
    @keyframes fall {{ 0% {{ transform:translateY(-30px) rotate(0deg); opacity:0; }} 10% {{ opacity:.75; }} 90% {{ opacity:.4; }} 100% {{ transform:translateY(340px) rotate(540deg); opacity:0; }} }}
    .juneteenth-line {{ font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--gold); margin-bottom:8px; font-weight:500; }}
    .for-name {{ font-family:'Playfair Display',serif; font-style:italic; font-size:14px; color:rgba(255,255,255,.75); margin-bottom:5px; }}
    .hero-beach {{ font-family:'Playfair Display',serif; font-size:clamp(28px,7vw,44px); font-weight:700; color:#fff; line-height:1.1; text-shadow:0 2px 12px rgba(90,10,40,.35); margin-bottom:4px; transition: opacity .2s; }}
    .hero-city {{ font-size:13px; color:rgba(255,255,255,.6); margin-bottom:12px; }}
    .hero-vibes {{ display:flex; flex-wrap:wrap; gap:5px; }}
    .vibe-chip {{ font-size:11px; padding:3px 10px; border-radius:99px; background:rgba(255,255,255,.18); color:rgba(255,255,255,.9); border:1px solid rgba(255,255,255,.22); }}
    .fp-chip {{ font-size:11px; padding:3px 10px; border-radius:99px; background:rgba(212,168,67,.28); color:var(--gold); border:1px solid rgba(212,168,67,.4); }}

    /* BEACH PICKER */
    .picker-wrap {{ padding: 20px 0 0; }}
    .picker-label {{ font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); font-weight:500; padding:0 20px; margin-bottom:10px; }}
    .picker-scroll {{ display:flex; gap:10px; overflow-x:auto; padding:4px 20px 12px; scroll-snap-type:x mandatory; -webkit-overflow-scrolling:touch; scrollbar-width:none; }}
    .picker-scroll::-webkit-scrollbar {{ display:none; }}
    .bp-card {{ flex-shrink:0; width:148px; background:#fff; border-radius:14px; padding:13px 14px; border:2px solid #F0E0EC; cursor:pointer; scroll-snap-align:start; transition:all .2s; user-select:none; }}
    .bp-card:active {{ transform:scale(.97); }}
    .bp-card.selected {{ border-color:var(--pink); background:linear-gradient(135deg,#FFF5F8,#FFE8F2); box-shadow:0 0 0 3px rgba(232,99,140,.15); }}
    .bp-top {{ display:flex; align-items:center; gap:4px; margin-bottom:3px; }}
    .bp-name {{ font-weight:600; font-size:13px; color:#2A1220; line-height:1.2; }}
    .bp-fire {{ font-size:12px; }}
    .bp-local {{ font-size:9px; padding:1px 6px; border-radius:99px; background:rgba(212,168,67,.2); color:#8A6A10; border:1px solid rgba(212,168,67,.3); margin-left:2px; }}
    .bp-city {{ font-size:11px; color:#B090A0; margin-bottom:4px; }}
    .bp-vibe {{ font-size:11px; color:#8A6070; line-height:1.3; margin-bottom:5px; }}
    .bp-budget {{ font-size:11px; font-weight:500; color:var(--pink); }}
    .bp-card.selected .bp-name {{ color:var(--crimson); }}

    /* BODY */
    .body-wrap {{ padding:0 20px 60px; max-width:640px; margin:0 auto; }}
    .intention {{ background:linear-gradient(135deg,#F8E8F0,#FFF0F7); border-radius:20px; padding:22px 24px; margin:24px 0 0; border:1px solid rgba(232,99,140,.15); position:relative; }}
    .intention::before {{ content:'🌸'; position:absolute; top:-12px; right:20px; font-size:24px; }}
    .intention-label {{ font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--pink); font-weight:500; margin-bottom:10px; }}
    .intention-note {{ font-family:'Playfair Display',serif; font-style:italic; font-size:17px; color:var(--crimson); line-height:1.55; margin-bottom:10px; }}
    .beach-blurb {{ font-size:15px; color:#5A3040; line-height:1.65; transition:opacity .2s; }}
    .meetup {{ margin-top:18px; background:#fff; border-radius:16px; padding:16px 18px; border:1px solid #F0D8E8; display:flex; align-items:center; gap:12px; }}
    .meetup-icon {{ font-size:24px; flex-shrink:0; }}
    .meetup-label {{ font-size:10px; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); margin-bottom:3px; }}
    .meetup-time {{ font-size:20px; font-family:'Playfair Display',serif; font-weight:700; color:var(--crimson); border:none; background:none; padding:0; outline:none; width:100%; }}
    .meetup-time::placeholder {{ color:#D4A0B8; }}
    .section {{ margin-top:28px; }}
    .section-header {{ display:flex; align-items:center; gap:10px; margin-bottom:12px; }}
    .section-icon {{ font-size:18px; }}
    .section-title {{ font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); font-weight:500; }}
    .section-line {{ flex:1; height:1px; background:linear-gradient(90deg,#F0D0E0,transparent); }}
    .pack-list {{ list-style:none; }}
    .pack-item {{ display:flex; align-items:center; gap:12px; padding:12px 15px; background:#fff; border-radius:12px; margin-bottom:8px; border:1px solid #F5E5EE; cursor:pointer; transition:all .2s; font-size:14px; color:#4A2030; user-select:none; }}
    .pack-item.checked {{ background:#FFF0F7; border-color:#F0C8DC; }}
    .pack-item.checked span:last-child {{ text-decoration:line-through; color:var(--pink-light); }}
    .check-box {{ width:21px; height:21px; border-radius:50%; border:2px solid #E8B0CC; flex-shrink:0; display:flex; align-items:center; justify-content:center; transition:all .2s; font-size:12px; }}
    .pack-item.checked .check-box {{ background:var(--pink); border-color:var(--pink); color:#fff; }}
    .pack-item.checked .check-box::after {{ content:'✓'; }}
    .food-list {{ display:flex; flex-direction:column; gap:10px; }}
    .food-card {{ background:#fff; border-radius:16px; padding:15px 16px; border:2px solid #F5E5EE; cursor:pointer; transition:all .25s; }}
    .food-card:active {{ transform:scale(.98); }}
    .food-card.picked {{ border-color:var(--pink); background:linear-gradient(135deg,#FFF5F8,#FFE8F2); }}
    .food-top {{ display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:3px; }}
    .food-name {{ font-weight:600; font-size:14px; color:#2A1220; flex:1; }}
    .price-tag {{ font-size:10px; padding:2px 8px; border-radius:99px; background:#F5EAF0; color:var(--muted); flex-shrink:0; margin-left:8px; }}
    .food-card.picked .price-tag {{ background:rgba(232,99,140,.15); color:var(--rose); }}
    .food-meta {{ font-size:11px; color:#B090A0; margin-bottom:4px; }}
    .food-note {{ font-size:13px; color:#6A4050; line-height:1.4; }}
    .pick-label {{ font-size:11px; color:#D0A0B8; margin-top:8px; text-align:right; }}
    .picked-label {{ font-size:11px; color:var(--pink); font-weight:500; margin-top:8px; text-align:right; display:none; }}
    .food-card.picked .pick-label {{ display:none; }}
    .food-card.picked .picked-label {{ display:block; }}
    .spot-item {{ display:flex; align-items:flex-start; gap:11px; padding:12px 15px; background:#fff; border-radius:12px; margin-bottom:8px; border:1px solid #F5E5EE; cursor:pointer; transition:all .2s; font-size:13px; color:#4A2030; line-height:1.45; user-select:none; }}
    .spot-item.done {{ background:#FFF0F7; border-color:#F0C8DC; }}
    .spot-item.done span:last-child {{ text-decoration:line-through; color:var(--pink-light); }}
    .spot-item .check-box {{ margin-top:1px; flex-shrink:0; }}
    .spot-item.done .check-box {{ background:var(--pink); border-color:var(--pink); color:#fff; }}
    .spot-item.done .check-box::after {{ content:'✓'; }}
    .parking-card {{ background:#fff; border-radius:14px; padding:14px 16px; border:1px solid #F5E5EE; font-size:14px; color:#5A3040; line-height:1.5; }}
    .golden {{ background:linear-gradient(135deg,#3D0A1E,#7A1535,#C04060); border-radius:20px; padding:24px 22px; position:relative; overflow:hidden; }}
    .golden::before {{ content:'✦'; position:absolute; right:18px; top:14px; font-size:38px; color:rgba(212,168,67,.3); }}
    .golden-label {{ font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:var(--gold); margin-bottom:8px; font-weight:500; }}
    .golden-text {{ font-family:'Playfair Display',serif; font-style:italic; font-size:17px; color:rgba(255,255,255,.92); line-height:1.6; }}
    .notes-area {{ width:100%; min-height:110px; background:#fff; border:1px solid #F5E5EE; border-radius:14px; padding:14px 16px; font-family:'DM Sans',sans-serif; font-size:14px; color:#4A2030; resize:vertical; outline:none; transition:border-color .2s; line-height:1.6; }}
    .notes-area:focus {{ border-color:var(--pink-light); }}
    .notes-area::placeholder {{ color:#D4B0C4; }}
    .footer {{ text-align:center; padding:36px 20px 20px; font-size:12px; color:#D4A0B8; }}
    .footer-flowers {{ font-size:17px; letter-spacing:4px; margin-bottom:5px; }}
  </style>
</head>
<body>

<div class="hero">
  <div class="clouds"><div class="cloud c1"></div><div class="cloud c2"></div><div class="cloud c3"></div></div>
  <div class="petals">
    <div class="petal p1">🌸</div><div class="petal p2">🌷</div><div class="petal p3">🌸</div><div class="petal p4">🌺</div>
    <div class="petal p5">🌸</div><div class="petal p6">🌷</div><div class="petal p7">🌸</div><div class="petal p8">🌺</div>
  </div>
  <div class="juneteenth-line">✦ Juneteenth 2026 ✦</div>
  <div class="for-name">a day for {name_display}</div>
  <div class="hero-beach" id="hero-beach">loading...</div>
  <div class="hero-city" id="hero-city"></div>
  <div class="hero-vibes" id="hero-vibes"></div>
</div>

<div class="picker-wrap">
  <div class="picker-label">pick your beach</div>
  <div class="picker-scroll" id="picker-scroll">
    {picker_cards}
  </div>
</div>

<div class="body-wrap">

  <div class="intention">
    <div class="intention-label">set the tone</div>
    {note_html}
    <div class="beach-blurb" id="beach-blurb"></div>
  </div>

  <div class="meetup">
    <div class="meetup-icon">🌅</div>
    <div style="flex:1">
      <div class="meetup-label">leaving around</div>
      <input class="meetup-time" id="meetup" type="text" placeholder="fill in a time..." oninput="saveGlobal('meetup',this.value)">
    </div>
  </div>

  <div class="section">
    <div class="section-header"><span class="section-icon">🌺</span><span class="section-title">bring this</span><div class="section-line"></div></div>
    <ul class="pack-list">
      <li class="pack-item" data-id="sunscreen" onclick="togglePack(this)"><span class="check-box"></span><span>sunscreen</span></li>
      <li class="pack-item" data-id="towels" onclick="togglePack(this)"><span class="check-box"></span><span>towels</span></li>
      <li class="pack-item" data-id="water" onclick="togglePack(this)"><span class="check-box"></span><span>water bottles</span></li>
      <li class="pack-item" data-id="snacks" onclick="togglePack(this)"><span class="check-box"></span><span>snacks</span></li>
      <li class="pack-item" data-id="speaker" onclick="togglePack(this)"><span class="check-box"></span><span>speaker</span></li>
      <li class="pack-item" data-id="blanket" onclick="togglePack(this)"><span class="check-box"></span><span>blanket</span></li>
      <li class="pack-item" data-id="charger" onclick="togglePack(this)"><span class="check-box"></span><span>portable charger</span></li>
      <li class="pack-item" data-id="cash" onclick="togglePack(this)"><span class="check-box"></span><span>cash (for food)</span></li>
      <li class="pack-item" data-id="change" onclick="togglePack(this)"><span class="check-box"></span><span>change of clothes</span></li>
      <li class="pack-item" id="pack-lighter" style="display:none" data-id="lighter" onclick="togglePack(this)"><span class="check-box"></span><span>lighter or matches 🔥</span></li>
    </ul>
  </div>

  <div class="section">
    <div class="section-header"><span class="section-icon">🌷</span><span class="section-title">where to eat — tap your pick</span><div class="section-line"></div></div>
    <div class="food-list" id="food-list"></div>
  </div>

  <div class="section">
    <div class="section-header"><span class="section-icon">🌸</span><span class="section-title">while you're there</span><div class="section-line"></div></div>
    <ul class="pack-list" id="spots-list"></ul>
  </div>

  <div class="section">
    <div class="section-header"><span class="section-icon">🌬️</span><span class="section-title">step away spots</span><div class="section-line"></div></div>
    <ul class="pack-list" id="smoke-list"></ul>
  </div>

  <div class="section">
    <div class="golden">
      <div class="golden-label">golden hour</div>
      <div class="golden-text">when the sun starts dropping, find somewhere quieter. just the two of you. you'll know when.</div>
    </div>
  </div>

  <div class="section">
    <div class="section-header"><span class="section-icon">✦</span><span class="section-title">parking</span><div class="section-line"></div></div>
    <div class="parking-card" id="parking-card"></div>
  </div>

  <div class="section">
    <div class="section-header"><span class="section-icon">🌺</span><span class="section-title">notes / thoughts</span><div class="section-line"></div></div>
    <textarea class="notes-area" id="notes" placeholder="write anything here..." oninput="saveGlobal('notes',this.value)"></textarea>
  </div>

</div>

<div class="footer">
  <div class="footer-flowers">🌸 🌷 🌺</div>
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

  // Update picker highlight
  document.querySelectorAll('.bp-card').forEach(c => c.classList.toggle('selected', c.dataset.key === key));

  const b = BEACHES[key];

  // Hero
  document.getElementById('hero-beach').textContent = b.name;
  document.getElementById('hero-city').textContent = b.city;
  const vc = document.getElementById('hero-vibes');
  vc.innerHTML = b.vibe.map(v => `<span class="vibe-chip">${{v}}</span>`).join('') +
    (b.fire_pit ? '<span class="fp-chip">🔥 fire pits allowed</span>' : '');

  // Blurb
  document.getElementById('beach-blurb').textContent = b.notes;

  // Lighter in pack list
  document.getElementById('pack-lighter').style.display = b.fire_pit ? '' : 'none';

  // Food
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
      <div class="pick-label">tap to pick this one</div>
      <div class="picked-label">✓ this is the pick</div>
    </div>`;
  }}).join('');

  // Spots
  const sl = document.getElementById('spots-list');
  sl.innerHTML = (b.spots_nearby || []).map((s, i) => {{
    const id = 'spot' + i;
    const done = (fd.spots || []).includes(id) ? 'done' : '';
    return `<li class="spot-item ${{done}}" data-id="${{id}}" onclick="toggleSpot(this)"><span class="check-box"></span><span>${{s}}</span></li>`;
  }}).join('');

  // Smoke spots
  const smk = document.getElementById('smoke-list');
  smk.innerHTML = (b.smoke_spots || []).map((s, i) => {{
    const id = 'smoke' + i;
    const done = (fd.spots || []).includes(id) ? 'done' : '';
    return `<li class="spot-item ${{done}}" data-id="${{id}}" onclick="toggleSpot(this)"><span class="check-box"></span><span>${{s}}</span></li>`;
  }}).join('');

  // Parking
  document.getElementById('parking-card').innerHTML =
    b.parking + `<br><small style="color:#C0A0B0;margin-top:4px;display:block">~$${{b.budget_per_person}}/person total</small>`;

  // Restore pack checks (global)
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

// Init
const gd = JSON.parse(localStorage.getItem(GLOBAL_KEY) || '{{}}');
if (gd.meetup) document.getElementById('meetup').value = gd.meetup;
if (gd.notes) document.getElementById('notes').value = gd.notes;
selectBeach(gd.selected || DEFAULT);

// Scroll selected picker card into view
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
