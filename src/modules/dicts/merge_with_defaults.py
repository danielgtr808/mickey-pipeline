from typing import Dict, Any
from copy import deepcopy

def merge_with_defaults(default: Dict[str, Any], to_fill: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge default values into to_fill dictionary, preserving existing values.
    
    This function creates a NEW dictionary with all keys from both 'default' and 'to_fill'.
    Keys in 'to_fill' take precedence. For nested dictionaries, the merge is recursive.
    Original dictionaries are NOT modified.
    
    Args:
        default: Dictionary containing default values to apply
        to_fill: Dictionary with values to preserve (takes precedence)
    
    Returns:
        A NEW dictionary with merged values (originals unchanged)
    
    Example:
        >>> defaults = {'a': 1, 'b': 2, 'c': {'x': 10, 'y': 20}}
        >>> config = {'b': 99, 'c': {'y': 999, 'z': 30}, 'd': 4}
        >>> result = merge_with_defaults(defaults, config)
        >>> print(result)
        {'a': 1, 'b': 99, 'c': {'x': 10, 'y': 999, 'z': 30}, 'd': 4}
        >>> print(defaults)  # Original unchanged
        {'a': 1, 'b': 2, 'c': {'x': 10, 'y': 20}}
        >>> print(config)  # Original unchanged
        {'b': 99, 'c': {'y': 999, 'z': 30}, 'd': 4}
        
        # Note: 'b' kept its original value from config (99)
        #       'c' was merged recursively: 'y' kept 999, 'x' added from defaults
        #       'a' was added from defaults
    """
    # Create a new dict starting with a deep copy of defaults
    result = deepcopy(default)
    
    # Recursively merge to_fill into result
    for key, value in to_fill.items():
        if key not in result:
            # Key doesn't exist in defaults, add it from to_fill
            result[key] = deepcopy(value)
        elif isinstance(value, dict) and isinstance(result[key], dict):
            # Both are dicts, merge recursively
            result[key] = merge_with_defaults(result[key], value)
        else:
            # Key exists, to_fill takes precedence
            result[key] = deepcopy(value)
    
    return result
