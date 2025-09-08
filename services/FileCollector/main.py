from services.FileCollector.manager import FileCollectorManager
import os
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    directory_path = os.getenv("DIRECTORY_PATH")
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic = os.getenv("KAFKA_TOPIC")
    manager = FileCollectorManager(directory_path, kafka_bootstrap_servers, kafka_topic)
    manager.process_files()