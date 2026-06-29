"""Documentation checklist generation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from ..models import Credit


def build_checklist(
    credits: Sequence[Credit],
    statuses: Mapping[str, str],
    saved_records: Mapping[str, Mapping[str, str]] | None = None,
) -> list[dict[str, str]]:
    """Return checklist rows only for credits assessed Yes or Maybe."""

    saved_records = saved_records or {}
    rows: list[dict[str, str]] = []
    for credit in credits:
        assessment = statuses.get(credit.code, "No")
        if assessment not in {"Yes", "Maybe"}:
            continue
        saved = saved_records.get(credit.code, {})
        rows.append(
            {
                "Credit Code": credit.code,
                "Credit Name": credit.name,
                "Assessment": assessment,
                "Required Deliverables": saved.get("Required Deliverables", credit.deliverables),
                "Responsible Party": saved.get("Responsible Party", credit.responsible_party),
                "Status": saved.get("Status", "Not Started"),
            }
        )
    return rows

