# Hunter

A personal job-lead tool. It scrapes job listings, **ranks them against your taste**
(pay, remote, recency, interesting roles — not just "developer"), shows only what's **new**
since your last run, and gives you **real apply links**. Comes with a CLI and a Discord bot.

## What it does

- Searches multiple queries
- Scores each job so the best float to the top
- Remembers what it's seen → each run is a fresh shortlist, not the same list
- Saves everything to `jobs_today.csv` with links, salary, recency, and a description snippet
- Optional Discord bot: type `!jobs` and it posts your new leads to a channel

## Install

```bash
pip install curl_cffi discord.py python-dotenv
```

## Run it (CLI)

```bash
python3 job_hunter.py
```

You'll get a ranked list of new jobs in the terminal, and a `jobs_today.csv` you can open
in any spreadsheet.

## Tune it

Two dials, both at the top of `job_hunter.py`:

- **`SEARCHES`** — what it hunts for. Add lines like `("research+assistant", "remote")` or
  `("production+coordinator", "Los+Angeles")`. Use `+` between words.
- **`PROFILE_KEYWORDS`** — what counts as "you", with weights. Bump up what you want to see
  more of, add new keywords, delete what bores you. Higher weight = ranks higher.

Scoring also rewards good pay, remote, fresh postings, and "urgently hiring" automatically.

## Run it (Discord bot)

1. Make a bot at [discord.com/developers](https://discord.com/developers/applications),
   enable **Message Content Intent**, invite it to your server.
2. Put its token in a `.env` file next to the scripts:
   ```
   JOB_BOT_TOKEN=your_bot_token
   ```
3. Start it:
   ```bash
   python3 job_bot.py
   ```
4. In Discord, type `!jobs` — it scrapes and posts your new ranked leads.

## Files

- `job_hunter.py` — the engine (scrape, score, dedupe) + CLI. Importable: `get_jobs()`.
- `job_bot.py` — the Discord bot (`!jobs` command).
- `seen_jobs.json` — remembers which jobs you've already seen (auto-managed).
- `jobs_today.csv` — latest results.

## Honest notes

- It scrapes Indeed, which is fragile (their site changes) and against their ToS — fine for
  personal use, but for something durable, add a real job API (e.g. RemoteOK's public API).
- Finding jobs isn't the bottleneck — **applying consistently is.** This just removes the
  friction so you can apply daily.
- `.env` holds your bot token — never commit it.

## Ideas / roadmap

- Add a legal API source (RemoteOK / Hacker News "Who's Hiring") so it never breaks
- Daily auto-run (cron) that posts to Discord every morning
- Application tracker (mark applied, follow-up reminders)
- Tailored-resume helper (feed a job description + your resume → a tailored draft)
