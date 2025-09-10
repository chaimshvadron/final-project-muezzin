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

    def refresh_index(self):
        self.es.indices.refresh(index=self.index_name)


    def index_document(self, document: dict):
        try:
            response = self.es.index(index=self.index_name, document=document)
            self.logger.info(f"Document indexed in '{self.index_name}': {response.get('_id')}")
            return response
        except Exception as e:
            self.logger.error(f"Error indexing document: {e}")
            raise
        
    def get_id_by_search(self, query: dict):
        try:
            self.refresh_index()
            response = self.es.search(index=self.index_name, query=query)
            self.logger.info(f"Search executed on '{self.index_name}'.")
            hits = response.get('hits', {}).get('hits', [])
            if hits:
                doc_id = hits[0].get('_id')
                return doc_id
            return None
        except Exception as e:
            self.logger.error(f"Error executing search: {e}")
            raise
        
    def search_documents(self, query: dict, size: int = 10):
        """General search function that returns all matching documents."""
        try:
            self.refresh_index()
            response = self.es.search(index=self.index_name, query=query, size=size)
            self.logger.info(f"Search executed on '{self.index_name}', found {response['hits']['total']['value']} results.")
            return response
        except Exception as e:
            self.logger.error(f"Error executing search: {e}")
            raise
        
    def update_document(self, doc_id: str, update_fields: dict):
        try:
            self.refresh_index()
            response = self.es.update(index=self.index_name, id=doc_id, doc=update_fields)
            self.logger.info(f"Document '{doc_id}' updated in '{self.index_name}'.")
            return response
        except Exception as e:
            self.logger.error(f"Error updating document '{doc_id}': {e}")
            raise