from kafka import KafkaConsumer
import json
from utils.logger import Logger



class KafkaConsumerManager:
    def __init__(self, kafka_server: str, group_id: str, topics: str, logger):
        self.kafka_server = kafka_server
        self.group_id = group_id
        self.topics = topics
        self.logger = logger
        self.consumer = self.get_consumer()

    def get_consumer(self):
        try:
            consumer = KafkaConsumer(
                self.topics,
                bootstrap_servers=self.kafka_server,
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True
            )
            self.logger.info(f"Kafka consumer created for topics: {self.topics}")
            return consumer
        except Exception as e:
            self.logger.error(f"Error creating Kafka consumer: {e}")
            raise
    