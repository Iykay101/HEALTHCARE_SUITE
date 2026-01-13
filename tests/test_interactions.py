from healthcare_suite.interactions import InteractionDB

def test_interaction_found(tmp_path):
    csv = tmp_path / "i.csv"
    csv.write_text("drug_a,drug_b,severity,description\nAspirin,Warfarin,major,Bleeding\n")
    db = InteractionDB.from_csv(csv)
    hits = db.check_list(["warfarin", "aspirin"])
    assert len(hits) == 1
    assert hits[0].severity.lower() == "major"

def test_interaction_none(tmp_path):
    csv = tmp_path / "i.csv"
    csv.write_text("drug_a,drug_b,severity,description\na,b,minor,x\n")
    db = InteractionDB.from_csv(csv)
    hits = db.check_list(["c", "d"])
    assert hits == []
