from pymongo import MongoClient

from chapter_2.interfaces.client_interface import ClientInterface


class MongoDBClient(ClientInterface):
    def __init__(self, uri='mongodb://localhost:27017/'):
        self._uri = uri
        self._client = None

    def connect(self):
        if self._client is None:
            self._client = MongoClient(self._uri)
        return self._client

    def close(self):
        if self._client is not None:
            self._client.close()
            self._client = None