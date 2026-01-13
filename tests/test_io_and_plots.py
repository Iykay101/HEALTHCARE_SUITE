from pathlib import Path
import pandas as pd

from healthcare_suite.interactions.io import parse_med_list_from_text, load_med_list_from_csv
from healthcare_suite.sir.plots import plot_sir_matplotlib, plot_sir_plotly

def test_parse_med_list_from_text():
    meds = parse_med_list_from_text(" warfarin,\n ibuprofen ,amiodarone ")
    assert meds == ["warfarin", "ibuprofen", "amiodarone"]

def test_load_med_list_from_csv(tmp_path: Path):
    p = tmp_path / "m.csv"
    p.write_text("medication\nwarfarin\nibuprofen\n")
    meds = load_med_list_from_csv(p)
    assert meds == ["warfarin", "ibuprofen"]

def test_plot_helpers_return_figures():
    df = pd.DataFrame({"t":[0,1],"S":[99,98],"I":[1,2],"R":[0,0]})
    fig1 = plot_sir_matplotlib(df, title="x")
    assert hasattr(fig1, "savefig")
    fig2 = plot_sir_plotly(df, title="x")
    assert fig2.to_dict()["layout"]["title"]["text"] == "x"
