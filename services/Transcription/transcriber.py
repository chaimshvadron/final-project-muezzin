from faster_whisper import WhisperModel
from utils.logger import Logger
logger = Logger.get_logger(service_name ="Transcription")

class Transcriber:
    def __init__(self, model_size: str, device: str, compute_type: str):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)


    def transcribe(self, file_path: str):
        try:
            segments, info = self.model.transcribe(file_path)
            transcript = " ".join([segment.text for segment in segments])
            logger.info(f"Transcription successful for {file_path}, transcript {transcript[:30]}...")
            return transcript
        except Exception as e:
            logger.error(f"Error during transcription of {file_path}: {e}")
            raise