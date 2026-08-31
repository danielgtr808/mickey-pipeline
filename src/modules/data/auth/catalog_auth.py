from pyspark.sql import SparkSession
from typing import Optional
from contextlib import contextmanager


class CatalogAuth:    
    def __init__(
        self,
        auth_config: dict,
        spark_session: Optional[SparkSession] = None
    ) -> None:
        self._auth_config: dict = auth_config
        self._spark_session: Optional[SparkSession] = spark_session
        self._auth_type: str = auth_config.get("_type", "catalog")
    
    @contextmanager
    def authenticate(self):
        # Get or create SparkSession
        if self._spark_session is None:
            self._spark_session = SparkSession.builder.getOrCreate()
        
        try:
            # For catalog type, we don't need to open/close connections
            # We're already authenticated in Databricks
            yield self._spark_session
        finally:
            # For catalog type, we don't close the connection
            # Future auth types (mongodb, etc.) will implement cleanup here
            pass
    
    @property
    def spark_session(self) -> SparkSession:
        """Get the current SparkSession (creates one if needed)"""
        if self._spark_session is None:
            self._spark_session = SparkSession.builder.getOrCreate()
        return self._spark_session
