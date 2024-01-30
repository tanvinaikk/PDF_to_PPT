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
            extracted_text.append(text)

        return extracted_text


def process_pdf(file_path):
    text = extract_text_from_pdf(file_path) 
    text_sum = summary(text)

    text_summ = """
Topic: Introduction, Points:
1. The increasing importance of managing different generations in the workplace
2. Focus on the role of knowledge-sharing
3. The impact of generational differences on cooperation and teamwork
4. The need for HR to adapt to the requirements of the new generations

Topic: Literature Review, Points:
1. Research on the characteristics of Generation Y and Generation Z
2. Differences between the two generations despite similarities
3. Emphasized differences in the corporate environment
4. Importance of knowledge-sharing and knowledge transfer in the context of generational characteristics

Topic: Methodology, Points:
1. Quantitative research conducted through questionnaires
2. Main question: how to approach new generations from an HR perspective
3. Survey results provide insights into managing the two generations
4. Research not considered representative, but offers an overview of the issues examined

Topic: Results, Points:
1. HR activities need to adapt to the requirements of new generations
2. The increase in the value of human resources and utilization of mental activities
3. Challenges in managing cooperation and conflicts between different age groups
4. The need for corporate solutions to meet the requirements of the youngest age-groups

Topic: Discussion, Points:
1. Corporate solutions influenced by the youngest age-groups in management
2. Examples of specific solutions, such as atypical employment and workplace organizational solutions
3. The role of culture, trust, and cooperation in knowledge management
4. Challenges in translating theoretical knowledge into practical implementation

Topic: Conclusion, Points:
1. Importance of recognizing and handling problems arising from intergenerational cooperation
2. Focus on the role of knowledge-sharing in managing different generations
3. Significance of intergenerational management in corporate practice
4. A call to further address the challenging problems and enhance knowledge-sharing practices in organizations.
"""

    return text_sum

 
