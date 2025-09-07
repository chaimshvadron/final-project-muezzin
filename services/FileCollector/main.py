from services.FileCollector.manager import FileCollectorManager
import os
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    directory_path = os.getenv("DIRECTORY_PATH", "./data/podcasts")
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_topic = os.getenv("KAFKA_TOPIC", "files-topic")
    manager = FileCollectorManager(directory_path, kafka_bootstrap_servers, kafka_topic)
    manager.process_files()