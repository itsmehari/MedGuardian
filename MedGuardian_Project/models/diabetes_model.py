"""
Diabetes risk scoring model.

Produces a risk score on a 0.0 – 1.0 scale from four clinical inputs.
The formula is a weighted linear combination; weights are derived from
the relative predictive importance documented in ADA risk-assessment
literature (glucose and HbA1c carry the majority of the signal).
"""


def calculate_diabetes_risk(
    glucose_dev: float,
    hba1c_dev: float,
    bmi: float,
    family_history: int,
) -> float:
    """
    Calculate a diabetes risk score on a 0.0 – 1.0 scale.

    Args:
        glucose_dev:    Fractional deviation of fasting glucose above its
                        normal upper limit (>= 0). Use
                        ``normalize_biomarker`` to produce this value.
        hba1c_dev:      Fractional deviation of HbA1c above its normal
                        upper limit (>= 0).
        bmi:            Patient's Body Mass Index (must be > 0).
        family_history: ``1`` if a first-degree relative has been
                        diagnosed with diabetes, ``0`` otherwise.

    Returns:
        Risk score rounded to 3 decimal places, capped at 1.0.
        Interpretation guide:
          0.00 – 0.20  Low risk
          0.21 – 0.50  Moderate risk
          0.51 – 1.00  High risk

    Raises:
        TypeError:  If glucose_dev, hba1c_dev, or bmi are not numeric.
        ValueError: If bmi <= 0, glucose_dev or hba1c_dev are negative,
                    or family_history is not 0 or 1.
    """
    for arg_name, arg_val in (
        ("glucose_dev", glucose_dev),
        ("hba1c_dev", hba1c_dev),
        ("bmi", bmi),
    ):
        if not isinstance(arg_val, (int, float)):
            raise TypeError(
                f"'{arg_name}' must be numeric, got {type(arg_val).__name__}"
            )

    if not isinstance(family_history, int) or family_history not in (0, 1):
        raise ValueError(
            f"'family_history' must be 0 or 1, got {family_history!r}"
        )
    if bmi <= 0:
        raise ValueError(f"'bmi' must be a positive number, got {bmi}")
    if glucose_dev < 0:
        raise ValueError(f"'glucose_dev' must be non-negative, got {glucose_dev}")
    if hba1c_dev < 0:
        raise ValueError(f"'hba1c_dev' must be non-negative, got {hba1c_dev}")

    weight_glucose = 0.4
    weight_hba1c = 0.4
    weight_bmi = 0.1
    weight_family = 0.1

    # Continuous BMI modifier: 0.0 at the healthy lower bound (18.5),
    # scaling linearly to 1.0 at severe-obesity threshold (40.0).
    # Clamped to [0.0, 1.0] so values outside that range don't distort
    # the overall score disproportionately.
    bmi_modifier = min(max((bmi - 18.5) / (40.0 - 18.5), 0.0), 1.0)

    score = (
        weight_glucose * glucose_dev
        + weight_hba1c * hba1c_dev
        + weight_bmi * bmi_modifier
        + weight_family * family_history
    )

    return round(min(score, 1.0), 3)
