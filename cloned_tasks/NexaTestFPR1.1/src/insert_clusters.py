import sqlite3
from pathlib import Path

DB_PATH = Path("db/feature_encoding.db")

# paste your real output here
KEYWORDS = {
    0: ['said', 'mr', 'government', 'people', 'labour'],
    1: ['said', 'time', 'win', 'years', 'game'],
    2: ['said', 'new', 'company', 'firm', 'bn'],
    3: ['technology', 'people', 'use', 'make', 'way'],
    4: ['economy', 'growth', 'market', 'rise', 'expected']
}

SILHOUETTE_SCORE = -0.0076

def insert_clusters():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for cluster_id, keywords in KEYWORDS.items():
        cursor.execute("""
            INSERT OR REPLACE INTO clusters
            (cluster_id, keywords, silhouette_score)
            VALUES (?, ?, ?)
        """, (cluster_id, ", ".join(keywords), SILHOUETTE_SCORE))

    conn.commit()
    conn.close()
    print("✅ Clusters inserted")

if __name__ == "__main__":
    insert_clusters()