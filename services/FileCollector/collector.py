import os
from datetime import datetime


print("current time:", datetime.now().strftime("%Y%m%d-%H%M%S"))

# reading files from a directory
class FileCollector:
    def __init__(self, path):
        self.path = path
        
    def collect_files(self):
        files_paths = []
        for root, dirs, files in os.walk(self.path):
            print(f"Inspecting {root}, found {len(files)} files.")
            for file in files:
                full_path = os.path.join(root, file)
                changed_path = self._changed_name_timestamp(full_path)
                if changed_path:
                    files_paths.append(changed_path)
        return files_paths


if __name__ == "__main__":
    collector = FileCollector("./data/podcasts")
    files = collector.collect_files()
    print("Collected files:", files)