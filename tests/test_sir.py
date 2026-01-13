from healthcare_suite.sir import SIRModel, SIRParams

def test_sir_conserves_population():
    params = SIRParams(population=1000, beta=0.3, gamma=0.1, initial_infected=10)
    df = SIRModel(params).simulate_euler(days=10, dt=0.5)
    totals = (df["S"] + df["I"] + df["R"]).round(6)
    assert (totals == params.population).all()

def test_sir_non_negative():
    params = SIRParams(population=100, beta=1.0, gamma=0.5, initial_infected=1)
    df = SIRModel(params).simulate_euler(days=5, dt=0.1)
    assert (df[["S", "I", "R"]] >= 0).all().all()
