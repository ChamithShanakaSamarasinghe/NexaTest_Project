import sqlite3

DB_PATH = "data/srs.db"

FEATURE_KEYWORDS = {
    "Authentication": ["authenticate", "login", "password"],
    "Authorization": ["role", "rbac", "access control"],
    "Security": ["encrypt", "secure", "security"],
    "User Management": ["user", "register", "profile", "student"],
    "Course Management": ["course", "enrol", "lecturer"],
    "Grading": ["grade", "gpa"],
    "Reporting": ["report", "pdf"],
    "Notification": ["email", "notify"],
    "Audit & Logging": ["log", "audit"]
}


def detect_features(requirement_text):
    detected = set()
    text = requirement_text.lower()

    for feature, keywords in FEATURE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                detected.add(feature)

    return detected


def insert_features():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT requirement_id, requirement_text FROM requirements"
    )
    requirements = cursor.fetchall()

    total = 0

    for req_id, req_text in requirements:
        features = detect_features(req_text)

        for feature in features:
            cursor.execute(
                """
                INSERT INTO features (requirement_id, feature_name)
                VALUES (?, ?)
                """,
                (req_id, feature)
            )
            total += 1

    conn.commit()
    conn.close()

    print(f"[DONE] Inserted {total} feature mappings")


if __name__ == "__main__":
    insert_features()
