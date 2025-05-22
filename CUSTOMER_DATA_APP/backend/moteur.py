from typing import Union



def _get_percentage_change(
    value: Union[int, float], prev_value: Union[int, float]
) -> float:
    """Calculate the percentage change between two values."""
    percentage_change = (
        round(((value - prev_value) / prev_value) * 100, 2)
        if prev_value != 0
        else 0.0
        if value == 0
        else float("inf")
    )
    return percentage_change
