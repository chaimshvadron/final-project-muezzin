from kafka import KafkaConsumer
import json
from utils.logger import Logger



class KafkaConsumerManager:
    def __init__(self, kafka_server: str, topics: str, logger, group_id: str = "main-consumer-group"):
        self.kafka_server = kafka_server
        self.topics = topics
        self.logger = logger
        self.group_id = group_id
        self.consumer = self.get_consumer()

    def get_consumer(self):
        try:
            consumer = KafkaConsumer(
                self.topics,
                bootstrap_servers=self.kafka_server,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id=self.group_id
            )
            self.logger.info(f"Kafka consumer created for topics: {self.topics}")
            return consumer
        except Exception as e:
            self.logger.error(f"Error creating Kafka consumer: {e}")
            raise
    