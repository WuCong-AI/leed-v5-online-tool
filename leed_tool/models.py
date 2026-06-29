"""Typed domain models shared by the LEED v5 application modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

AssessmentStatus = Literal["Yes", "Maybe", "No"]
RiskLevel = Literal["Low", "Medium", "High"]


@dataclass(frozen=True, slots=True)
class ProjectProfile:
    """Project inputs used to tailor planning outputs."""

    name: str
    gross_floor_area_m2: float
    location: str
    project_type: str
    target_level: str


@dataclass(frozen=True, slots=True)
class Prerequisite:
    code: str
    category: str
    name: str
    pillar: str
    applicability: tuple[str, ...] = ("BD+C", "ID+C")
    summary: str = ""


@dataclass(frozen=True, slots=True)
class Credit:
    code: str
    category: str
    name: str
    points: int
    pillar: str
    deliverables: str
    responsible_party: str
    applicability: tuple[str, ...] = ("BD+C", "ID+C")
    strategy: str = ""
    platinum_gate: bool = False


@dataclass(frozen=True, slots=True)
class CertificationResult:
    yes_points: int
    maybe_points: int
    projected_points: int
    level: str
    next_level: str | None
    points_to_next: int


@dataclass(frozen=True, slots=True)
class ReviewFinding:
    criterion: str
    severity: str
    title: str
    evidence: str
    drawing_comment: str
    status: str = "Issue"


@dataclass(frozen=True, slots=True)
class RiskAssessment:
    level: RiskLevel
    score: int
    evidence_coverage: int
    strengths: tuple[str, ...] = field(default_factory=tuple)
    flags: tuple[str, ...] = field(default_factory=tuple)
    corrective_actions: tuple[str, ...] = field(default_factory=tuple)

