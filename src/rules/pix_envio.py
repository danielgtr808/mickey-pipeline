from pyspark.sql import DataFrame
from src.modules.data.access import CatalogAccess
from src.modules.metadata import RuleParameter, RuleParameterDefinition, rule_metadata
from typing import Any, Dict, List


params_implementation: Dict[str, RuleParameterDefinition] = {
    "htrans": {
        "description": "Hora em que a transação PIX aconteceu.",
        "name": "Hora transação",
        "type": "timestamp",
        "operators": {
            "equal": lambda df, value: df.where(df["htrans"] == value),
            "not_equal": lambda df, value: df.where(df["htrans"] != value),
            "greater_than": lambda df, value: df.where(df["htrans"] > value),
            "greater_than_or_equal": lambda df, value: df.where(df["htrans"] >= value),
            "less_than": lambda df, value: df.where(df["htrans"] < value),
            "less_than_or_equal": lambda df, value: df.where(df["htrans"] <= value)
        }
    }
}

@rule_metadata(
    description = "Regra para filtrar transações PIX de envio baseado em parâmetros dinâmicos.",
    label = "PIX envio",
    params = params_implementation
)
def pix_envio(
    ca: CatalogAccess,
    rule_parameters: list[RuleParameter]
) -> DataFrame:
    df: DataFrame = catalog_access.get_data(data_path=["subject", "pix", "envio"])

    for param in filters:
        param_id = param["id"]
        operator = param["operator"]
        value = param["value"]
        
        param_impl = params_implementation.get(param_id)
        if param_impl and operator in param_impl["operators"]:
            df = param_impl["operators"][operator](df, value)

    return df
