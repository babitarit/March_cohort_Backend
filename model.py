# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from fpdf import FPDF
# import google.generativeai as genai
# import configparser


# config = configparser.ConfigParser()
# config.read('C:/Users/SAKSHI/Desktop/1 - Copy/pokie/Backend/secret.properties')
# API_KEY = config.get('DEFAULT', 'API_KEY')


# genai.configure(api_key=API_KEY)


# app = Flask(__name__)
# CORS(app)

# # PDF Generation Class
# class PDF(FPDF):
#     def header(self):
#         self.set_font("Arial", size=12)
#         self.cell(0, 10, "Travel Itinerary", align="C", ln=1)

#     def add_day(self, day, content):
#         self.set_font("Arial", style="B", size=12)
#         self.cell(0, 10, f"Day {day}", ln=1)
#         self.set_font("Arial", size=12)
#         self.multi_cell(0, 10, content)


# def generate_itinerary(source, destination, duration, budget, preferences):
#     model = genai.GenerativeModel("gemini-2.0-flash")
    
#     # Replace ₹ with Rs. in the prompt
#     prompt = f"Generate a {duration}-day itinerary from {source} to {destination} with Rs. {budget}. Preferences: {preferences}."
#     response = model.generate_content([prompt])
#     return response.text

# # Function to save itinerary to a PDF file
# def save_to_pdf(text):
#     pdf = PDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     # Replace ₹ with Rs. in the generated text before saving to PDF
#     text = text.replace("₹", "Rs.")
    
#     pdf.multi_cell(0, 10, text)
#     pdf.output("itinerary.pdf")
#     return "itinerary.pdf"


# @app.route('/generate_itinerary', methods=['POST'])
# def generate_itinerary_api():
#     data = request.json
    
    
#     source = data.get("source", "")
#     destination = data.get("destination", "")
#     duration = data.get("duration", "")
#     budget = data.get("budget", "")
#     preferences = data.get("preferences", "")

   
#     itinerary_text = generate_itinerary(source, destination, duration, budget, preferences)
    
#     # Save to PDF
#     pdf_path = save_to_pdf(itinerary_text)
    
#     return jsonify({"itinerary_text": itinerary_text, "pdf_path": pdf_path})


# @app.route('/download_pdf')
# def download_pdf():
#     return send_file("itinerary.pdf", as_attachment=True)


# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from fpdf import FPDF
import google.generativeai as genai
import configparser

# config = configparser.ConfigParser()
# config.read('C:/Users/SAKSHI/Desktop/1 - Copy/pokie/Backend/secret.properties')
# API_KEY = config.get('DEFAULT', 'API_KEY')

import os
API_KEY = os.getenv('API_KEY')

genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app)

# PDF Generation Class
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", size=12)
        self.cell(0, 10, "Travel Itinerary", align="C", ln=1)

    def add_day(self, day, content):
        self.set_font("Arial", style="B", size=12)
        self.cell(0, 10, f"Day {day}", ln=1)
        self.set_font("Arial", size=12)
        self.multi_cell(0, 10, content)

def generate_itinerary(source, destination, duration, budget, preferences):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # Replace ₹ with Rs. in the prompt
    prompt = f"Generate a {duration}-day itinerary from {source} to {destination} with Rs. {budget}. Preferences: {preferences}."
    response = model.generate_content([prompt])
    return response.text

# Function to save itinerary to a PDF file
def save_to_pdf(text):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Replace ₹ with Rs. and handle encoding issues
    text = text.replace("₹", "Rs.")
    
    try:
        # Convert unsupported characters to safe ones
        encoded_text = text.encode("latin-1", "replace").decode("latin-1")
    except UnicodeEncodeError:
        encoded_text = text.encode("ascii", "ignore").decode("ascii")  # Remove problematic characters

    pdf.multi_cell(0, 10, encoded_text)
    pdf.output("itinerary.pdf", "F")  # Ensure explicit file mode

    return "itinerary.pdf"

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary_api():
    data = request.json
    
    source = data.get("source", "")
    destination = data.get("destination", "")
    duration = data.get("duration", "")
    budget = data.get("budget", "")
    preferences = data.get("preferences", "")

    itinerary_text = generate_itinerary(source, destination, duration, budget, preferences)
    
    # Save to PDF
    pdf_path = save_to_pdf(itinerary_text)
    
    return jsonify({"itinerary_text": itinerary_text, "pdf_path": pdf_path})

@app.route('/download_pdf')
def download_pdf():
    return send_file("itinerary.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
