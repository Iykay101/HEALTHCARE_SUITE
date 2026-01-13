from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd


def load_med_list_from_csv(path: str | Path, column: str = "medication") -> List[str]:
    df = pd.read_csv(path)
    if column not in df.columns:
        raise ValueError(f"CSV must contain a '{column}' column")
    return [str(x) for x in df[column].dropna().tolist()]


def parse_med_list_from_text(text: str) -> List[str]:
    if not text:
        return []
    raw = []
    for chunk in text.replace("\n", ",").split(","):
        c = chunk.strip()
        if c:
            raw.append(c)
    return raw
