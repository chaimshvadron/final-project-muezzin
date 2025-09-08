from kafka import KafkaProducer
import json
from utils.logger import Logger

logger = Logger.get_logger(service_name="FileCollector")

class KafkaFileMetadataProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                       value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'))
        self.topic = topic

    def send_file_metadata(self, file_metadata: dict):
        try:
            self.producer.send(self.topic, file_metadata)
            self.producer.flush()
            logger.info(f"Sent file metadata to topic {self.topic}: {file_metadata}")
        except Exception as e:
            logger.error(f"Failed to send file metadata: {e}")
