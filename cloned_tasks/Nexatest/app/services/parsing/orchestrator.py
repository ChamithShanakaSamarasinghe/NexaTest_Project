from app.services.parsing.docling_parser import DoclingParser
from app.services.parsing.pdf_fallback import PDFFallback
from app.services.enrichment.keywords import KeywordExtractor
from app.services.enrichment.entities import EntityExtractor
from app.services.enrichment.summarizer import Summarizer

import os


class Orchestrator:
    def __init__(self):
        self.docling = DoclingParser()  
        self.pdf_fallback = PDFFallback()
        self.keywords = KeywordExtractor()
        self.entities = EntityExtractor()
        self.summarizer = Summarizer()

    def process(self, job_id: str, file_path: str):
        # Normalize extension
        file_ext = os.path.splitext(file_path)[1].upper()

        content = {}
        method = "unknown"

        try:
            # PARSING STRATEGY (NO OCR)
            if file_ext == ".PDF":
                try:
                    # Try Docling first
                    content = self.docling.parse(file_path, job_id)
                    method = "docling_pdf"

                    text_len = len(content.get("text", "").strip())

                    # If text is too short → fallback parser
                    if text_len < 50:
                        print("⚠️ Low text detected — trying PDF fallback parser")
                        content = self.pdf_fallback.parse(file_path)
                        method = "pdf_fallback"

                except Exception as e:
                    print(f"Docling failed: {e}")
                    content = {"text": ""}
                    method = "failed"

            else:
                # Try Docling for other formats (docx etc.)
                try:
                    content = self.docling.parse(file_path, job_id)
                    method = "docling_generic"
                except Exception as e:
                    print(f"Parsing failed: {e}")
                    content = {"text": ""}
                    method = "failed"

        except Exception as e:
            print(f"❌ Parsing completely failed: {e}")
            content = {"text": ""}
            method = "failed"

        extracted_text = content.get("text", "").strip()


        # ENRICHMENT PIPELINE
        features = {}
        summary = ""

        if len(extracted_text) > 20:

            # -------- Chunking --------
            chunks = []
            paragraphs = extracted_text.split("\n\n")

            for i, para in enumerate(paragraphs):
                clean = para.strip()
                if len(clean) > 10:
                    chunks.append({
                        "text": clean,
                        "chunk_index": i,
                        "section_title": None,
                        "page_start": None,
                        "page_end": None
                    })

            features["chunks"] = chunks

            # -------- NLP Enrichment --------
            try:
                features["keywords"] = self.keywords.extract(extracted_text)
            except Exception as e:
                print("Keyword extraction failed:", e)
                features["keywords"] = []

            try:
                features["entities"] = self.entities.extract(extracted_text)
            except Exception as e:
                print("Entity extraction failed:", e)
                features["entities"] = []

            try:
                summary = self.summarizer.summarize(extracted_text)
            except Exception as e:
                print("Summarization failed:", e)
                summary = ""


        # FINAL OUTPUT
        return {
            "job_id": job_id,
            "file_path": file_path,
            "file_type": file_ext,
            "parsing_method": method,
            "content": content,
            "enrichment": {
                "summary": summary,
                "features": features
            }
        }
