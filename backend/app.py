from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key is None:
    raise ValueError("API_KEY environment variable not set.")
# Configure the Google Generative AI with the retrieved API key
genai.configure(api_key=api_key)
print(f"API Key: {os.environ.get('GOOGLE_API_KEY')}")

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) for the application
CORS(app)  
# Initialize the GenerativeModel with the specified model identifier
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_section(prompt):
    """
    Generate content for a given prompt using the GenerativeModel.
    """
    response = model.generate_content(prompt)
    return response.text.strip()  

@app.route('/generate-description', methods=['POST'])
def generate_description():
    """
    Endpoint to generate a job description based on the provided job title, industry, and tone.
    """
    # Extract the JSON data from the request
    data = request.json
    job_title = data.get('job_title')
    industry = data.get('industry', 'general') 
    tone = data.get('tone', 'neutral') 

    # Generate job summary, responsibilities, and requirements sections
    job_summary = generate_section(
        f"Provide a concise job summary for a {job_title} in the {industry} industry with a {tone} tone. Describe the key objectives, and unique aspects of the role without using any special formatting or markdown or."
    )   
    
    responsibilities = generate_section(
        f"List 5-7 precise responsibilities for a {job_title} in the {industry} industry. Present them in plain text without bullet points or special formatting."
    )
    
    requirements = generate_section(
        f"List 5-7 essential requirements for a {job_title} in the {industry} industry. Present them in plain text without bullet points or special formatting."
    )

    # Format the data to return as an object
    job_description = {
        "job_summary": job_summary,
        "responsibilities": responsibilities.split('\n'),
        "requirements": requirements.split('\n')
    }

    # Return the generated job description as JSON
    return jsonify(job_description)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
