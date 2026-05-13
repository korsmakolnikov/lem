# %%
# =========================
# CONFIG
# =========================

import json
import random

import numpy as np
from bokeh.io import output_notebook
from bokeh.models.annotations.geometry import Span
from bokeh.models.annotations.labels import Label
from bokeh.plotting import figure, show
from utils import config

output_notebook()

config = config.load_config()
with open("data/throughput.json") as f:
    data = json.load(f)

historical = data["throughput"]

print("Historical throughput:", historical)


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
        run = [random.choice(thresholds) for _ in range(n_sprints)]
        results.append(sum(run))

    return results


# %%
# =========================
# SIMULAZIONE
# =========================

results = simulate_sprint(thresholds=historical)
results = np.array(results)

print("Simulations:", len(results))

p50 = np.percentile(results, 50)
p85 = np.percentile(results, 85)
p95 = np.percentile(results, 95)

print("\n--- FORECAST ---")
print(f"P50 (median): {p50:.0f} items")
print(f"P85: {p85:.0f} items")
print(f"P95: {p95:.0f} items")

hist, edges = np.histogram(results, bins=30)

p = figure(
    title="Monte Carlo Forecast - Total Throughput (10 sprints)",
    x_axis_label="Items completed",
    y_axis_label="Frequency",
    width=800,
    height=400,
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

p.quad(
    top=hist,
    bottom=0,
    left=edges[:-1],
    right=edges[1:],
    fill_color="steelblue",
    line_color="white",
    fill_alpha=0.8,
)

# Linee percentili
for value, color, label_text in [
    (p50, "blue", f"P50 ({p50:.0f})"),
    (p85, "orange", f"P85 ({p85:.0f})"),
    (p95, "red", f"P95 ({p95:.0f})"),
]:
    p.add_layout(
        Span(
            location=value,
            dimension="height",
            line_color=color,
            line_width=2,
            line_dash="dashed",
        )
    )
    p.add_layout(
        Label(
            x=value + (edges[-1] - edges[0]) * 0.01,
            y=max(hist) * 0.95,
            text=label_text,
            text_color=color,
            text_font_size="11px",
        )
    )

show(p)

print("\n--- INTERPRETATION ---")
print("P50: scenario realistico")
print("P85: scenario conservativo")
print("P95: worst-case planning buffer")
