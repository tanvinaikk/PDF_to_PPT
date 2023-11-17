from cs50 import SQL
from flask import redirect, render_template, session
from functools import wraps
import PyPDF2

from model import summary

db = SQL("sqlite:///tanvi.db")

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def extract_text_from_pdf(file_path):
    """ Function to extract text from a PDF file using PyPDF2 """
    
    with open(file_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        num_pages = len(pdf.pages)
        extracted_text = []

        for page_num in range(num_pages):
            page = pdf.pages[page_num]
            text = page.extract_text()
            extracted_text.append(f"Page {page_num + 1}:\n{text}\n")

        return extracted_text


def process_pdf(file_path):
    text = extract_text_from_pdf(file_path) 
    # text_summ = summary(text)

    return text

 
