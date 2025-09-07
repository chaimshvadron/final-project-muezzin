from kafka import KafkaProducer
import json

class KafkaFileMetadataProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                       value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'))
        self.topic = topic

    def send_file_metadata(self, file_metadata: dict):
        try:
            self.producer.send(self.topic, file_metadata)
            self.producer.flush()
        except Exception as e:
            print(f"Failed to send file metadata: {e}")
