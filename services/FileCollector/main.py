from services.FileCollector.manager import FileCollectorManager
from utils.logger import Logger
import os
from dotenv import load_dotenv
load_dotenv()

logger = Logger.get_logger(service_name="FileCollector")

if __name__ == "__main__":
    logger.info("FileCollector service started.")
    directory_path = os.getenv("DIRECTORY_PATH")
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic = os.getenv("KAFKA_TOPIC")
    manager = FileCollectorManager(directory_path, kafka_bootstrap_servers, kafka_topic)
    manager.process_files()
    logger.info("FileCollector service finished.")