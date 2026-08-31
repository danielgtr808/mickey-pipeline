from typing import Any, Callable, TypedDict


class RuleOperators(TypedDict, total = False):
    """
    Dictionary of operator implementations for rule parameters.
    Each operator is a callable that takes a DataFrame and a value, returning a filtered DataFrame.
    """
    equal: Callable
    not_equal: Callable
    greater_than: Callable
    greater_than_or_equal: Callable
    less_than: Callable
    less_than_or_equal: Callable


class RuleParameterDefinition(TypedDict):
    """
    Complete definition of a rule parameter, including metadata and operator implementations.
    """
    description: str
    name: str
    type: str
    operators: RuleOperators


class RuleParameter(TypedDict):
    """
    A rule parameter instance with its ID, operator, and value.
    Used when applying filters to a DataFrame based on rule metadata.
    """
    id: str
    operator: str
    value: Any
