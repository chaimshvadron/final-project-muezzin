import os
from dotenv import load_dotenv
from utils.kafka.consumer_helper import KafkaConsumerManager
from services.ThreatDetectionService.manager import ThreatDetectionManager
from utils.logger import Logger
load_dotenv()

logger = Logger.get_logger(service_name="ThreatDetectionService")

def main():
	kafka_server = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
	kafka_topic_detection = os.getenv("KAFKA_TOPIC_DETECTION")
	kafka_group_id = os.getenv("KAFKA_GROUP_ID")
	consumer_manager = KafkaConsumerManager(kafka_server, kafka_topic_detection, logger=logger, group_id=kafka_group_id)

	elastic_uri = os.getenv("ELASTIC_URI")
	index_name = os.getenv("ELASTIC_INDEX_NAME")
	encoded_hostile_words = os.getenv("ENCODED_HOSTILE_WORDS")
	encoded_less_hostile_words = os.getenv("ENCODED_LESS_HOSTILE_WORDS")

	threat_manager = ThreatDetectionManager(elastic_uri, index_name, encoded_hostile_words, encoded_less_hostile_words)

	for message in consumer_manager.consumer:
		try:
			doc_id = message.value.get('id_doc')
			transcription = message.value.get('transcription')
			if doc_id and transcription:
				threat_manager.process_threat_detection(doc_id, transcription)
				logger.info(f"Processed threat detection for doc_id: {doc_id}")
			else:
				logger.error(f"Missing doc_id or transcription in message: {message.value}")
		except Exception as e:
			logger.error(f"Error processing message: {e}")

if __name__ == "__main__":
	main()
