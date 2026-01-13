from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from .models import DrugInteraction, InteractionHit, normalize_drug_name


@dataclass
class InteractionDB:
    """In-memory interaction DB indexed by unordered normalized pairs."""
    _index: Dict[Tuple[str, str], DrugInteraction]

    @classmethod
    def from_csv(cls, path: str | Path) -> "InteractionDB":
        path = Path(path)
        index: Dict[Tuple[str, str], DrugInteraction] = {}
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            required = {"drug_a", "drug_b", "severity", "description"}
            if not required.issubset(reader.fieldnames or set()):
                raise ValueError(f"CSV must contain columns: {sorted(required)}")
            for row in reader:
                di = DrugInteraction(
                    drug_a=row["drug_a"],
                    drug_b=row["drug_b"],
                    severity=row["severity"],
                    description=row["description"],
                )
                index[di.key()] = di
        return cls(index)

    def check_list(self, meds: Iterable[str]) -> List[InteractionHit]:
        meds_norm = [normalize_drug_name(m) for m in meds if m and m.strip()]
        original_map = {normalize_drug_name(m): m for m in meds if m and m.strip()}

        hits: List[InteractionHit] = []
        seen = set()
        for i in range(len(meds_norm)):
            for j in range(i + 1, len(meds_norm)):
                a, b = meds_norm[i], meds_norm[j]
                key = tuple(sorted((a, b)))
                if key in seen:
                    continue
                seen.add(key)
                di = self._index.get(key)
                if di:
                    hits.append(
                        InteractionHit(
                            a=original_map.get(a, di.drug_a),
                            b=original_map.get(b, di.drug_b),
                            severity=di.severity,
                            description=di.description,
                        )
                    )

        severity_order = {"major": 0, "moderate": 1, "minor": 2}
        hits.sort(key=lambda h: (severity_order.get(h.severity.lower(), 99), h.pair_key()))
        return hits
