FROM python:3.11-slim

WORKDIR /app

COPY ../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir faster-whisper

COPY ../../utils ./utils
COPY ../../services/Transcription ./services/Transcription

CMD ["python", "-m", "services.Transcription.main"]
