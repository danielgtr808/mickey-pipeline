from typing import Optional
from contextlib import contextmanager
from pymongo import MongoClient
from pymongo.database import Database


class MongoDBAuth:
    """
    Authentication handler for MongoDB access.
    Manages MongoDB client connections using context manager pattern.
    """
    
    def __init__(self, auth_config: dict) -> None:
        """
        Initialize MongoDBAuth.
        
        Args:
            auth_config: Authentication configuration dict with:
                - _type: 'explicit' or 'connection_string'
                - For explicit: host, username, password
                - For connection_string: connection_string
        """
        self._auth_config: dict = auth_config
        self._auth_type: str = auth_config.get("_type")
        self._connection_string: str = self._build_connection_string()
    
    def _build_connection_string(self) -> str:
        """Build MongoDB connection string based on auth type."""
        if self._auth_type == "explicit":
            username = self._auth_config["username"]
            password = self._auth_config["password"]
            host = self._auth_config["host"]
            return f"mongodb+srv://{username}:{password}@{host}/"
        elif self._auth_type == "connection_string":
            return self._auth_config["connection_string"]
        else:
            raise ValueError(f"Unsupported auth type: {self._auth_type}")
    
    @contextmanager
    def authenticate(self):
        """
        Context manager for authenticated MongoDB operations.
        Opens connection on enter, closes on exit.
        
        Yields:
            MongoClient: Active MongoDB client
        """
        client = None
        try:
            # Create new client connection
            client = MongoClient(self._connection_string)
            # Test connection
            client.admin.command('ping')
            yield client
        finally:
            # Always close the connection
            if client is not None:
                client.close()
    
