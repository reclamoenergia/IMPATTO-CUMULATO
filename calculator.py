"""Core cumulative-impact math, independent from QGIS APIs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class ImpactComponent:
    """Single weighted component used in cumulative impact."""

    name: str
    value: float
    weight: float = 1.0


class InvalidImpactData(ValueError):
    """Raised when one or more components are invalid."""


def compute_cumulative_impact(components: Sequence[ImpactComponent]) -> float:
    """Return weighted average impact in [0, 1].

    Each component value must already be normalized in [0, 1].
    """
    if not components:
        raise InvalidImpactData("At least one impact component is required.")

    weighted_sum = 0.0
    weight_sum = 0.0

    for component in components:
        if not 0.0 <= component.value <= 1.0:
            raise InvalidImpactData(
                f"Component '{component.name}' has value {component.value}, expected [0, 1]."
            )
        if component.weight < 0.0:
            raise InvalidImpactData(
                f"Component '{component.name}' has negative weight {component.weight}."
            )

        weighted_sum += component.value * component.weight
        weight_sum += component.weight

    if weight_sum <= 0.0:
        raise InvalidImpactData("The total weight must be greater than zero.")

    return weighted_sum / weight_sum


def compute_from_pairs(pairs: Iterable[tuple[str, float, float]]) -> float:
    """Convenience wrapper for UI/table-driven workflows."""
    components = [ImpactComponent(name=n, value=v, weight=w) for n, v, w in pairs]
    return compute_cumulative_impact(components)
