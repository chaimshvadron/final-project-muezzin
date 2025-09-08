import logging
import os
from elasticsearch import Elasticsearch
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

NAME_LOGGER = os.getenv("NAME_LOGGER")
ES_HOST = os.getenv("ELASTIC_URI")
INDEX_LOGS = os.getenv("INDEX_LOGS")

class Logger:
    _logger = None
    @classmethod
    def get_logger(cls, name=NAME_LOGGER, es_host=ES_HOST, index=INDEX_LOGS, level=logging.DEBUG, service_name="unknown_service"):
        if cls._logger:
            return cls._logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:
            es = Elasticsearch(es_host)
            class ESHandler(logging.Handler):
                def emit(self, record):
                    try:
                        es.index(index=index, document={
                            "timestamp": datetime.utcnow().isoformat(),
                            "level": record.levelname,
                            "logger": record.name,
                            "service": service_name,
                            "message": record.getMessage()
                        })
                    except Exception as e:
                        print(f"ES log failed: {e}")
            logger.addHandler(ESHandler())
            logger.addHandler(logging.StreamHandler())
        cls._logger = logger
        return logger
