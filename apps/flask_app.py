from __future__ import annotations

from flask import Flask, jsonify, request

from healthcare_suite.interactions import InteractionDB
from healthcare_suite.sir import SIRModel, SIRParams

app = Flask(__name__)
DEFAULT_INTERACTIONS = "data/sample_interactions.csv"

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/interactions/check")
def interactions_check():
    payload = request.get_json(force=True)
    meds = payload.get("medications", [])
    db_path = payload.get("db_path", DEFAULT_INTERACTIONS)
    db = InteractionDB.from_csv(db_path)
    hits = db.check_list(meds)
    return jsonify({"count": len(hits), "hits": [h.__dict__ for h in hits]})

@app.post("/sir/simulate")
def sir_simulate():
    payload = request.get_json(force=True)
    params = SIRParams(
        population=int(payload["population"]),
        beta=float(payload["beta"]),
        gamma=float(payload["gamma"]),
        initial_infected=int(payload.get("initial_infected", 1)),
        initial_recovered=int(payload.get("initial_recovered", 0)),
    )
    days = int(payload.get("days", 160))
    dt = float(payload.get("dt", 0.2))
    df = SIRModel(params).simulate_euler(days=days, dt=dt)
    return jsonify({"rows": df.to_dict(orient="records")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
