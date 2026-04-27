# %%
import json
import random

import matplotlib.pyplot as plt
import numpy as np
from utils import config

config = config.load_config()

# %%
# =========================
# CARICAMENTO DATI
# =========================

ACCESS_MODE = "r"

with open("data/throughput.json", ACCESS_MODE) as f:
    data = json.load(f)

historical = data["throughput"]

print("Historical throughput:", historical)

# %%
# =========================
# MODELLO MONTE CARLO
# =========================


def simulate_sprint(
    thresholds,
    n_simulations=config.simulations.n_simulations,
    n_sprints=config.simulations.default_sprints,
):
    """
    Simula n_sprints futuri usando distribuzione empirica storica
    """
    results = []

    for _ in range(n_simulations):
        run = []

        for _ in range(n_sprints):
            run.append(random.choice(thresholds))

        results.append(sum(run))

    return results


# %%
# =========================
# SIMULAZIONE
# =========================

results = simulate_sprint(thresholds=historical)

results = np.array(results)

print("Simulations:", len(results))

# %%
# =========================
# STATISTICHE (DECISION MAKING)
# =========================

p50 = np.percentile(results, 50)
p85 = np.percentile(results, 85)
p95 = np.percentile(results, 95)

print("\n--- FORECAST ---")
print(f"P50 (median): {p50:.0f} items")
print(f"P85: {p85:.0f} items")
print(f"P95: {p95:.0f} items")

# %%
# =========================
# DISTRIBUZIONE
# =========================

plt.hist(results, bins=30)
plt.title("Monte Carlo Forecast - Total Throughput (10 sprints)")
plt.xlabel("Items completed")
plt.ylabel("Frequency")
plt.show()

# %%
# =========================
# INTERPRETAZIONE
# =========================

print("\n--- INTERPRETATION ---")
print("P50: scenario realistico")
print("P85: scenario conservativo")
print("P95: worst-case planning buffer")

