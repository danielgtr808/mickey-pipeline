from abc import ABC, abstractmethod
from typing import Any


class BaseRepository(ABC):
    """
    Abstract base class for all data repositories.
    Defines the common interface that all repositories must implement.
    """
    
    def __init__(self, data_config: dict) -> None:
        """
        Initialize repository with data configuration.
        
        Args:
            data_config: Dictionary mapping data entities to their configurations
        """
        self._data_config: dict = data_config
    
    @abstractmethod
    def upsert_rules(self, rules: list[dict]) -> None:
        """
        Upsert (insert or update) rules data.
        
        Args:
            rules: List of rule dictionaries to upsert
        """
        pass
    
    @abstractmethod
    def get_rules(self) -> list[dict]:
        """
        Retrieve all rules from the data source.
        
        Returns:
            List of rule dictionaries
        """
        pass
