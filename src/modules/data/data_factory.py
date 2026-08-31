from pyspark.sql import SparkSession
from src.modules.data.access import CatalogAccess
from src.modules.data.path_builder import CatalogPathBuilder
from src.modules.data.repository import CatalogRepository
from typing import Optional



def data_factory(
    config: dict,
    environment: str,
    layer_config: dict[str, str],
    spark_session: Optional[SparkSession] = None
) -> tuple[CatalogAccess, CatalogRepository]:
    config_type: str = config["_type"]
    
    if (config_type == "catalog"):
        path_builder: CatalogPathBuilder = CatalogPathBuilder(
            environment = environment,
            layer_config = layer_config
        )
        
        access: CatalogAccess = CatalogAccess(
            spark_session = spark_session,
            catalog_path_builder = path_builder
        )

        repository: CatalogRepository = CatalogRepository(
            catalog_access = access,
            data_config = config["data"]
        )

        return (access, repository)
        
    raise RuntimeError(f"The type \"{config_type}\" is not supported.")