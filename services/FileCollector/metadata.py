import os
from mutagen import File as MutagenFile
from datetime import datetime
from utils.logger import Logger
logger = Logger.get_logger(service_name="FileCollector")

class FileMetadataCollector:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def collect_metadata(self):
        try:
            state = os.stat(self.file_path)
            audio = MutagenFile(self.file_path)
            length_in_seconds = audio.info.length
            metadata = {
                "name": os.path.basename(self.file_path),
                "size": state.st_size,
                "last_modified": datetime.fromtimestamp(state.st_mtime),
                "last_accessed": datetime.fromtimestamp(state.st_atime),
                "creation_time": datetime.fromtimestamp(state.st_ctime),
                "audio_length": length_in_seconds,
            }
            logger.info(f"Metadata collected for file {self.file_path}: {metadata}")
            return metadata
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            return None
        except Exception as e:
            logger.error(f"Error accessing {self.file_path}: {e}")
            return None

    def to_dict(self):
        metadata = self.collect_metadata()
        if metadata is not None:
            return metadata
        return None