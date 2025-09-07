import os

class FileMetadata:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_metadata(self):
        try:
            state = os.stat(self.file_path)
            return {
                "name": os.path.basename(self.file_path),
                "size": state.st_size,
                "last_modified": state.st_mtime,
                "last_accessed": state.st_atime,
                "creation_time": state.st_birthtime,
            }
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            return None
        except Exception as e:
            print(f"Error accessing {self.file_path}: {e}")
            return None