"""Pydantic models for electrolyte inventory and formulation plans."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, validator

VIAL_MAX_VOLUME_UL = 1500.0
DEFAULT_BATTERY_ELECTROLYTE_UL = 60.0
DEFAULT_LOW_VOLUME_THRESHOLD_UL = 2 * DEFAULT_BATTERY_ELECTROLYTE_UL
DEFAULT_EMPTY_VOLUME_THRESHOLD_UL = 30.0


class IngredientRequirement(BaseModel):
    """A required stock solution by volume or weight percent."""

    solution_name: str = Field(..., min_length=1)
    volume_ul: Optional[float] = Field(default=None, gt=0)
    weight_percent: Optional[float] = Field(default=None, gt=0, le=100)

    @validator("solution_name")
    def _strip_solution_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value

    @validator("weight_percent", always=True)
    def _validate_weight_or_volume(
        cls, value: Optional[float], values: dict
    ) -> Optional[float]:
        volume_ul = values.get("volume_ul")
        has_volume = volume_ul is not None
        has_weight_percent = value is not None
        if has_volume == has_weight_percent:
            raise ValueError("exactly one of volume_ul or weight_percent must be set")
        if value is None:
            return None
        return float(value)


class FormulationRequest(BaseModel):
    """A recipe request for a target mix."""

    recipe_name: str = Field(..., min_length=1)
    destination: str = Field(default="mix_vessel", min_length=1)
    target_total_volume_ul: Optional[float] = Field(default=None, gt=0)
    ingredients: List[IngredientRequirement] = Field(default_factory=list)

    @validator("recipe_name", "destination")
    def _strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value

    @validator("ingredients")
    def _validate_ingredient_modes(
        cls, ingredients: List[IngredientRequirement], values: dict
    ) -> List[IngredientRequirement]:
        if not ingredients:
            return ingredients

        has_weight = any(item.weight_percent is not None for item in ingredients)
        has_volume = any(item.volume_ul is not None for item in ingredients)
        if has_weight and has_volume:
            raise ValueError("ingredients must be all volume-based or all weight-percent-based")

        target_total_volume_ul = values.get("target_total_volume_ul")
        if has_weight and target_total_volume_ul is None:
            raise ValueError("target_total_volume_ul is required for weight-percent recipes")

        if has_weight:
            total_wt_percent = sum(item.weight_percent or 0.0 for item in ingredients)
            if abs(total_wt_percent - 100.0) > 1e-6:
                raise ValueError("weight_percent values must sum to 100")

        return ingredients


class TransferInstruction(BaseModel):
    """A robot-readable pipetting action."""

    step_index: int = Field(..., ge=1)
    ingredient_name: str = Field(..., min_length=1)
    source_x_ind: int = Field(..., ge=0)
    source_y_ind: int = Field(..., ge=0)
    source_solution: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    volume_ul: float = Field(..., gt=0)

    @validator("ingredient_name", "source_solution", "destination")
    def _strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value


class VialContents(BaseModel):
    """A stock vial that can be consumed across multiple sessions."""

    x_ind: int = Field(..., ge=0)
    y_ind: int = Field(..., ge=0)
    current_solution_name: Optional[str] = None
    previous_solution_name: Optional[str] = None
    current_solution_density_g_per_ml: Optional[float] = Field(default=None, gt=0)
    volume_ul: float = Field(..., ge=0, le=VIAL_MAX_VOLUME_UL)
    capacity_ul: float = Field(default=VIAL_MAX_VOLUME_UL, gt=0, le=VIAL_MAX_VOLUME_UL)
    low_volume_threshold_ul: float = Field(default=DEFAULT_LOW_VOLUME_THRESHOLD_UL, ge=0)

    @validator("current_solution_name", "previous_solution_name", pre=True)
    def _normalize_optional_solution(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @validator("current_solution_density_g_per_ml", always=True)
    def _validate_density_for_current_solution(cls, density: Optional[float], values: dict) -> Optional[float]:
        current_solution = values.get("current_solution_name")
        if current_solution and density is None:
            raise ValueError("current_solution_density_g_per_ml is required when current_solution_name is set")
        if not current_solution and density is not None:
            raise ValueError("current_solution_density_g_per_ml must be null when current_solution_name is null")
        return density

    @validator("low_volume_threshold_ul")
    def _check_threshold(cls, value: float, values: dict) -> float:
        capacity = values.get("capacity_ul", VIAL_MAX_VOLUME_UL)
        if value > capacity:
            raise ValueError("low_volume_threshold_ul must be <= capacity_ul")
        return value


class VialAlert(BaseModel):
    """Machine-readable alert for a vial nearing depletion."""

    x_ind: int = Field(..., ge=0)
    y_ind: int = Field(..., ge=0)
    current_solution_name: Optional[str] = None
    previous_solution_name: Optional[str] = None
    remaining_volume_ul: float = Field(..., ge=0)
    low_volume_flag: bool
    empty_or_unusable_flag: bool


class VialUsageRecord(BaseModel):
    """Volume consumed from a vial during one planned operation."""

    x_ind: int = Field(..., ge=0)
    y_ind: int = Field(..., ge=0)
    solution_name: str = Field(..., min_length=1)
    used_volume_ul: float = Field(..., gt=0)
    remaining_volume_ul: float = Field(..., ge=0)

    @validator("solution_name")
    def _strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value


class FeasibilityIssue(BaseModel):
    """Why a formulation could not be produced."""

    solution_name: str = Field(..., min_length=1)
    required_volume_ul: float = Field(..., ge=0)
    available_volume_ul: float = Field(..., ge=0)
    deficit_volume_ul: float = Field(..., ge=0)

    @validator("solution_name")
    def _strip_solution_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value


class FormulationPlan(BaseModel):
    """Feasibility result and the instructions to execute it."""

    feasible: bool
    recipe_name: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    total_required_volume_ul: float = Field(..., ge=0)
    instructions: List[TransferInstruction] = Field(default_factory=list)
    issues: List[FeasibilityIssue] = Field(default_factory=list)
    low_volume_flag: bool = False
    vial_alerts: List[VialAlert] = Field(default_factory=list)
    vial_usage: List[VialUsageRecord] = Field(default_factory=list)

    @validator("recipe_name", "destination")
    def _strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value


class Inventory(BaseModel):
    """A vial inventory with unique x_ind/y_ind coordinates."""

    vials: List[VialContents] = Field(default_factory=list)

    @validator("vials")
    def _check_unique_vials(cls, vials: List[VialContents]) -> List[VialContents]:
        seen = set()
        for vial in vials:
            key = (vial.x_ind, vial.y_ind)
            if key in seen:
                raise ValueError(
                    f"duplicate vial coordinates: x_ind={vial.x_ind}, y_ind={vial.y_ind}"
                )
            seen.add(key)
        return vials

    def available_volume(self, solution_name: str) -> float:
        return sum(
            vial.volume_ul
            for vial in self.vials
            if vial.current_solution_name == solution_name
        )

    def vials_for_solution(self, solution_name: str) -> List[VialContents]:
        return [
            vial for vial in self.vials if vial.current_solution_name == solution_name
        ]

    def density_for_solution(self, solution_name: str) -> float:
        matching = self.vials_for_solution(solution_name)
        if not matching:
            raise KeyError(f"No vial found for solution: {solution_name}")

        densities = {vial.current_solution_density_g_per_ml for vial in matching}
        if None in densities:
            raise ValueError(
                f"Density missing on one or more vials for solution: {solution_name}"
            )
        if len(densities) != 1:
            raise ValueError(
                f"Inconsistent densities across vials for solution: {solution_name}"
            )
        return list(densities)[0]  # guaranteed single item