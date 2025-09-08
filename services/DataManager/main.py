from services.DataManager.kafka_consumer import KafkaConsumerManager
from services.DataManager.data_manager import DataManager
import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    kafka_server = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_topic = os.getenv("KAFKA_TOPIC", "files-topic")
    group_id = os.getenv("KAFKA_GROUP_ID", "files-group")
    
    consumer_manager = KafkaConsumerManager(kafka_server, group_id, kafka_topic)
    
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db = os.getenv("MONGO_DB", "files_db")
    elastic_uri = os.getenv("ELASTIC_URI", "http://localhost:9200")
    data_manager = DataManager(mongo_uri, elastic_uri, mongo_db)
    data_manager.create_index()

    for message in consumer_manager.consumer:
        try:
            metadata = message.value.get('metadata')
            path_file = message.value.get('path')
            data_manager.save_document(path_file, metadata)
        except Exception as e:
            print(f"Error processing message: {e}")
