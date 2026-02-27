import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("db/feature_encoding.db")
CSV_PATH = Path("output/output_with_clusters.csv")

def insert_documents():
    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO documents (text, cluster_id) VALUES (?, ?)",
            (row["text"], int(row["cluster"]))
        )

    conn.commit()
    conn.close()
    print(f"Inserted {len(df)} documents")

if __name__ == "__main__":
    insert_documents()