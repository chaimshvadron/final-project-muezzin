from gridfs import GridFS
from utils.logger import Logger
Logger = Logger.get_logger(service_name="DataManager")

class MongoDAL:
    def __init__(self, connection, collection_name="files_collection"):
        self.connection = connection
        self.fs = GridFS(self.connection.db, collection=collection_name)

    def insert_file(self, file_path: str, filename: str, metadata: dict):
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
            file_id = self.fs.put(file_data, filename=filename, metadata=metadata)
            Logger.info(f"File inserted with ID: {file_id}")
            return file_id
        except Exception as e:
            Logger.error(f"Error inserting file: {e}")
            return None