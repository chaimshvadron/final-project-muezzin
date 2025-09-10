import os
from utils.logger import Logger
logger = Logger.get_logger(service_name="FileCollector")

# reading files from a directory
class FileCollector:
    def __init__(self, path: str):
        self.path = path

    def collect_files(self):
        files_paths = []
        for root, dirs, files in os.walk(self.path):
            logger.info(f"Inspecting {root}, found {len(files)} files.")
            for file in files:
                full_path = os.path.normpath(os.path.join(root, file)).replace("\\", "/")
                files_paths.append(full_path)
        logger.info(f"Total files collected: {len(files_paths)}")
        return files_paths


