# %%
# =========================
# SETUP
# =========================

import json
import os
from collections import defaultdict
from datetime import UTC, datetime

import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv
from utils.config import load_config

# Carica .env (override per evitare problemi in Jupyter)
load_dotenv(override=True)


# %%
# =========================
# CONFIGURAZIONE
# =========================


config = load_config()

headers = {
    "Authorization": f"Bearer {config.youtrack.token}",
    "Accept": "application/json",
}

SPRINT_PREFIX = "sprint-"
FIELDS = "idReadable,tags(name),customFields(name,value)"

# %%
# =========================
# FETCH PAGINATO
# =========================


def fetch_all_issues(base_url, headers, fields, query=None, batch_size=50):
    all_issues = []
    skip = 0

    while True:
        params = {"fields": fields, "$top": batch_size, "$skip": skip}

        if query:
            params["query"] = query

        response = requests.get(
            f"{base_url}/api/issues", headers=headers, params=params
        )

        response.raise_for_status()
        batch = response.json()

        if not batch:
            break

        all_issues.extend(batch)
        skip += batch_size

        print(f"Fetched {len(all_issues)} issues...")

    return all_issues


# %%
# =========================
# PARSING
# =========================


def get_sprint(issue):
    for tag in issue.get("tags", []):
        name = tag["name"]
        if name.startswith(SPRINT_PREFIX):
            return name
    return None


def get_story_points(issue):
    for field in issue.get("customFields", []):
        if field["name"] == "Story Points":
            return field.get("value")
    return None


# %%
# =========================
# AGGREGAZIONE
# =========================


def build_throughput(issues):
    sprint_counts = defaultdict(int)

    for issue in issues:
        sprint = get_sprint(issue)
        if sprint:
            sprint_counts[sprint] += 1

    return sprint_counts


def sort_sprints(sprint_counts):
    def sprint_key(s):
        return int(s.replace(SPRINT_PREFIX, ""))

    sorted_sprints = sorted(sprint_counts.keys(), key=sprint_key)
    throughput = [sprint_counts[s] for s in sorted_sprints]

    return sorted_sprints, throughput


# %%
# =========================
# PIPELINE
# =========================

print("Fetching issues from YouTrack...")

issues = fetch_all_issues(config.youtrack.url, headers, FIELDS, query="tag: sprint-*")

print(f"Total issues fetched: {len(issues)}")

sprint_counts = build_throughput(issues)
sprints, throughput = sort_sprints(sprint_counts)

print("Sprints:", sprints)
print("Throughput:", throughput)

# %%
# =========================
# VALIDAZIONE
# =========================

assert len(throughput) >= 3, "Too few sprints"
assert all(x > 0 for x in throughput), "Invalid throughput values"

# %%
# =========================
# SALVATAGGIO
# =========================

os.makedirs("data", exist_ok=True)

output = {
    "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "throughput": throughput,
    "sprints": sprints,
}

with open("data/throughput.json", "w") as f:
    json.dump(output, f, indent=2)

print("Saved to data/throughput.json")

# %%
# =========================
# VISUAL CHECK (OPZIONALE)
# =========================

plt.plot(throughput, marker="o")
plt.title("Throughput per sprint")
plt.xlabel("Sprint")
plt.ylabel("Items completed")
plt.show()
