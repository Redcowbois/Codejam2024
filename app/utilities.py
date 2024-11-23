import fitz
import io
import os
from PIL import Image

def extract_images_from_pdf(pdf_path, output_folder):
    # Create the output directory if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Iterate through each page
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)
        
        # Iterate through each image
        for image_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))
            
            # Save the image
            image_filename = f"{output_folder}/image_page{page_number+1}_{image_index+1}.{image_ext}"
            image.save(image_filename)
            print(f"Saved image: {image_filename}")

def extract_text_from_pdf(pdf_path, output_text_file):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Open the output text file
    with open(output_text_file, 'w', encoding='utf-8') as text_file:
        # Iterate through each page
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            text = page.get_text()
            
            # Write the text to the file
            text_file.write(f"Page {page_number + 1}\n")
            text_file.write(text)
            text_file.write("\n\n")
            print(f"Extracted text from page {page_number + 1}")