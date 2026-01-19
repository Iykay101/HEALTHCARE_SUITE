# Healthcare Suite

## Project Overview
Healthcare Suite is a Python-based healthcare management system designed to demonstrate
core healthcare informatics concepts. The project integrates multiple components,
including drug interaction checking, epidemiological modeling, and appointment scheduling.

The system shows how healthcare software can automate decision-making, improve safety,
and support clinical workflows.

---

## Features

### 1. Drug Interaction Checker
- Accepts a list of medications
- Loads interaction data from CSV files
- Identifies known drug–drug interactions
- Provides warnings for potentially unsafe combinations

### 2. Epidemiological SIR Model
- Simulates disease spread using the SIR model
- Adjustable parameters (infection rate, recovery rate, population size)
- Numerical solution using the Euler method
- Visualisation of results using plots

### 3. Appointment Scheduling System
- Priority-based appointment scheduling
- Emergency appointments scheduled before routine ones
- Time-slot management using Python datetime
- Simple algorithm for efficient scheduling

### 4. User Interfaces
- Command-line interface for core functionality
- Streamlit and Flask interfaces for interactive use

---


## Project Structure
- `apps/` – GUI applications (Flask / Streamlit)
- `data/` – CSV files and datasets
- `src/healthcare_suite/`
  - `interactions/` – Drug interaction logic
  - `sir/` – SIR epidemiological model
  - `scheduler/` – Appointment scheduling
- `tests/` – Unit tests
- `README.md`
- `pyproject.toml`
- `requirements.txt`





yaml
Copy code

---

## Technologies Used
- Python
- Flask
- Streamlit
- Matplotlib
- Pandas
- Pytest

---

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
Run Streamlit app
bash
Copy code
streamlit run apps/streamlit_app.py
Run Flask app
bash
Copy code
python apps/flask_app.py
Testing
Unit tests are provided in the tests/ directory.

bash
Copy code
pytest
Notes
This project is for academic and learning purposes to demonstrate healthcare software
design principles and algorithmic problem solving.
