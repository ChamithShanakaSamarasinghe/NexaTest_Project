import pytesseract
from PIL import Image
import pdf2image

class OCRFallback:
    def parse_image(self, file_path: str):
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return {"text": text}

    def parse_scanned_pdf(self, file_path: str):
        # Convert PDF to images
        images = pdf2image.convert_from_path(file_path)
        full_text = []
        for img in images:
            text = pytesseract.image_to_string(img)
            full_text.append(text)
        
        return {"text": "\n\n".join(full_text)}
