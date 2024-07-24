import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
import io
from docx import Document

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from a PDF file using pdfplumber and Tesseract OCR
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            pil_image = page.to_image(resolution=300).original
            text += pytesseract.image_to_string(pil_image)
    return text

# Function to extract text from an image file using Tesseract OCR
def extract_text_from_image(image_file):
    pil_image = Image.open(image_file)
    return pytesseract.image_to_string(pil_image)

# Function to save text to a .docx file
def save_text_to_docx(text):
    doc = Document()
    doc.add_paragraph(text)
    byte_io = io.BytesIO()
    doc.save(byte_io)
    byte_io.seek(0)
    return byte_io

# Streamlit app
st.title("Document Extraction using FormNet")

# Dropdown menu to choose between PDF and Image
option = st.selectbox("Choose the file type", ["PDF", "Image"])

if option == "PDF":
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file:
        # Display the PDF file
        st.subheader("PDF Preview")
        st.write("Displaying first page of the PDF...")
        with pdfplumber.open(uploaded_file) as pdf:
            first_page = pdf.pages[0].to_image(resolution=300).original
            st.image(first_page, caption="First page of the PDF", use_column_width=True)
        
        # Extract and display text
        st.write("Extracting text from PDF...")
        extracted_text = extract_text_from_pdf(uploaded_file)
        st.subheader("Extracted Text")
        st.text_area("Text", extracted_text, height=300)

elif option == "Image":
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        # Display the image file
        st.subheader("Image Preview")
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Extract and display text
        st.write("Extracting text from image...")
        extracted_text = extract_text_from_image(uploaded_file)
        st.subheader("Extracted Text")
        st.text_area("Text", extracted_text, height=300)

# Button to save the text as a .docx file
if uploaded_file:
    if st.button("Save as DOCX"):
        docx_file = save_text_to_docx(extracted_text)
        st.download_button(
            label="Download DOCX",
            data=docx_file,
            file_name="extracted_text.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
