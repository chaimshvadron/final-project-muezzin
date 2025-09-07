from gridfs import GridFS

class MongoDAL:
    def __init__(self, connection, collection_name="files_collection"):
        self.connection = connection
        self.fs = GridFS(self.connection.db, collection=collection_name)

    def insert_file(self, file_data, filename, metadata):
        try:
            file_id = self.fs.put(file_data, filename=filename, metadata=metadata)
            return file_id
        except Exception as e:
            print(f"Error inserting file: {e}")
            return None