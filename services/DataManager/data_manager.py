from services.DataManager.elastic.elastic_connection import ElasticConnection
from services.DataManager.elastic.elastic_dal import ElasticDAL
from services.DataManager.db.mongo_connection import MongoDBConnection
from services.DataManager.db.mongo_dal import MongoDAL
import hashlib

metadata_mapping = {
    "properties": {
        "name": {"type": "text"},
        "size": {"type": "integer"},
        "last_modified": {"type": "date"},
        "last_accessed": {"type": "date"},
        "creation_time": {"type": "date"},
        "audio_length": {"type": "float"},
        "unique_id": {"type": "keyword"}
    }
}

class DataManager:
    def __init__(self, mongo_uri: str, elastic_uri: str, mongo_db: str, index_name: str = "files_index"):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.elastic_uri = elastic_uri
        self.index_name = index_name
        self.mongo_dal = None
        self.elastic_dal = None


    def create_index(self):
        if self.elastic_dal:
            try:
                self.elastic_dal.index_create()
            except Exception as e:
                print(f"Error creating Elasticsearch index: {e}")


    def calculate_unique_id(self, metadata: dict):
        name = str(metadata.get('name', ''))
        size = str(metadata.get('size', ''))
        creation_time = str(metadata.get('creation_time', ''))
        combined = f"{name}_{size}_{creation_time}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    def build_metadata_with_id(self, metadata: dict):
        metadata['unique_id'] = self.calculate_unique_id(metadata)
        return metadata

    def save_metadata_to_elastic(self, metadata_with_id: dict):
        if self.elastic_dal:
            try:
                self.elastic_dal.index_metadata(metadata_with_id)
            except Exception as e:
                print(f"Error saving metadata to Elasticsearch: {e}")
        else:
            print("ElasticDAL is not initialized.")

    def save_file_to_mongo(self, file_path: str, metadata_with_id: dict):
        if self.mongo_dal:
            try:
                unique_id = metadata_with_id.get('unique_id')
                self.mongo_dal.insert_file(file_path, unique_id, {'unique_id': unique_id})
            except Exception as e:
                print(f"Error saving file to MongoDB: {e}")
        else:
            print("MongoDAL is not initialized.")

    def save_document(self, file_path: str, metadata: dict):
        metadata_with_id = self.build_metadata_with_id(metadata)
        with MongoDBConnection(self.mongo_uri, self.mongo_db) as mongo_db, ElasticConnection(self.elastic_uri) as es_client:
            self.mongo_dal = MongoDAL(mongo_db)
            self.elastic_dal = ElasticDAL(es_client, self.index_name)
            self.save_metadata_to_elastic(metadata_with_id)
            self.save_file_to_mongo(file_path, metadata_with_id)

