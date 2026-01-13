from __future__ import annotations

from dataclasses import dataclass


def normalize_drug_name(name: str) -> str:
    """Normalize a drug name for matching (simple lowercase + strip)."""
    return name.strip().lower()


@dataclass(frozen=True)
class DrugInteraction:
    drug_a: str
    drug_b: str
    severity: str
    description: str

    def key(self) -> tuple[str, str]:
        a = normalize_drug_name(self.drug_a)
        b = normalize_drug_name(self.drug_b)
        return tuple(sorted((a, b)))


@dataclass(frozen=True)
class InteractionHit:
    a: str
    b: str
    severity: str
    description: str

    def pair_key(self) -> tuple[str, str]:
        return tuple(sorted((normalize_drug_name(self.a), normalize_drug_name(self.b))))
