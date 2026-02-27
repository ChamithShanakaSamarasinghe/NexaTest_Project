import os
import chardet
from src.pipeline.database import get_connection


class DataIngestor:


    def __init__(self):
        pass

    def detect_encoding(self, file_path):
        
        with open(file_path, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result["encoding"]

    def read_file(self, file_path):
        
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found")

        encoding = self.detect_encoding(file_path)

        with open(file_path, "r", encoding=encoding, errors="ignore") as f:
            return f.read()

    def save_file_record(self, filename):
        
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO files (filename) VALUES (%s) RETURNING id;",
            (filename,)
        )

        file_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return file_id

    def ingest(self, file_path):
        """
        Main ingestion function.
        """
        filename = os.path.basename(file_path)

        text = self.read_file(file_path)
        file_id = self.save_file_record(filename)

        return file_id, text


# Test block
if __name__ == "__main__":
    ingestor = DataIngestor()
    fid, content = ingestor.ingest("data/raw/sample.txt")

    print("File ID:", fid)
    print("Content preview:", content[:200])
