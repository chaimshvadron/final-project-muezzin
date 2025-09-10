from kafka import KafkaProducer
import json
import time

class KafkaProducerHelper:

    def __init__(self, bootstrap_servers: str, logger):
        self.logger = logger
        self.producer = self._wait_for_kafka(bootstrap_servers)

    def _wait_for_kafka(self, bootstrap_servers):
        while True:
            try:
                producer = KafkaProducer(
                    bootstrap_servers=bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
                )
                return producer
            except Exception as e:
                time.sleep(5)

    def send_message(self, topic: str, value: dict):
        try:
            self.producer.send(topic, value)
            self.producer.flush()
            self.logger.info(f"Sent message to topic {topic}: {value}")
        except Exception as e:
            self.logger.error(f"Failed to send message to topic {topic}: {e}")

