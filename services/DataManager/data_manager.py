from utils.elastic.elastic_connection import ElasticConnection
from utils.elastic.elastic_dal import ElasticDAL
from utils.mongo.mongo_connection import MongoDBConnection
from utils.mongo.mongo_dal import MongoDAL
from utils.logger import Logger
from utils.kafka.producer_helper import KafkaProducerHelper
import hashlib

logger = Logger.get_logger(service_name="DataManager")

metadata_mapping = {
    "properties": {
        "unique_id": {"type": "keyword"},
        "name": {"type": "text"},
        "size": {"type": "integer"},
        "last_modified": {"type": "date"},
        "last_accessed": {"type": "date"},
        "creation_time": {"type": "date"},
        "audio_length": {"type": "float"},
        "transcription": {"type": "text"},
        "transcript_status": {"type": "boolean"}
    }
}


class DataManager:
    def __init__(self, mongo_uri: str, elastic_uri: str, mongo_db: str, index_name: str, kafka_bootstrap_servers: str, kafka_topic: str):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.elastic_uri = elastic_uri
        self.index_name = index_name
        self.kafka_topic  = kafka_topic
        self.mongo_dal = None
        self.elastic_dal = None
        self.producer = KafkaProducerHelper(kafka_bootstrap_servers, logger)

    def create_index(self):
        if self.elastic_dal:
            self.elastic_dal.index_create()

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
            self.elastic_dal.index_document(metadata_with_id)


    def save_file_to_mongo(self, file_path: str, metadata_with_id: dict):
        if self.mongo_dal:
            with open(file_path, "rb") as f:
                file_data = f.read()
            unique_id = metadata_with_id.get('unique_id')
            self.mongo_dal.insert_file(file_data, unique_id)


    def save_document(self, file_path: str, metadata: dict, collection_name: str):
        try:
            metadata_with_id = self.build_metadata_with_id(metadata)
            with MongoDBConnection(self.mongo_uri, self.mongo_db, logger) as mongo_db:
                with ElasticConnection(self.elastic_uri, logger) as es_client:
                    self.mongo_dal = MongoDAL(mongo_db, collection_name, logger)
                    self.elastic_dal = ElasticDAL(es_client, self.index_name, logger)
                    self.save_metadata_to_elastic(metadata_with_id)
                    self.save_file_to_mongo(file_path, metadata_with_id)
                    self.producer.send_message(self.kafka_topic, metadata_with_id)
                    logger.info(f"Document for file '{file_path}' saved successfully.")
        except Exception as e:
            logger.error(f"Error saving document for file '{file_path}': {e}")

