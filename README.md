# final-project-muezzin

This project analyzes audio files (podcasts) through 4 microservices that process files sequentially using Kafka for communication.

## Connection Management
Used `with` statements for MongoDB and Elasticsearch to manage connections securely and ensure they close properly.

## Logging Management
- `try` and `except` in all relevant services
- Created logger that updates in Elasticsearch automatically
- Logger receives additional `service_name` parameter to identify which service sent the log message

## Code Organization
Services like kafka, elastic, and mongo are located in `utils` subdirectory to avoid code duplication. These are imported in relevant Dockerfiles.

## Environment Variables
Environment variables are managed centrally and must be configured in compose file accordingly.

## Responsibility Management
Clear responsibility management and proper class division.

## Connection Mechanism
Kafka and Elasticsearch have mechanism to check connection - if it fails, it waits and tries to connect again.

## Entry Point
In each service, `main` is the entry point where environment variables are defined and service is started.

## Development Decisions for 4 Services

### 1. FileCollector
Service scans specific directory, extracts metadata and sends to Kafka.

**Metadata**: Using `os` to get relevant metadata:
- File size
- File creation time
- File modification time
- Last access time
- Audio length - important to know audio duration, using `mutagen` library

### 2. DataManager
Receives metadata from FileCollector service, saves file in MongoDB by path and saves metadata in Elasticsearch. Sends uniqueID to Kafka for next service.

**Unique ID Creation**: Uses `hashlib.sha256` to create uniqueID based on some metadata.

**MongoDB**: Uses GridFS to store large files in MongoDB.

### 3. Transcription
Receives uniqueID from DataManager service, retrieves file from MongoDB, transcribes it and saves transcription in Elasticsearch.

**Operation Order**: Decided to add transcription after saving in MongoDB and indexing in Elasticsearch because transcription takes time, so it's important to first insert metadata then transcribe.

**Transcription Library**: Used `faster-whisper` because it transcribes most accurately and with high quality.

**Optimization**: After transcription, updates Elasticsearch and sends to Kafka the Elasticsearch DOC ID and transcription itself, to save unnecessary retrieval in next service.

### 4. ThreatDetectionService
Receives Elasticsearch ID and transcription from Transcription service, checks against word lists how many problematic words appear and classifies if dangerous and at what threat level.

**Word Lists**: Receives 2 lists - one more dangerous and one less. Checks how many times problematic words appear, so more dangerous words get multiplied by 2.

**Threat Calculation**: Calculation is (problematic words count / transcription word length) * 100 - this gives ratio of dangerous words by transcription length.

**Level Classification**:
- Up to 5% problematic words = not dangerous
- 5-15% = medium
- Above 15% = most dangerous

Updates results in Elasticsearch for later analysis.

## DOCKER

### Dockerfiles
Each service has dockerfile that includes relevant files in image.

### Volumes
First and second services have volume defined to computer directory to retrieve podcasts.

### Docker Compose
Compose manages everything and brings up all relevant services. Configured `depends_on` for services that depend on each other, and restart on error (`restart: unless-stopped`).

