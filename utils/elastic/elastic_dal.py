from elasticsearch import Elasticsearch

class ElasticDAL:
    def __init__(self, es_client: Elasticsearch, index_name: str, logger):
        self.es = es_client
        self.index_name = index_name
        self.logger = logger

    def create_index(self, mapping: dict = None):

        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name, mappings=mapping)
                self.logger.info(f"Index '{self.index_name}' created.")
            else:
                self.logger.info(f"Index '{self.index_name}' already exists.")
        except Exception as e:
            self.logger.error(f"Error creating index '{self.index_name}': {e}")
            raise

    def index_document(self, document: dict):

        try:
            response = self.es.index(index=self.index_name, document=document)
            self.logger.info(f"Document indexed in '{self.index_name}': {response.get('_id')}")
            return response
        except Exception as e:
            self.logger.error(f"Error indexing document: {e}")
            raise
