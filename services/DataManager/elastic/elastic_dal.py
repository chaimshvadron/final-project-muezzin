from elasticsearch import Elasticsearch

class ElasticDAL:
    def __init__(self, es_client: Elasticsearch, index_name: str, mapping: dict):
        self.es = es_client
        self.index_name = index_name
        self.mapping = mapping

    def index_create(self):
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name, mappings=self.mapping)
                print(f"Index '{self.index_name}' created.")
            else:
                print(f"Index '{self.index_name}' already exists.")
        except Exception as e:
            print(f"Error creating index '{self.index_name}': {e}")
            raise
        
    def index_metadata(self, metadata: dict):
        try:
            response = self.es.index(index=self.index_name, document=metadata)
            return response
        except Exception as e:
            print(f"Error indexing metadata: {e}")
            raise