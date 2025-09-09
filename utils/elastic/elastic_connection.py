from elasticsearch import Elasticsearch

class ElasticConnection:
    def __init__(self, uri: str, logger):
        self.uri = uri
        self.client = None
        self.logger = logger

    def __enter__(self):
        try:
            self.client = Elasticsearch(self.uri)
            self.logger.info(f"Connected to Elasticsearch: {self.uri}")
            return self.client
        except Exception as e:
            self.logger.error(f"Failed to connect to Elasticsearch: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()
            self.logger.info("Elasticsearch connection closed.")
