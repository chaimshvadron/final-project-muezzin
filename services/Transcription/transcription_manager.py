import os

from utils.elastic.elastic_connection import ElasticConnection
from utils.elastic.elastic_dal import ElasticDAL
from utils.mongo.mongo_connection import MongoDBConnection
from utils.mongo.mongo_dal import MongoDAL
from utils.logger import Logger
from services.Transcription.transcriber import Transcriber
from utils.logger import Logger
import tempfile

logger = Logger.get_logger(service_name="Transcription")

class TranscriptionManager:
    def __init__(self, mongo_uri: str, elastic_uri: str, mongo_db: str, collection_name: str, index_name: str = "files_index"):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name
        self.elastic_uri = elastic_uri
        self.index_name = index_name
        self.mongo_dal = None
        self.elastic_dal = None
        self.transcriber = Transcriber(model_size="small", device="cpu", compute_type="float32")

    def transcribe_audio(self, audio_file_path: str):
        return self.transcriber.transcribe(audio_file_path)

    def fetch_and_save_temp_file(self, mongo_dal, unique_id: str):
        file_data = mongo_dal.get_file_by_unique_id(unique_id)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(file_data)
            logger.info(f"Temporary file saved: {temp_file.name}")
            return temp_file.name
        
    def save_transcription(self, elastic_dal, id_doc: str, transcription: str):
        document = {
            "transcript_status": True,
            "transcription": transcription
        }
        elastic_dal.update_document(id_doc, document)
        logger.info(f"Transcription updated for id_doc: {id_doc}")

    def get_id_by_unique_id(self, elastic_dal, unique_id: str):
        query = {
            "term": {
                "unique_id": unique_id
            }
        }
        return elastic_dal.get_id_by_search(query)
        
    def process_transcription(self, unique_id: str):
        try:
            with MongoDBConnection(self.mongo_uri, self.mongo_db, logger) as mongo_db:
                with ElasticConnection(self.elastic_uri, logger) as es_client:
                    mongo_dal = MongoDAL(mongo_db, self.collection_name, logger)
                    elastic_dal = ElasticDAL(es_client, self.index_name, logger)
                    id_doc = self.get_id_by_unique_id(elastic_dal, unique_id)
                    temp_file_path = self.fetch_and_save_temp_file(mongo_dal, unique_id)
                    transcription = self.transcribe_audio(temp_file_path)
                    self.save_transcription(elastic_dal, id_doc, transcription)
                    logger.info(f"Transcription process completed for unique_id: {unique_id}")
        except Exception as e:
            logger.error(f"Error in transcription process for unique_id {unique_id}: {e}")
        finally:
            os.remove(temp_file_path)

if __name__ == "__main__":
    mongo_uri = os.getenv("MONGO_URI")
    elastic_uri = os.getenv("ELASTIC_URI")
    mongo_db = os.getenv("MONGO_DB")
    collection_name = os.getenv("MONGO_COLLECTION")
    unique_id = "aa2c71cc4b5ff2e42db3cbe2575f87a1b022fea1d1a8ff7a0e310cb722c99bec"
    manager = TranscriptionManager(mongo_uri, elastic_uri, mongo_db, collection_name)
    manager.process_transcription(unique_id)
    
