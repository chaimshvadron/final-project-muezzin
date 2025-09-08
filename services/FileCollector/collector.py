import os
from datetime import datetime


# reading files from a directory
class FileCollector:
    def __init__(self, path: str):
        self.path = path

    def collect_files(self):
        files_paths = []
        for root, dirs, files in os.walk(self.path):
            print(f"Inspecting {root}, found {len(files)} files.")
            for file in files:
                full_path = os.path.join(root, file)
                files_paths.append(full_path)
        return files_paths


if __name__ == "__main__":
    path_file = os.path.join(".", "data", "podcasts")
    collector = FileCollector(path_file)
    files = collector.collect_files()
    print("Collected files:", files)