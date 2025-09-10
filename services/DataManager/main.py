from utils.kafka.consumer_helper import KafkaConsumerManager
from services.DataManager.data_manager import DataManager
import os
from dotenv import load_dotenv
from utils.logger import Logger

logger = Logger.get_logger(service_name="DataManager")

load_dotenv()

if __name__ == "__main__":
    kafka_server = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic = os.getenv("KAFKA_TOPIC")
    kafka_topic_transcription = os.getenv("KAFKA_TOPIC_TRANSCRIPTION")
    kafka_group_id = os.getenv("KAFKA_GROUP_ID")
    consumer_manager = KafkaConsumerManager(kafka_server, kafka_topic, logger=logger, group_id=kafka_group_id)
    
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db = os.getenv("MONGO_DB")
    mongo_collection = os.getenv("MONGO_COLLECTION")
    elastic_uri = os.getenv("ELASTIC_URI")
    index_name = os.getenv("ELASTIC_INDEX_NAME")
    data_manager = DataManager(
        mongo_uri,
        elastic_uri,
        mongo_db,
        index_name,
        kafka_server,
        kafka_topic_transcription
    )
    data_manager.create_index()

    for message in consumer_manager.consumer:
        try:
            metadata = message.value.get('metadata')
            path_file = message.value.get('path')
            data_manager.save_document(path_file, metadata, mongo_collection)
            logger.info(f"Processed message for file: {path_file}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
