from flask import redirect, render_template, session
from functools import wraps
import PyPDF2

from model import summary

def extract_text_from_pdf(file_path):
    """ Function to extract text from a PDF file using PyPDF2 """
    
    with open(file_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        num_pages = len(pdf.pages)
        extracted_text = []

        for page_num in range(num_pages):
            page = pdf.pages[page_num]
            text = page.extract_text()
            extracted_text.append(text)

        return extracted_text


def process_pdf(file_path):
    text = extract_text_from_pdf(file_path) 
    text_sum = summary(text)
    return text_sum

 
