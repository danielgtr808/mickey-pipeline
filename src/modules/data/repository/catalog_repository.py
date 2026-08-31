from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession, functions as f
from src.modules.data.access import CatalogAccess
from typing import Optional


class CatalogRepository:    
    def __init__(self, catalog_access: CatalogAccess, data_config: dict) -> None:
        self._catalog_access = catalog_access
        self._data_config = data_config
    
    def upsert_rules(self, rules: list[dict]) -> None:
        rules_data_path: dict = self._data_config["rules"]
        rules_data_frame: DataFrame = (
            self
            ._catalog_access
            .spark_session
            .createDataFrame(
                data = rules,
                schema = self._catalog_access.get_data(**rules_data_path).schema
            )
        )

        rules_delta_table: DeltaTable = self._catalog_access.get_delta_data(**rules_data_path)
        (
            rules_delta_table.alias("target")
            .merge(
                source = rules_data_frame.alias("source"),
                condition = "target.id = source.id"
            )
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute()
        )
