# final-project-muezzin

This project is designed to collect audio files, extract their metadata, and store both the files and metadata in MongoDB and Elasticsearch. It uses Kafka for communication between services.

## Development Decisions

- **Structure**: The project is split into  multiple services for better separation.
- **Technologies**:
	- **Kafka**: Used for reliable, scalable messaging between services.
	- **MongoDB**: Stores files using GridFS, suitable for large binary data.
	- **Elasticsearch**: Indexes metadata for fast search and analytics.
    - **Kibana**: Visualization and exploration of Elasticsearch data.

- **Libraries**:
	- `mutagen` for audio metadata extraction.
	- `kafka-python` for Kafka integration.
	- `pymongo` and `gridfs` for MongoDB.
	- `elasticsearch` for Elasticsearch.
	- `python-dotenv` for environment variable management.
- **Logging**: Centralized logging to Elasticsearch for traceability and monitoring.

