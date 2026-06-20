# job_bot.py — a Discord bot that posts your ranked job leads + beach day planner.
# Commands:
#   !jobs               → ranked new job leads
#   !beach              → list all beaches with budget/vibe
#   !beach <name>       → full breakdown for a beach (e.g. !beach dockweiler)
#   !beach --vibe <v>   → beaches by vibe (quiet, fire pit, hidden, energy, sunset...)
#   !beach --budget <n> → beaches you can do under $n/person
#
# Setup:
#   1. pip install discord.py
#   2. Make a bot at discord.com/developers (enable Message Content Intent),
#      invite it to your server, and put its token in .env as JOB_BOT_TOKEN.
#      (Can be the same app as Vern's bot or a separate one — your call.)
#   3. python3 job_bot.py

import os
import asyncio
import discord
from dotenv import load_dotenv
from job_hunter import get_jobs, save_csv
from beach_day import BEACHES, VIBES

load_dotenv()
TOKEN = os.getenv("JOB_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def format_job(j):
    # One job as a compact Discord line with a clickable link.
    tag = " 🔥" if j["urgent"] else ""
    sal = f" · {j['salary']}" if j["salary"] else ""
    remote = " · remote" if j["remote"] else ""
    return (f"**[{j['score']}] {j['title']}** — {j['company']}{tag}\n"
            f"{j['location']} · {j['posted']}{remote}{sal}\n{j['url']}")


@client.event
async def on_ready():
    print(f"Job bot online as {client.user}")


def format_beach(key):
    b = BEACHES[key]
    fp = "  🔥 fire pits" if b["fire_pit"] else ""
    lines = [
        f"**{b['name']}** — {b['city']}{fp}",
        f"Vibe: {', '.join(b['vibe'][:3])}",
        f"Parking: {b['parking']}",
        f"Budget: ~${b['budget_per_person']}/person",
        f"",
        b["notes"],
        f"",
        "**Food nearby:**",
    ]
    for f in b["food_nearby"]:
        lines.append(f"{f['price']} **{f['name']}** ({f['type']}) — {f['distance']}\n   _{f['note']}_")
    lines += ["", "**Also nearby:**"]
    for s in b["spots_nearby"]:
        lines.append(f"• {s}")
    return "\n".join(lines)


@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()
    lower = content.lower()

    if lower.startswith("!beach"):
        args = content[6:].strip().split()

        if not args:
            lines = ["**SoCal beaches — pick one or filter by vibe/budget:**\n"]
            for key, b in BEACHES.items():
                fp = " 🔥" if b["fire_pit"] else ""
                lines.append(f"`{key}` — **{b['name']}**, {b['city']}{fp}  ~${b['budget_per_person']}/person  |  {', '.join(b['vibe'][:3])}")
            lines.append("\n`!beach <name>` · `!beach --vibe quiet` · `!beach --budget 20`")
            await message.channel.send("\n".join(lines))
            return

        if args[0] == "--vibe" and len(args) > 1:
            vibe = " ".join(args[1:]).lower()
            matches = VIBES.get(vibe, [])
            if not matches:
                await message.channel.send(f"No matches for vibe **{vibe}**. Try: {', '.join(VIBES.keys())}")
            else:
                for key in matches:
                    await message.channel.send(format_beach(key))
            return

        if args[0] == "--budget" and len(args) > 1:
            try:
                cap = int(args[1])
            except ValueError:
                await message.channel.send("Usage: `!beach --budget 20`")
                return
            matches = [k for k, b in BEACHES.items() if b["budget_per_person"] <= cap]
            if not matches:
                lowest = min(b["budget_per_person"] for b in BEACHES.values())
                await message.channel.send(f"Nothing under ${cap}/person. Cheapest option is ~${lowest}.")
            else:
                await message.channel.send(f"**Beaches under ${cap}/person:**")
                for key in matches:
                    await message.channel.send(format_beach(key))
            return

        key = args[0].lower().replace("-", "_")
        if key in BEACHES:
            await message.channel.send(format_beach(key))
        else:
            known = ", ".join(f"`{k}`" for k in BEACHES)
            await message.channel.send(f"Beach `{args[0]}` not found. Known: {known}")
        return

    if not lower.startswith("!jobs"):
        return

    async with message.channel.typing():
        # Scraping is blocking — run it off the event loop so the bot stays responsive.
        jobs, new_jobs = await asyncio.to_thread(get_jobs)
        await asyncio.to_thread(save_csv, jobs)

    show = new_jobs if new_jobs else jobs
    if not show:
        await message.channel.send("No jobs found right now — try again later.")
        return

    header = (f"**{len(new_jobs)} new job(s)** since last check "
              f"(of {len(jobs)} total). Best matches first:")
    await message.channel.send(header)

    # Post the top 8, one message each (keeps links clickable, dodges the 2000-char cap).
    for j in show[:8]:
        await message.channel.send(format_job(j))


if __name__ == "__main__":
    if not TOKEN:
        print("No JOB_BOT_TOKEN in .env — add it first (see setup notes), then re-run.")
    else:
        client.run(TOKEN)
