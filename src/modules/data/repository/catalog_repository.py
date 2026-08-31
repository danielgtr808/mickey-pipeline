from delta.tables import DeltaTable
from pyspark.sql import DataFrame, Row
from src.modules.data.access import CatalogAccess
from src.modules.data.repository.base_repository import BaseRepository
from typing import Optional


class CatalogRepository(BaseRepository):
    """
    Catalog (Databricks Unity Catalog) implementation of the data repository.
    Handles data operations for Delta tables in Unity Catalog.
    """
    
    def __init__(self, catalog_access: CatalogAccess, data_config: dict) -> None:
        """
        Initialize Catalog repository.
        
        Args:
            catalog_access: Catalog access handler
            data_config: Dictionary mapping data entities to their configurations
                         (data_layer and data_name)
        """
        super().__init__(data_config)
        self._catalog_access: CatalogAccess = catalog_access
    
    def upsert_rules(self, rules: list[dict]) -> None:
        """
        Upsert rules into Delta table.
        Updates existing rules by id or inserts new ones using Delta merge.
        
        Args:
            rules: List of rule dictionaries to upsert
        """
        rules_data_path: dict = self._data_config["rules"]
        
        # Get the schema from existing table
        existing_df: DataFrame = self._catalog_access.get_data(**rules_data_path)
        schema = existing_df.schema
        
        # Create DataFrame with rules using authenticated session
        with self._catalog_access.catalog_auth.authenticate() as spark_session:
            rules_data_frame: DataFrame = spark_session.createDataFrame(
                data=rules,
                schema=schema
            )
        
        # Get delta table and perform merge
        rules_delta_table: DeltaTable = self._catalog_access.get_delta_data(**rules_data_path)
        (
            rules_delta_table.alias("target")
            .merge(
                source=rules_data_frame.alias("source"),
                condition="target.id = source.id"
            )
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute()
        )
    
    def get_rules(self) -> list[dict]:
        """
        Retrieve all rules from the Delta table.
        
        Returns:
            List of rule dictionaries
        """
        rules_data_path: dict = self._data_config["rules"]
        
        # Get the DataFrame from catalog
        rules_df: DataFrame = self._catalog_access.get_data(**rules_data_path)
        
        # Convert DataFrame to list of dictionaries
        rules_rows: list[Row] = rules_df.collect()
        rules_list: list[dict] = [row.asDict() for row in rules_rows]
        
        return rules_list
