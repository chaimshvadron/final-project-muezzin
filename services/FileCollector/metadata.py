import os
import json
from mutagen import File as MutagenFile
from datetime import datetime

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
                "creation_time": datetime.fromtimestamp(state.st_birthtime),
                "audio_length": length_in_seconds,
            }
            return metadata
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            return None
        except Exception as e:
            print(f"Error accessing {self.file_path}: {e}")
            return None

    def to_json(self):
        metadata = self.collect_metadata()
        if metadata is not None:
            return json.dumps({self.file_path: metadata}, default=str)
        return None