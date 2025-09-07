from services.DataManager.elastic.elastic_connection import ElasticConnection
from services.DataManager.elastic.elastic_dal import ElasticDAL
from services.DataManager.db.mongo_connection import MongoDBConnection
from services.DataManager.db.mongo_dal import MongoDAL
import os
import json
from datetime import datetime

class DataManager:
    def __init__(self, mongo_uri: str, elastic_uri: str, mongo_db: str):
        self.mongo_client =  MongoDBConnection(mongo_uri, mongo_db)
        self.elastic_client = ElasticConnection(elastic_uri)
        self.mongo_dal = MongoDAL(self.mongo_client)
        self.elastic_dal = ElasticDAL(self.elastic_client)

    def return_unique_id(self, metadata: dict):
        name_file = metadata.get("name", "")
        last_modified = metadata.get("last_modified", "")
        return f"{name_file}_{datetime.timestamp(last_modified)}"
    
    