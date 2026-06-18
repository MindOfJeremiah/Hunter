# job_bot.py — a Discord bot that posts your ranked job leads.
# Type "!jobs" in any channel the bot can see, and it scrapes, ranks, and posts
# the NEW jobs since last time. Reuses job_hunter_v2.py as its engine.
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


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if not message.content.lower().strip().startswith("!jobs"):
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
