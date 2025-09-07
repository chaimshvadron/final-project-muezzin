import os
from datetime import datetime


print("current time:", datetime.now().strftime("%Y%m%d-%H%M%S"))

# reading files from a directory
class FileCollector:
    def __init__(self, path):
        self.path = path
        
        
    def _changed_name_timestamp(self, file_path):
        try:            
            state = os.stat(file_path)
            current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
            base_name = os.path.basename(file_path)
            dir_name = os.path.dirname(file_path)
            new_name = f"{current_time}_{base_name}"
            new_path = os.path.join(dir_name, new_name)
            os.rename(file_path, new_path)
            os.utime(new_path, (state.st_atime, state.st_mtime))
            return new_path
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except Exception as e:
            print(f"Error accessing {file_path}: {e}")
            return None

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
    path_file = os.path.join(".", "data", "podcasts")
    collector = FileCollector(path_file)
    files = collector.collect_files()
    print("Collected files:", files)