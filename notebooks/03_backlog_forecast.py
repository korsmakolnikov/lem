# %%
# ==========
# CONFIG
# ==========

import ipywidgets as widgets
import numpy as np
from bokeh.io import output_notebook
from bokeh.models.annotations.geometry import Span
from bokeh.models.annotations.labels import Label
from bokeh.plotting import figure, show
from fetch.youtrack import YouTrackClient
from IPython.display import clear_output, display
from utils.config import load_config

# Va chiamata UNA volta qui, fuori da tutto
output_notebook()

config = load_config()
client = YouTrackClient(config)

issues = client.fetch_issues(query="tag: sprint-*")
items_data = client.build_throughput_items(issues)
_, throughput = client.sort_sprints(items_data)

print("Throughput storico:", throughput)


def simulate_sprints_to_complete(
    backlog_size: int, throughput_history: list[int], n_sim: int
):
    results = []
    for _ in range(n_sim):
        remaining = backlog_size
        sprints = 0
        while remaining > 0:
            sampled = np.random.choice(throughput_history)
            remaining -= sampled
            sprints += 1
        results.append(sprints)
    return results


def plot_backlog_forecast(results, p50, p85, p95):
    hist, edges = np.histogram(results, bins=range(min(results), max(results) + 2))

    p = figure(
        title="Distribuzione sprint necessari",
        x_axis_label="Sprint",
        y_axis_label="Frequenza",
        width=800,
        height=400,
        tools="pan,wheel_zoom,box_zoom,reset",
    )

    p.quad(
        top=hist,
        bottom=0,
        left=edges[:-1],
        right=edges[1:],
        fill_color="steelblue",
        line_color="white",
    )

    def add_percentile_line(value, color, label_text):
        line = Span(location=value, dimension="height", line_color=color, line_width=3)
        label = Label(
            x=value,
            y=max(hist) * 0.95,  # leggermente sotto il bordo per non uscire
            text=label_text,
            text_color=color,
        )
        p.add_layout(line)
        p.add_layout(label)

    add_percentile_line(p50, "blue", f"P50 ({p50})")
    add_percentile_line(p85, "orange", f"P85 ({p85})")
    add_percentile_line(p95, "red", f"P95 ({p95})")

    # display() esplicito necessario dentro widgets.Output()
    display(show(p, notebook_handle=True))


# %%
# ==========
# GUI
# ==========

backlog_input = widgets.IntText(value=50, description="Backlog:")
sim_input = widgets.IntText(value=config.simulations.n_simulations, description="Sim:")
run_button = widgets.Button(description="Run Simulation", button_style="success")
output = widgets.Output()

display(backlog_input, sim_input, run_button, output)


def run_simulation(_):
    with output:
        clear_output(wait=True)  # wait=True evita flickering

        backlog = backlog_input.value
        n_sim = sim_input.value

        results = simulate_sprints_to_complete(backlog, throughput, n_sim)

        p50 = int(np.percentile(results, 50))
        p85 = int(np.percentile(results, 85))
        p95 = int(np.percentile(results, 95))

        print(f"Backlog: {backlog}")
        print(f"P50: {p50} sprint")
        print(f"P85: {p85} sprint")
        print(f"P95: {p95} sprint")

        plot_backlog_forecast(results, p50, p85, p95)


run_button.on_click(run_simulation)
