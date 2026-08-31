from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession
from src.modules.data.path_builder import CatalogPathBuilder
from src.modules.data.writer import CatalogWriter
from typing import Optional, List



class CatalogAccess:
    def __init__(
        self,
        spark_session: SparkSession,
        catalog_path_builder: CatalogPathBuilder
    ) -> None:
        self.spark_session: SparkSession = spark_session
        self._catalog_path_builder: CatalogPathBuilder = catalog_path_builder

    def data_exists(
        self,
        data_layer: Optional[str] = None,
        data_name: Optional[str] = None,
        data_path: Optional[List[str]] = None
    ) -> bool:
        table_name: str = self._catalog_path_builder.build(data_layer, data_name, data_path)
        return self.spark_session.catalog.tableExists(table_name)

    def get_data(
        self,
        data_layer: Optional[str] = None,
        data_name: Optional[str] = None,
        data_path: Optional[List[str]] = None
    ) -> DataFrame:
        table_name: str = self._catalog_path_builder.build(data_layer, data_name, data_path)
        return self.spark_session.table(table_name)
    
    def get_data_if_exists(
        self,
        data_layer: Optional[str] = None,
        data_name: Optional[str] = None,
        data_path: Optional[List[str]] = None
    ) -> Optional[DataFrame]:
        exists: bool = self.data_exists(data_layer, data_name, data_path)
        if exists:
            return self.get_data(data_layer, data_name, data_path)
        return None
    
    def get_delta_data(
        self,
        data_layer: Optional[str] = None,
        data_name: Optional[str] = None,
        data_path: Optional[List[str]] = None
    ) -> DeltaTable:
        table_name: str = self._catalog_path_builder.build(data_layer, data_name, data_path)
        return DeltaTable.forName(self.spark_session, table_name)
    
    def write_data(self, data: DataFrame) -> CatalogWriter:
        return CatalogWriter(self._catalog_path_builder, data.write)