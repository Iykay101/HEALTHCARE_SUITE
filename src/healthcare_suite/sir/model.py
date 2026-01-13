from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import pandas as pd


@dataclass(frozen=True)
class SIRParams:
    population: int
    beta: float
    gamma: float
    initial_infected: int = 1
    initial_recovered: int = 0


class SIRModel:
    """SIR model:
    dS/dt = -beta*S*I/N
    dI/dt =  beta*S*I/N - gamma*I
    dR/dt =  gamma*I
    """

    def __init__(self, params: SIRParams):
        if params.population <= 0:
            raise ValueError("population must be positive")
        if params.initial_infected < 0 or params.initial_recovered < 0:
            raise ValueError("initial values must be non-negative")
        if params.initial_infected + params.initial_recovered > params.population:
            raise ValueError("initial states exceed population")
        if params.beta < 0 or params.gamma < 0:
            raise ValueError("beta and gamma must be non-negative")
        self.params = params

    def initial_state(self) -> Tuple[float, float, float]:
        S = float(self.params.population - self.params.initial_infected - self.params.initial_recovered)
        I = float(self.params.initial_infected)
        R = float(self.params.initial_recovered)
        return S, I, R

    def derivatives(self, S: float, I: float, R: float) -> Tuple[float, float, float]:
        N = float(self.params.population)
        beta = self.params.beta
        gamma = self.params.gamma
        dS = -beta * S * I / N
        dI = beta * S * I / N - gamma * I
        dR = gamma * I
        return dS, dI, dR

    def simulate_euler(self, days: int, dt: float = 0.1) -> pd.DataFrame:
        if days <= 0:
            raise ValueError("days must be positive")
        if dt <= 0:
            raise ValueError("dt must be positive")

        steps = int(days / dt) + 1
        S, I, R = self.initial_state()
        t = 0.0
        rows: List[Dict[str, float]] = []

        for _ in range(steps):
            rows.append({"t": t, "S": S, "I": I, "R": R})
            dS, dI, dR = self.derivatives(S, I, R)
            S = max(0.0, S + dt * dS)
            I = max(0.0, I + dt * dI)
            R = max(0.0, R + dt * dR)

            # enforce conservation
            total = S + I + R
            if total > 0:
                scale = self.params.population / total
                S *= scale
                I *= scale
                R *= scale

            t += dt

        return pd.DataFrame(rows)
