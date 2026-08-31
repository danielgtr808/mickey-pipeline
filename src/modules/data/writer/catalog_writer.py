from pyspark.sql import DataFrameWriter
from src.modules.data.path_builder import CatalogPathBuilder
from typing import List, Optional


class CatalogWriter:
    def __init__(
        self,
        catalog_path_builder: CatalogPathBuilder,
        data_frame_writer: DataFrameWriter
    ) -> None:
        self._catalog_path_builder: CatalogPathBuilder = catalog_path_builder
        self._data_frame_writer: DataFrameWriter = data_frame_writer

    def option(self, key: str, value) -> 'CatalogWriter':
        self._data_frame_writer = self._data_frame_writer.option(key, value)
        return self

    def options(self, **kwargs) -> 'CatalogWriter':
        self._data_frame_writer = self._data_frame_writer.options(**kwargs)
        return self

    def mode(self, save_mode: str) -> 'CatalogWriter':
        self._data_frame_writer = self._data_frame_writer.mode(save_mode)
        return self

    def save(
        self,
        data_layer: Optional[str] = None,
        data_name: Optional[str] = None,
        data_path: Optional[List[str]] = None
    ) -> None:
        table_name = self._catalog_path_builder.build(
            data_layer = data_layer,
            data_name = data_name,
            data_path = data_path
        )
        self._data_frame_writer.saveAsTable(table_name)