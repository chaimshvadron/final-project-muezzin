from pymongo import MongoClient
from utils.logger import Logger

logger = Logger.get_logger(service_name="DataManager")

class MongoDBConnection:
    def __init__(self, connection_string, db_name):
        self.connection_string = connection_string
        self.db_name = db_name  
        self.client = None
        self.db = None

    def __enter__(self):
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.db_name]
            logger.info(f"Connected to MongoDB, DB: {self.db_name}")
            return self
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")