from utils.elastic.elastic_connection import ElasticConnection
from utils.elastic.elastic_dal import ElasticDAL
from services.ThreatDetectionService.detector import Detector
from utils.logger import Logger

import base64
import json

logger = Logger.get_logger(service_name="ThreatDetectionService")

class ThreatDetectionManager:
    def __init__(self, elastic_uri: str, index_name: str, encoded_hostile_words: str, encoded_less_hostile_words: str):
        self.elastic_uri = elastic_uri
        self.index_name = index_name        
        hostile_words = self.decode_word_list(encoded_hostile_words)
        less_hostile_words = self.decode_word_list(encoded_less_hostile_words)      
        self.detector = Detector(hostile_words, less_hostile_words)

    def decode_word_list(self, encoded_list: str):
        try:
            decoded_bytes = base64.b64decode(encoded_list)
            decoded_str = decoded_bytes.decode('utf-8')
            word_list = [w.strip() for w in decoded_str.split(',') if w.strip()]
            return word_list
        except Exception as e:
            logger.error(f"Error decoding word list: {e}")
            raise
            
    def update_threat_analysis(self, elastic_dal, doc_id: str, threat_result: dict):
        elastic_dal.update_document(doc_id, threat_result)
        logger.info(f"Updated document {doc_id} with threat level: {threat_result['bds_threat_level']}")

    def process_threat_detection(self, doc_id: str, transcription: str):
        try:
            with ElasticConnection(self.elastic_uri, logger) as es_client:
                elastic_dal = ElasticDAL(es_client, self.index_name, logger)             
                threat_result = self.detector.detect(transcription)
                self.update_threat_analysis(elastic_dal, doc_id, threat_result)
                logger.info(f"Threat detection processed for document {doc_id}")             
        except Exception as e:
            logger.error(f"Error processing threat detection for document {doc_id}: {e}")
            raise