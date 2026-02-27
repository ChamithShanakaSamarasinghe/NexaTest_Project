import pdfplumber

class PDFFallback:
    def parse(self, file_path: str):
        text_content = []
        tables = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Extract Text
                text = page.extract_text()
                if text:
                    text_content.append(text)
                
                # Extract Tables
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)
                    
        return {
            "text": "\n\n".join(text_content),
            "tables": tables
        }
