"""
Biomarker normalisation — converts a raw measured value into a deviation
score and a status label relative to a clinical reference range.
"""

from typing import Tuple


def normalize_biomarker(
    value: float,
    ref_low: float,
    ref_high: float,
) -> Tuple[float, str]:
    """
    Normalise a biomarker value against its reference range.

    Args:
        value:    The measured biomarker reading.
        ref_low:  Lower bound of the normal reference range (must be > 0).
        ref_high: Upper bound of the normal reference range (must be > 0
                  and strictly greater than ref_low).

    Returns:
        A ``(deviation, status)`` tuple where:
        - ``deviation`` is 0.0 when the value is within range, or a
          positive fractional distance from the nearer boundary otherwise.
        - ``status`` is one of ``"Normal"``, ``"High"``, or ``"Low"``.

    Raises:
        TypeError:  If any argument is not a numeric type.
        ValueError: If ref_low or ref_high are non-positive, or if
                    ref_low >= ref_high.
    """
    for arg_name, arg_val in (
        ("value", value),
        ("ref_low", ref_low),
        ("ref_high", ref_high),
    ):
        if not isinstance(arg_val, (int, float)):
            raise TypeError(
                f"'{arg_name}' must be numeric, got {type(arg_val).__name__}"
            )

    if ref_low <= 0:
        raise ValueError(f"'ref_low' must be positive, got {ref_low}")
    if ref_high <= 0:
        raise ValueError(f"'ref_high' must be positive, got {ref_high}")
    if ref_low >= ref_high:
        raise ValueError(
            f"'ref_low' ({ref_low}) must be strictly less than 'ref_high' ({ref_high})"
        )

    if ref_low <= value <= ref_high:
        return 0.0, "Normal"

    if value > ref_high:
        deviation = (value - ref_high) / ref_high
        return round(deviation, 3), "High"

    # value < ref_low
    deviation = (ref_low - value) / ref_low
    return round(deviation, 3), "Low"
