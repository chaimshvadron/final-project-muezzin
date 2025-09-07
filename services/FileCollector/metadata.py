import os
import json
from pydub import AudioSegment

class FileMetadataCollector:
    def __init__(self, file_path):
        self.file_path = file_path

    def collect_metadata(self):
        try:
            state = os.stat(self.file_path)
            audio = AudioSegment.from_file(self.file_path)
            metadata = {
                "name": os.path.basename(self.file_path),
                "size": state.st_size,
                "last_modified": state.st_mtime,
                "last_accessed": state.st_atime,
                "creation_time": state.st_birthtime,
                "audio_length": len(audio) / 1000.0,
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
            return json.dumps(metadata)
        return None