


# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from fpdf import FPDF
# import google.generativeai as genai
# import configparser

# # config = configparser.ConfigParser()
# # config.read('C:/Users/SAKSHI/Desktop/1 - Copy/pokie/Backend/secret.properties')
# # API_KEY = config.get('DEFAULT', 'API_KEY')

# import os
# API_KEY = os.getenv('API_KEY')

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

#     # Replace ₹ with Rs. and handle encoding issues
#     text = text.replace("₹", "Rs.")
    
#     try:
#         # Convert unsupported characters to safe ones
#         encoded_text = text.encode("latin-1", "replace").decode("latin-1")
#     except UnicodeEncodeError:
#         encoded_text = text.encode("ascii", "ignore").decode("ascii")  # Remove problematic characters

#     pdf.multi_cell(0, 10, encoded_text)
#     pdf.output("itinerary.pdf", "F")  # Ensure explicit file mode

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
#     app.run(host='0.0.0.0', debug=True)



from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from fpdf import FPDF
import google.generativeai as genai
import os
from datetime import datetime
# import configparser

# config = configparser.ConfigParser()
# config.read('C:/Users/SAKSHI/Desktop/March_backend/secret.properties')
# API_KEY = config.get('DEFAULT', 'API_KEY')
 

API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app)


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 15)
        # Add header text
        self.cell(0, 10, "Om Tours and Travel", ln=1, align="C")
        # Add a line below the header
        self.line(10, 20, 200, 20)  
        self.ln(5)

    def add_day(self, day, content):
        self.set_font("Arial", style="B", size=12)
        self.multi_cell(0, 10, f"{day}", ln=1)
        self.set_font("Arial", size=12)
        self.multi_cell(0, 10, content)
        self.ln(5)  

    def footer(self):
        self.set_y(-15)
        # Set font for the footer
        self.set_font("Arial", 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def calculate_duration(start_date="12-12-2026", end_date="21-12-2026"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return (end - start).days + 1


def generate_itinerary(source, destination, duration, budget, preferences,trip_type):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    
    prompt = (
        f"Generate a detailed {duration}-day travel itinerary from {source} to {destination} "
        f"with a budget of Rs. {budget}. Preferences: {preferences}.  Trip type: {trip_type}. "
        f"Format the itinerary with 'Day X:' followed by activities for each day and then followed by each day budget as 'Day X Budget: Rs. Y'. "
        f"Include travel tips and local cuisine recommendations. "
        f"Use plain text and avoid Markdown or bullet points."
    )

    response = model.generate_content([prompt])
    
    
    itinerary_text = response.text.replace("*", "").replace("#", "").replace("-", "").strip()
    
    return itinerary_text


def save_to_pdf(text):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    
    text = text.replace("₹", "Rs.")
    
    
    lines = text.split("\n")
    for line in lines:
        if line.startswith("Day "):  
            pdf.set_font("Arial", style="B", size=12)  
            pdf.multi_cell(0, 10, line)
        elif "Budget:" in line:  
            pdf.set_font("Arial", style="I", size=12)  
            pdf.multi_cell(0, 10, line)
        else:
            pdf.set_font("Arial", size=12) 
            pdf.multi_cell(0, 10, line)
    pdf_path = os.path.join(app.root_path, "itinerary.pdf")
    pdf.output(pdf_path)
    pdf.output("itinerary.pdf")
    return "itinerary.pdf"

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary_api():
    data = request.json
    
    source = data.get("source", "")
    destination = data.get("destination", "")
    start_date = data.get("start_date", "") or datetime.now().strftime("%Y-%m-%d") 
    end_date = data.get("end_date", "") or datetime.now().strftime("%Y-%m-%d")
    budget = data.get("budget", "")
    preferences = data.get("preferences", "")
    trip_type = data.get("trip_type", "")

    duration = calculate_duration(start_date, end_date)

    itinerary_text = generate_itinerary(source, destination, duration, budget, preferences, trip_type)
    
    
    pdf_path = save_to_pdf(itinerary_text)
    
    return jsonify({"itinerary_text": itinerary_text, "pdf_path": pdf_path})

@app.route('/download_pdf')
def download_pdf():
    pdf_path = os.path.join(app.root_path, "itinerary.pdf")
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
