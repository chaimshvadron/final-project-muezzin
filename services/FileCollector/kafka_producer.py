from utils.logger import Logger
from utils.kafka.producer_helper import KafkaProducerHelper

logger = Logger.get_logger(service_name="FileCollector")

class KafkaFileMetadataProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.topic = topic
        self.kafka_helper = KafkaProducerHelper(bootstrap_servers, logger=logger)

    def send_file_metadata(self, file_metadata: dict):
        self.kafka_helper.send_message(self.topic, file_metadata)
