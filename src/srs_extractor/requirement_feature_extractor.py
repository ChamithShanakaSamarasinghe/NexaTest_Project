import re
import json
import sqlite3
from datetime import datetime

from src.extract_text import extract_text_from_pdf
from src.segment_requirements import extract_requirements
from src.enhancer import PipelineEnhancer

DB_PATH = r"C:\Users\raven\OneDrive\Desktop\SRS - NexaTest\db.sqlite3"

class SRSExtractor:

    def __init__(self):
        self.enhancer = PipelineEnhancer()

        self.nfr_keywords = [
            "performance", "security", "availability", "usability",
            "reliability", "scalability", "latency", "throughput",
            "maintainability", "portability", "response time",
            "uptime", "concurrent", "encryption"
        ]

    def normalize_list(self, items):
        cleaned = []
        for item in items:
            parts = re.split(r'•', item)
            for part in parts:
                part = part.strip()
                if len(part) > 5 and part not in cleaned:
                    cleaned.append(part)
        return cleaned

    def extract(self, file_path):

        print(f"Using SRS file: {file_path}\n")

        raw_text = extract_text_from_pdf(file_path)

        enhanced = self.enhancer.enhance(raw_text)
        clean_text = enhanced["clean_text"]

        requirements = extract_requirements(clean_text)

        functional = []
        non_functional = []
        features = []

        # Classify requirements
        for req in requirements:
            req = req.strip()
            if len(req) < 10:
                continue
            lower = req.lower()
            if any(keyword in lower for keyword in self.nfr_keywords):
                non_functional.append(req)
            elif re.search(r"(system shall|system must|system should|user can)", lower):
                functional.append(req)

        # Extract features
        for line in clean_text.split("\n"):
            line = line.strip()
            if len(line) < 5:
                continue
            if re.search(r"(feature|module|component|service|allow .* to|enable .* to)", line.lower()):
                features.append(line)

        functional = self.normalize_list(functional)
        non_functional = self.normalize_list(non_functional)
        features = self.normalize_list(features)

        output = {
            "functional_requirements": functional,
            "non_functional_requirements": non_functional,
            "features": features
        }

        # Save output file
        filename = f"srs_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)
        print(f"Output saved to {filename}")

        # Update database
        self.update_database(output)

        return output

    def update_database(self, results):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Helper to get existing columns for a table
            def existing_columns(table_name):
                cursor.execute(f"PRAGMA table_info({table_name})")
                return {row[1] for row in cursor.fetchall()}

            # Ensure required columns exist in fpr_results
            fr_cols = existing_columns("fpr_results")
            fr_needed = {
                "metrics": "TEXT",
                "created_at": "TEXT"
            }
            for col, col_type in fr_needed.items():
                if col not in fr_cols:
                    cursor.execute(f"ALTER TABLE fpr_results ADD COLUMN {col} {col_type}")
                    print(f"Added column `{col}` to fpr_results")

            # Ensure required columns exist in requirements
            rq_cols = existing_columns("requirements")
            rq_needed = {
                "fpr_id": "INTEGER",
                "requirement_text": "TEXT",
                "type": "TEXT"
            }
            for col, col_type in rq_needed.items():
                if col not in rq_cols:
                    cursor.execute(f"ALTER TABLE requirements ADD COLUMN {col} {col_type}")
                    print(f"Added column `{col}` to requirements")

            # Ensure required columns exist in features
            ft_cols = existing_columns("features")
            ft_needed = {
                "fpr_id": "INTEGER",
                "feature_text": "TEXT"
            }
            for col, col_type in ft_needed.items():
                if col not in ft_cols:
                    cursor.execute(f"ALTER TABLE features ADD COLUMN {col} {col_type}")
                    print(f"Added column `{col}` to features")

            conn.commit()

            # Insert new run row into fpr_results
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            metrics_json = json.dumps(results)
            cursor.execute("""
                INSERT INTO fpr_results (metrics, created_at)
                VALUES (?, ?)
            """, (metrics_json, now))
            fpr_id = cursor.lastrowid
            print(f"Inserted new fpr_results row with id = {fpr_id}")

            # Insert functional requirements
            inserted_req = 0
            for req in results.get("functional_requirements", []):
                cursor.execute("""
                    INSERT INTO requirements (fpr_id, requirement_text, type)
                    VALUES (?, ?, ?)
                """, (fpr_id, req, "functional"))
                inserted_req += 1

            # Insert non-functional requirements
            for req in results.get("non_functional_requirements", []):
                cursor.execute("""
                    INSERT INTO requirements (fpr_id, requirement_text, type)
                    VALUES (?, ?, ?)
                """, (fpr_id, req, "non-functional"))
                inserted_req += 1

            # Insert features
            inserted_feat = 0
            for feat in results.get("features", []):
                cursor.execute("""
                    INSERT INTO features (fpr_id, feature_text)
                    VALUES (?, ?)
                """, (fpr_id, feat))
                inserted_feat += 1

            conn.commit()
            conn.close()

            print(f"Database updated successfully ✅ (requirements inserted: {inserted_req}, features inserted: {inserted_feat})")

        except Exception as e:
            print("Database update failed ❌:", e)