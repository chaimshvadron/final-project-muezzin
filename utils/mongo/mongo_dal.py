from gridfs import GridFS


class MongoDAL:
    def __init__(self, connection, collection_name, logger):
        self.connection = connection
        self.logger = logger
        self.fs = GridFS(self.connection.db, collection=collection_name)

    def insert_file(self, data_file: bytes, unique_id: str):
        try:
            file_id = self.fs.put(data_file, unique_id=unique_id)
            self.logger.info(f"File inserted with ID: {file_id}")
            return file_id
        except Exception as e:
            self.logger.error(f"Error inserting file: {e}")
            return None
        
    def get_file_by_unique_id(self, unique_id: str):
        try:
            file_doc = self.fs.find_one({"unique_id": unique_id})
            if file_doc:
                self.logger.info(f"File retrieved with unique ID: {unique_id}")
                return file_doc
            else:
                self.logger.info(f"No file found with unique ID: {unique_id}")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving file by unique ID: {unique_id}: {e}")
            return None