from datetime import datetime
from pymongo.collection import Collection
from pymongo.results import BulkWriteResult
from pymongo import UpdateOne
from src.modules.data.auth import MongoDBAuth
from src.modules.data.repository.base_repository import BaseRepository


class MongoDBRepository(BaseRepository):
    """
    MongoDB implementation of the data repository.
    Handles data operations for MongoDB collections.
    """
    
    def __init__(self, mongodb_auth: MongoDBAuth, data_config: dict) -> None:
        """
        Initialize MongoDB repository.
        
        Args:
            mongodb_auth: MongoDB authentication handler
            data_config: Dictionary mapping data entities to their configurations
                         (database and collection names)
        """
        super().__init__(data_config)
        self._mongodb_auth: MongoDBAuth = mongodb_auth
    
    def upsert_rules(self, rules: list[dict]) -> None:
        """
        Upsert rules into MongoDB collection.
        Updates existing rules by id or inserts new ones.
        
        Args:
            rules: List of rule dictionaries to upsert
        """
        # Map rules with updated_at timestamp
        mapped_rules: list[dict] = [
            {
                **rule,
                "id": rule["id"],
                "updated_at": datetime.now()
            }
            for rule in rules
        ]
        
        # Create bulk update operations
        operations: list = [
            UpdateOne(
                {"id": item["id"]},
                {"$set": item},
                upsert=True
            )
            for item in mapped_rules
        ]
        
        # Execute bulk write within authenticated context
        with self._mongodb_auth.authenticate() as client:
            rules_config: dict = self._data_config["rules"]
            database = client[rules_config["database"]]
            collection: Collection = database[rules_config["collection"]]
            result: BulkWriteResult = collection.bulk_write(operations)
    
    def get_rules(self) -> list[dict]:
        """
        Retrieve all rules from the MongoDB collection.
        
        Returns:
            List of rule dictionaries
        """
        # Execute find within authenticated context
        with self._mongodb_auth.authenticate() as client:
            rules_config: dict = self._data_config["rules"]
            database = client[rules_config["database"]]
            collection: Collection = database[rules_config["collection"]]
            
            cursor = collection.find({})
            rules_list: list[dict] = list(cursor)
            
        return rules_list
