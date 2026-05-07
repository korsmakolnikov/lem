# %%
# =========================
# SETUP
# =========================

import json
import os
from datetime import UTC, datetime

from dotenv import load_dotenv
from fetch.youtrack import YouTrackClient
from utils.config import load_config

load_dotenv(override=True)

config = load_config()
client = YouTrackClient(config)


# %%
# =========================
# FETCH
# =========================

print("Fetching issues from YouTrack...")

issues = client.fetch_issues(query="tag: sprint-*")

print(f"Total issues fetched: {len(issues)}")

items_data = client.build_throughput_items(issues)
sprints, throughput_items = client.sort_sprints(items_data)

print("Sprints:", sprints)
print("Throughput:", throughput_items)

assert len(throughput_items) >= 3, "Too few sprints"
assert all(x > 0 for x in throughput_items), "Invalid throughput values"

# %%
# =========================
# SALVATAGGIO
# =========================

os.makedirs("data", exist_ok=True)

output = {
    "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "throughput": throughput_items,
    "sprints": sprints,
}

with open("data/throughput.json", "w") as f:
    json.dump(output, f, indent=2)

print("Saved to data/throughput.json")
