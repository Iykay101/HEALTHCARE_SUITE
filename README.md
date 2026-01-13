# Healthcare Suite (Python)

Three mini-systems with tests and simple UIs:

1) **Drug interaction checker**
- Input: meds (manual text or CSV)
- Output: known interactions (pairwise) from a CSV "database"

2) **Epidemiological simulator (SIR)**
- Differential equations + Euler method solver
- Matplotlib and Plotly plots
- Adjustable parameters (beta, gamma, N, dt)

3) **Appointment scheduler**
- Doctor calendar with working hours + time slots
- Greedy scheduling and emergency preemption
- Outputs confirmed/rejected/preempted lists

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Run tests (with coverage)

```bash
pytest
```

## Run Streamlit UI

```bash
streamlit run apps/streamlit_app.py
```

## Run Flask API

```bash
python apps/flask_app.py
```

## Architecture

- `src/healthcare_suite/interactions/` — load + query interactions
- `src/healthcare_suite/sir/` — SIR model + simulation + plotting
- `src/healthcare_suite/scheduler/` — time-slot calendar + greedy scheduling
- `apps/` — Streamlit + Flask
- `tests/` — unit tests (aim: ≥80% coverage)

## Notes on LLM usage (for report)

Document where LLMs were used (schema ideas, algorithm suggestions, UI scaffolding) and what you changed:
refactoring, edge cases, improved validation, and added unit tests.
