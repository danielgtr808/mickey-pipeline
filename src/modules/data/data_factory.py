from pyspark.sql import SparkSession
from src.modules.data.access import CatalogAccess
from src.modules.data.auth import CatalogAuth, MongoDBAuth
from src.modules.data.path_builder import CatalogPathBuilder
from src.modules.data.repository import BaseRepository, CatalogRepository, MongoDBRepository
from typing import Optional, Union


def data_factory(
    config: dict,
    environment: Optional[str] = None,
    layer_config: Optional[dict[str, str]] = None,
    spark_session: Optional[SparkSession] = None
) -> BaseRepository:
    """
    Factory function to create data repositories.
    
    Args:
        config: Data configuration with _type, auth, and data definitions
        environment: Environment name (e.g., 'dv', 'prod') - required for catalog type
        layer_config: Layer configuration mapping - required for catalog type
        spark_session: Optional SparkSession instance - used for catalog type
    
    Returns:
        BaseRepository: Repository instance for data operations (CatalogRepository or MongoDBRepository)
    
    Raises:
        RuntimeError: If the config type is not supported
        ValueError: If required parameters are missing for a given type
    """
    config_type: str = config.get("_type")
    
    if config_type == "catalog":
        # Validate required parameters for catalog
        if environment is None or layer_config is None:
            raise ValueError("'environment' and 'layer_config' are required for catalog type")
        
        # Get or create auth config (default to catalog type)
        auth_config: dict = config.get("auth", {"_type": "catalog"})
        
        # Create authentication handler
        catalog_auth: CatalogAuth = CatalogAuth(
            auth_config=auth_config,
            spark_session=spark_session
        )
        
        # Create path builder
        path_builder: CatalogPathBuilder = CatalogPathBuilder(
            environment=environment,
            layer_config=layer_config
        )
        
        # Create access layer
        access: CatalogAccess = CatalogAccess(
            catalog_auth=catalog_auth,
            catalog_path_builder=path_builder
        )

        # Create and return repository
        repository: CatalogRepository = CatalogRepository(
            catalog_access=access,
            data_config=config["data"]
        )

        return repository
    
    if config_type == "mongodb":
        # Validate required parameters for mongodb
        if "auth" not in config:
            raise ValueError("'auth' configuration is required for mongodb type")
        
        # Create MongoDB authentication handler
        mongodb_auth: MongoDBAuth = MongoDBAuth(
            auth_config=config["auth"]
        )
        
        # Create and return MongoDB repository (no access or path_builder needed)
        repository: MongoDBRepository = MongoDBRepository(
            mongodb_auth=mongodb_auth,
            data_config=config["data"]
        )
        
        return repository
        
    raise RuntimeError(f'The type "{config_type}" is not supported.')
