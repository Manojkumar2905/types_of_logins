from typing import Optional

from pymongo import MongoClient

from constants.config import settings


class BaseDatabaseConnection:
    _client: Optional[MongoClient] = None

    @classmethod
    def _initialize_client(cls):
        if cls._client is None:
            cls._client = MongoClient(settings.FIRSTOCK_MONGODB_CREDENTIALS, tls=True,
                                      tlsAllowInvalidCertificates=True)
        return cls._client

    @classmethod
    def get_client(cls) -> MongoClient:
        return cls._initialize_client()

    @classmethod
    def close_connection(cls):
        if cls._client:
            cls._client.close()
            cls._client = None


class ClientConnection(BaseDatabaseConnection):
    _database = None
    _default_collection = None

    @classmethod
    def connect(cls):
        if cls._database is None:
            cls._initialize_client()
            cls._database = cls._client[settings.CLIENT_DB]
            cls._default_collection = cls._database[settings.CLIENT_DETAILS]

        return cls._database

    @classmethod
    def get_database(cls):
        return cls.connect()

    @classmethod
    def get_collection(cls, collection_name: str = None):
        cls.connect()
        if collection_name:
            return cls._database[collection_name]
        return cls._default_collection