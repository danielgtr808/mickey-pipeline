from typing import Any, Callable, Dict, List, Optional


def extract_rule_metadata(func: Callable, name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Extract metadata from a function decorated with @rule_metadata.
    
    Args:
        func: Function to extract metadata from
        name: Optional name to use as fallback for id/label (defaults to func.__name__)
    
    Returns:
        Dictionary with extracted metadata structure, or None if no metadata found
        Structure: {"id": str, "label": str, "params": [{"id": str, "label": str, "operators": List[str], "type": str}]}
    
    Example:
        >>> @rule_metadata(description="Test", label="Test Rule", params={"val": {"label": "Value", "operators": {"==": None}, "type": "string"}})
        ... def my_rule(val):
        ...     return True
        >>> extract_rule_metadata(my_rule)
        {'id': 'my_rule', 'label': 'Test Rule', 'params': [{'id': 'val', 'label': 'Value', 'operators': ['=='], 'type': 'string'}]}
    """
    if name is None:
        name = func.__name__
    
    meta = getattr(func, "meta", None)
    if meta is None:
        print(f"# {name} — no 'meta' attribute, skipping")
        return None
    
    # Ensure meta has the expected keys; if it's already a dict, use it directly
    entry = {
        "description": meta.get("description", name),
        "id": meta.get("id", name),
        "label": meta.get("label", name),
        "params": []
    }

    for param_id, param_definition in meta["params"].items():
        entry["params"].append({
            "description": param_definition.get("description"),
            "id": param_id,
            "label": param_definition.get("label", param_id),
            "operators": list(param_definition.get("operators", {}).keys()),
            "type": param_definition.get("type", "string")
        })

    return entry
