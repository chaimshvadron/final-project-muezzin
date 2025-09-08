from services.FileCollector.collector import FileCollector
from services.FileCollector.metadata import FileMetadataCollector
from services.FileCollector.kafka_producer import KafkaFileMetadataProducer

class FileCollectorManager:
    def __init__(self, directory_path: str, kafka_bootstrap_servers: str, kafka_topic: str):
        self.collector = FileCollector(directory_path)
        self.producer = KafkaFileMetadataProducer(kafka_bootstrap_servers, kafka_topic)

    def process_files(self):
        files = self.collector.collect_files()
        for file_path in files:
            metadata_collector = FileMetadataCollector(file_path)
            metadata_dict = metadata_collector.to_dict()
            if metadata_dict:
                message = {
                    "path": file_path,
                    "metadata": metadata_dict
                }
                self.producer.send_file_metadata(message)