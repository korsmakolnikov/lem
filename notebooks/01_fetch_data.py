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
from fetch.youtrack import YouTrackClient
from utils.config import load_config

# Carica .env (override per evitare problemi in Jupyter)
load_dotenv(override=True)


# %%
# =========================
# CONFIGURAZIONE
# =========================

config = load_config()
client = YouTrackClient(config)


# %%
# =========================
# PIPELINE
# =========================

print("Fetching issues from YouTrack...")

issues = client.fetch_issues(query="tag: sprint-*")

print(f"Total issues fetched: {len(issues)}")

items_data = client.build_throughput_items(issues)
sprints, throughput_items = client.sort_sprints(items_data)

print("Sprints:", sprints)
print("Throughput:", throughput_items)

# %%
# =========================
# VALIDAZIONE
# =========================

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

# %%
# =========================
# VISUAL CHECK (OPZIONALE)
# =========================

plt.plot(throughput_items, marker="o")
plt.title("Throughput per sprint")
plt.xlabel("Sprint")
plt.ylabel("Items completed")
plt.show()
