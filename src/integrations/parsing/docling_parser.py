from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

class DoclingParser:
    def __init__(self):
        # Configure pipeline to generate images for pictures
        pipeline_options = PdfPipelineOptions()
        pipeline_options.generate_picture_images = True
        
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def parse(self, file_path: str, job_id: str = None):
        result = self.converter.convert(file_path)
        # Export to markdown or JSON as needed. 
        # Using simpler export for now, can refine to detailed JSON later.
        text = result.document.export_to_markdown()
        
        # Extract Tables
        tables = []
        for table in result.document.tables:
            # Table data structure varies, usually has 'data' or 'grid'
            # Exporting to markdown gives the structure in text, 
            # but here we can try to get metadata
            tables.append({
                "num_rows": table.data.num_rows,
                "num_cols": table.data.num_cols,
                # 'content': table.export_to_markdown() # Optional: duplicate info
            })

        # Extract Images (Pictures)
        images = []
        import os
        
        # Create image directory if job_id is provided
        image_save_dir = None
        if job_id:
            image_save_dir = os.path.join("uploads", "images", job_id)
            os.makedirs(image_save_dir, exist_ok=True)

        for i, picture in enumerate(result.document.pictures):
            # PictureItem structure might vary by format (PDF vs DOCX)
            # Safely get caption if it exists
            caption = getattr(picture, "caption", None)
            
            image_path = None
            if image_save_dir:
                # Try to get PIL image
                try:
                    pil_image = None
                    # Modern Docling: use get_image(doc) to resolve ImageRef
                    if hasattr(picture, "get_image"):
                        pil_image = picture.get_image(result.document)
                    
                    # Fallback for older versions or specific formats where .image might be the PIL object
                    elif hasattr(picture, "image"): 
                         img = picture.image
                         if hasattr(img, "save"):
                             pil_image = img


                    if pil_image:
                        image_filename = f"image_{i+1}.png"
                        full_image_path = os.path.join(image_save_dir, image_filename)
                        pil_image.save(full_image_path)
                        image_path = full_image_path
                except Exception as e:
                    print(f"Failed to save image {i}: {e}")

            images.append({
                "caption": caption, 
                "image_path": image_path
            })

        return {
            "text": text,
            "tables": tables,
            "images": images
        }
