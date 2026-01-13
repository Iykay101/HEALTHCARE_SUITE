from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go


def plot_sir_matplotlib(df: pd.DataFrame, title: str = "SIR Simulation") -> plt.Figure:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(df["t"], df["S"], label="Susceptible")
    ax.plot(df["t"], df["I"], label="Infected")
    ax.plot(df["t"], df["R"], label="Recovered")
    ax.set_xlabel("Time (days)")
    ax.set_ylabel("People")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_sir_plotly(df: pd.DataFrame, title: str = "SIR Simulation") -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["t"], y=df["S"], mode="lines", name="Susceptible"))
    fig.add_trace(go.Scatter(x=df["t"], y=df["I"], mode="lines", name="Infected"))
    fig.add_trace(go.Scatter(x=df["t"], y=df["R"], mode="lines", name="Recovered"))
    fig.update_layout(title=title, xaxis_title="Time (days)", yaxis_title="People")
    return fig
