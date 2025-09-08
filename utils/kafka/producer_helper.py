from kafka import KafkaProducer
import json

class KafkaProducerHelper:

    def __init__(self, bootstrap_servers: str, logger):
        self.logger = logger
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
        )

    def send_message(self, topic: str, value: dict):
        try:
            self.producer.send(topic, value)
            self.producer.flush()
            self.logger.info(f"Sent message to topic {topic}: {value}")
        except Exception as e:
            self.logger.error(f"Failed to send message to topic {topic}: {e}")
