from services.FileCollector.collector import FileCollector
from services.FileCollector.metadata import FileMetadataCollector
from utils.kafka.producer_helper import KafkaProducerHelper

from utils.logger import Logger
logger = Logger.get_logger(service_name="FileCollector")

class FileCollectorManager:
    def __init__(self, directory_path: str, kafka_bootstrap_servers: str, kafka_topic: str):
        self.collector = FileCollector(directory_path)
        self.producer = KafkaProducerHelper(kafka_bootstrap_servers, logger)
        self.kafka_topic = kafka_topic

    def process_files(self):
        logger.info("Starting to process files.")
        files = self.collector.collect_files()
        if not files:
            logger.error("No files found to process.")
            return
        for file_path in files:
            metadata_collector = FileMetadataCollector(file_path)
            metadata_dict = metadata_collector.to_dict()
            if metadata_dict:
                message = {
                    "path": file_path,
                    "metadata": metadata_dict
                }
                self.producer.send_message(self.kafka_topic, message)
        logger.info("Finished processing files.")