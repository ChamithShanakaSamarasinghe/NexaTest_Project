import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "pipeline_db",
    "user": "pipeline_user",
    "password": "pipeline_pass",
    "host": "postgres",
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            filename TEXT,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id SERIAL PRIMARY KEY,
            file_id INT,
            token TEXT,
            frequency INT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id SERIAL PRIMARY KEY,
            token TEXT,
            vector FLOAT[]
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS similarity (
            id SERIAL PRIMARY KEY,
            token1 TEXT,
            token2 TEXT,
            score FLOAT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rule_mappings (
            id SERIAL PRIMARY KEY,
            token TEXT,
            category TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
   
    print("Tables created successfully")

def insert_tokens(file_id, token_freq):
    conn = get_connection()
    cur = conn.cursor()

    for token, freq in token_freq.items():
        cur.execute(
            "INSERT INTO tokens (file_id, token, frequency) VALUES (%s, %s, %s);",
            (file_id, token, freq)
        )

    conn.commit()
    cur.close()
    conn.close()


def insert_embeddings(embeddings):
    conn = get_connection()
    cur = conn.cursor()

    for token, vector in embeddings.items():
        cur.execute(
            "INSERT INTO embeddings (token, vector) VALUES (%s, %s);",
            (token, vector)
        )

    conn.commit()
    cur.close()
    conn.close()


def insert_similarity(word, similarities):
    conn = get_connection()
    cur = conn.cursor()

    for other_word, score in similarities:
        cur.execute(
            "INSERT INTO similarity (token1, token2, score) VALUES (%s, %s, %s);",
            (word, other_word, float(score))
        )

    conn.commit()
    cur.close()
    conn.close()


def insert_rule_mappings(mappings):
    conn = get_connection()
    cur = conn.cursor()

    for token, category in mappings.items():
        cur.execute(
            "INSERT INTO rule_mappings (token, category) VALUES (%s, %s);",
            (token, category)
        )

    conn.commit()
    cur.close()
    conn.close()

def fetch_tokens(file_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT token, frequency FROM tokens WHERE file_id=%s;", (file_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def fetch_all_similarity():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT token1, token2, score FROM similarity ORDER BY score DESC;"
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

def fetch_rule_mappings():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT token, category FROM rule_mappings;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

if __name__ == "__main__":
        create_tables()
