"""Scorecard calculations and certification forecasting."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from ..data import CERTIFICATION_THRESHOLDS
from ..models import AssessmentStatus, CertificationResult, Credit


def score_assessment(
    credits: Sequence[Credit], statuses: Mapping[str, AssessmentStatus | str]
) -> tuple[int, int]:
    """Return committed (Yes) and potential (Maybe) points."""

    yes_points = sum(c.points for c in credits if statuses.get(c.code, "No") == "Yes")
    maybe_points = sum(c.points for c in credits if statuses.get(c.code, "No") == "Maybe")
    return yes_points, maybe_points


def level_for_points(points: int) -> str:
    if points >= CERTIFICATION_THRESHOLDS["Platinum"]:
        return "Platinum"
    if points >= CERTIFICATION_THRESHOLDS["Gold"]:
        return "Gold"
    if points >= CERTIFICATION_THRESHOLDS["Silver"]:
        return "Silver"
    if points >= CERTIFICATION_THRESHOLDS["Certified"]:
        return "Certified"
    return "Not Certified"


def calculate_certification(yes_points: int, maybe_points: int) -> CertificationResult:
    """Calculate a pipeline projection using Yes + Maybe points."""

    projected = min(110, yes_points + maybe_points)
    level = level_for_points(projected)
    next_level: str | None = None
    points_to_next = 0
    for candidate, threshold in CERTIFICATION_THRESHOLDS.items():
        if projected < threshold:
            next_level = candidate
            points_to_next = threshold - projected
            break
    return CertificationResult(
        yes_points=yes_points,
        maybe_points=maybe_points,
        projected_points=projected,
        level=level,
        next_level=next_level,
        points_to_next=points_to_next,
    )


def category_scores(
    credits: Sequence[Credit], statuses: Mapping[str, AssessmentStatus | str]
) -> list[dict[str, int | str]]:
    """Aggregate points by credit category for progress visualization."""

    ordered_categories: list[str] = []
    result: dict[str, dict[str, int | str]] = {}
    for credit in credits:
        if credit.category not in result:
            ordered_categories.append(credit.category)
            result[credit.category] = {
                "Category": credit.category,
                "Yes": 0,
                "Maybe": 0,
                "Available": 0,
            }
        row = result[credit.category]
        row["Available"] = int(row["Available"]) + credit.points
        status = statuses.get(credit.code, "No")
        if status in ("Yes", "Maybe"):
            row[str(status)] = int(row[str(status)]) + credit.points
    return [result[name] for name in ordered_categories]

