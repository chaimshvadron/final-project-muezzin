from utils.kafka.consumer_helper import KafkaConsumerManager
from services.Transcription.transcription_manager import TranscriptionManager
from utils.logger import Logger
import os
from dotenv import load_dotenv
load_dotenv()

logger = Logger.get_logger(service_name="Transcription")

def main():
    kafka_server = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic = os.getenv("KAFKA_TOPIC_TRANSCRIPTION")
    group_id = os.getenv("KAFKA_GROUP_ID_TRANSCRIPTION")
    
    consumer_manager = KafkaConsumerManager(kafka_server, group_id, kafka_topic, logger=logger)
    
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db = os.getenv("MONGO_DB")
    mongo_collection = os.getenv("MONGO_COLLECTION")
    elastic_uri = os.getenv("ELASTIC_URI")
    index_name = os.getenv("ELASTIC_INDEX_NAME")

    transcription_manager = TranscriptionManager(mongo_uri, elastic_uri, mongo_db, mongo_collection, index_name)

    for message in consumer_manager.consumer:
        try:
            unique_id = message.value.get('unique_id')
            if unique_id:
                transcription_manager.process_transcription(unique_id)
                logger.info(f"Processed transcription for unique_id: {unique_id}")
            else:
                logger.error("No unique_id found in message.")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            
if __name__ == "__main__":
    main()