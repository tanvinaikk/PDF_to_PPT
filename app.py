import os


from flask import Flask, redirect, url_for, render_template, request, session, send_file
from flask_session import Session
from io import BytesIO

from helpers import process_pdf
from utils.generate_ppt import generate_presentation
from utils.gpt import gpt_divide


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Configure application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set the secret key to some random bytes. Keep this really secret!
_mail_enabled = os.environ.get("MAIL_ENABLED", default="true")
MAIL_ENABLED = _mail_enabled.lower() in {"1", "t", "true"}

# SECRET_KEY = os.environ.get("SECRET_KEY")

# if not SECRET_KEY:
#     raise ValueError("No SECRET_KEY set for Flask application")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Homepage"""

    return render_template("index.html")  


@app.route("/upload", methods = ['POST'])
def upload(): 
    """ Takes pdf as input """
    if request.method == 'POST':  

        if 'file' not in request.files:
            return 'No file part', 400

        f = request.files['file'] 
        # f.save(f.filename) 

        # Save the uploaded file to 'uploads' folder
        pdf_file_path = 'uploads/' + f.filename
        f.save(pdf_file_path)

        # Process the PDF
        text = process_pdf(pdf_file_path)  

        # Call the summarization function
        result = gpt_divide(text)

        # Print or log the result
        print("ChatGPT Sections Result:", result)

        # Pass the 'text' to generate_presentation function
        ppt_buffer = generate_presentation(result)

        # Save ppt_buffer to session for later use
        session['ppt_buffer'] = ppt_buffer.getvalue()
            
        return redirect(url_for('download_presentation')) 
    return render_template("index.html")  

@app.route("/download")
def download_presentation():
    """ Downloads ppt as an output """
    
    # Retrieve ppt_buffer from session
    ppt_buffer = BytesIO(session.get('ppt_buffer', b''))

    return send_file(ppt_buffer, download_name="Output.pptx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    













