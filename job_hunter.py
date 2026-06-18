# job_hunter_v2.py — an upgraded version of the Indeed scraper.
# What's new vs v1:
#   - Captures the APPLY URL (you can finally click through and apply)
#   - Captures the description snippet + how recently it was posted
#   - SCORES each job against your profile and sorts best-first
#   - Remembers what it's seen, so each run shows only NEW jobs (a fresh shortlist)
#
# Note: scraping Indeed is fragile (their site changes) and against their ToS.
# Fine for personal job-hunting; for something durable, swap to a real job API later.

import re
import json
import csv
import os
from curl_cffi import requests as cffi_requests
from datetime import datetime

# Keyword -> weight. Higher = more "you". This is your main DIAL — edit it freely
# to steer what surfaces. You like variety + good experience, so it's broad, not dev-only.
PROFILE_KEYWORDS = {
    # entry-accessible (you're early-career)
    "junior": 3, "entry": 3, "apprentice": 3, "trainee": 2, "no experience": 3,
    # flexible / side-quest energy
    "freelance": 3, "contract": 2, "remote": 2, "flexible": 1, "part time": 1, "part-time": 1, "internship": 2,
    # tech (cool but not required)
    "developer": 2, "web": 1, "frontend": 2, "full stack": 2, "it support": 2, "help desk": 2,
    "qa": 2, "tester": 1, "technical": 1, "automation": 2, "no code": 2, "no-code": 2,
    # interesting / good-experience / creative
    "creative": 2, "design": 2, "media": 1, "content": 1, "marketing": 1, "production": 1,
    "event": 2, "startup": 2, "ai": 2, "data": 1, "community": 2, "coordinator": 2, "operations": 1,
}

# Titles to skip entirely (too senior for an entry-level search).
SENIOR_WORDS = ["senior", "principal", "staff", "lead", "architect",
                "manager", "director", "sr.", "sr ", "head of", "vp ", "ii "]

SEEN_FILE = "seen_jobs.json"   # remembers job keys across runs


def load_seen():
    try:
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_seen(keys):
    with open(SEEN_FILE, "w") as f:
        json.dump(sorted(keys), f)


def salary_value(text):
    # Pull a rough yearly number out of a salary string, for ranking. 0 if none.
    if not text:
        return 0
    nums = re.findall(r"\d[\d,]*", text)
    if not nums:
        return 0
    n = int(nums[0].replace(",", ""))
    if "hour" in text.lower():
        n *= 2000        # ~full-time year, so hourly and yearly compare fairly
    return n


def score_job(job):
    # Turn a job into a "how good is this" number so the best float to the top.
    # Rewards: fit to your interests + good pay + remote + fresh + urgent.
    title = job["title"].lower()
    score = sum(weight for kw, weight in PROFILE_KEYWORDS.items() if kw in title)

    pay = salary_value(job["salary"])         # good pay = a "good" job, broadly
    if pay >= 90000:
        score += 3
    elif pay >= 65000:
        score += 2
    elif pay >= 45000:
        score += 1

    if job["remote"]:
        score += 2
    posted = job["posted"].lower()
    if "today" in posted or "just posted" in posted:
        score += 2                            # fresh postings are worth jumping on
    elif "1 day" in posted or "2 day" in posted:
        score += 1
    if job["urgent"]:
        score += 1
    return score


def scrape_indeed(query, location):
    url = f"https://www.indeed.com/jobs?q={query}&l={location}&start=0"
    print(f"  searching '{query}' in '{location}'...")
    try:
        r = cffi_requests.get(url, impersonate="chrome124", timeout=30)
    except Exception as e:
        print(f"    error: {e}")
        return []
    if r.status_code != 200:
        print(f"    blocked: {r.status_code}")
        return []

    m = re.search(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]\s*=\s*({.+?});', r.text)
    if not m:
        print("    no job data found")
        return []

    results = (json.loads(m.group(1))
               .get("metaData", {})
               .get("mosaicProviderJobCardsModel", {})
               .get("results", []))

    jobs = []
    for j in results:
        title = j.get("title", "")
        if any(w in title.lower() for w in SENIOR_WORDS):
            continue
        jobkey = j.get("jobkey", "")
        salary = j.get("salarySnippet") or {}
        jobs.append({
            "title": title,
            "company": j.get("company", "Unknown"),
            "location": j.get("formattedLocation", "Unknown"),
            "salary": salary.get("text", ""),
            "remote": bool(j.get("remoteWorkModel")) or "remote" in j.get("formattedLocation", "").lower(),
            "posted": j.get("formattedRelativeTime", ""),
            "urgent": bool(j.get("urgentlyHiring")),
            "url": f"https://www.indeed.com/viewjob?jk={jobkey}" if jobkey else "",
            "snippet": re.sub(r"<[^>]+>", " ", j.get("snippet", "")).strip()[:200],
            "jobkey": jobkey,
            "found": datetime.now().strftime("%Y-%m-%d"),
        })
    print(f"    found {len(jobs)}")
    return jobs


# Your other DIAL — what to go looking for. Mix of dev + side-quests + good experience.
# Edit / add lines freely; (search terms, location). Used by both the CLI and the Discord bot.
SEARCHES = [
    ("junior+web+developer", "remote"),
    ("freelance+developer", "remote"),
    ("entry+level+tech", "remote"),
    ("creative+technologist", "remote"),
    ("ai+training", "remote"),
    ("remote+internship", "remote"),
    ("event+production", "Los+Angeles"),
    ("operations+coordinator", "Los+Angeles"),
    ("community+manager", "remote"),
    ("it+support", "Los+Angeles"),
]


def get_jobs(mark_seen=True):
    # The reusable entry point — scrape, dedupe, score, sort, and figure out what's NEW.
    # Returns (all_jobs, new_jobs), both sorted best-first. The Discord bot calls this too.
    all_jobs = []
    for query, location in SEARCHES:
        all_jobs.extend(scrape_indeed(query, location))

    unique = {}                              # dedupe by jobkey
    for j in all_jobs:
        if j["jobkey"] and j["jobkey"] not in unique:
            unique[j["jobkey"]] = j
    jobs = list(unique.values())

    for j in jobs:
        j["score"] = score_job(j)
    jobs.sort(key=lambda x: x["score"], reverse=True)

    seen = load_seen()
    new_jobs = [j for j in jobs if j["jobkey"] not in seen]
    if mark_seen:
        save_seen(seen | {j["jobkey"] for j in jobs})
    return jobs, new_jobs


def save_csv(jobs, path="jobs_today.csv"):
    if not jobs:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "score", "title", "company", "location", "salary",
            "remote", "posted", "url", "snippet", "found"])
        writer.writeheader()
        for j in jobs:
            writer.writerow({k: j[k] for k in writer.fieldnames})


if __name__ == "__main__":
    jobs, new_jobs = get_jobs()
    save_csv(jobs)

    print(f"\n{'='*60}")
    print(f"{len(jobs)} jobs total | {len(new_jobs)} NEW since last run")
    print(f"{'='*60}\n")

    show = new_jobs if new_jobs else jobs
    label = "NEW jobs" if new_jobs else "top jobs (nothing new this run)"
    print(f"Your {label}, best-matched first:\n")
    for j in show[:10]:
        tag = " [URGENT]" if j["urgent"] else ""
        sal = f" | {j['salary']}" if j["salary"] else ""
        print(f"[{j['score']}] {j['title']} @ {j['company']}{tag}")
        print(f"     {j['location']} | {j['posted']}{sal}")
        print(f"     {j['url']}")
        print()

    print(f"Saved {len(jobs)} jobs to jobs_today.csv (remembered keys for next run).")
