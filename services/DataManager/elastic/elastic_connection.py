from elasticsearch import Elasticsearch

class ElasticConnection:
    def __init__(self, uri):
        self.uri = uri
        self.client = None

    def __enter__(self):
        self.client = Elasticsearch(self.uri)
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()
