from kafka import KafkaConsumer
import os
import json

class KafkaConsumerManager:
    def __init__(self, kafka_server: str, group_id: str, topics: str):
        self.kafka_server = kafka_server
        self.group_id = group_id
        self.topics = topics
        self.consumer = self.get_consumer()

    def get_consumer(self):
        return KafkaConsumer(
            self.topics,
            bootstrap_servers=self.kafka_server,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id=self.group_id
    )
    
