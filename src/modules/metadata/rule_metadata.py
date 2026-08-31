import functools
from typing import Any, Callable, Dict


def rule_metadata(description: str, label: str, params: Dict[str, Any]) -> Callable:
    """
    Decorator that attaches metadata to a rule function.
    
    Args:
        description: Human-readable description of what the rule does
        label: Display label for the rule
        params: Dictionary defining parameters for the rule, where each key is a param ID
                and value is a dict with "label", "operators", and "type"
    
    Returns:
        Decorated function with a 'meta' attribute containing the metadata
    
    Example:
        >>> @rule_metadata(
        ...     description="Check if value is in range",
        ...     label="Range Check",
        ...     params={
        ...         "min_value": {"label": "Minimum", "operators": {">=": None}, "type": "number"},
        ...         "max_value": {"label": "Maximum", "operators": {"<=": None}, "type": "number"}
        ...     }
        ... )
        ... def check_range(value, min_value, max_value):
        ...     return min_value <= value <= max_value
    """
    def decorator(func: Callable) -> Callable:
        # Keeps original function name and docstrings intact
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Attach the metadata dict to the wrapper function
        wrapper.meta = {
            "description": description,
            "label": label,
            "params": params
        }
        return wrapper
    
    return decorator
