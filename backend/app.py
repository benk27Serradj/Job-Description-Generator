#export GOOGLE_API_KEY="AIzaSyArLN1-bvRvLyjX17kmxAWo40Gh12f0Qro"

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

api_key = os.environ.get("GOOGLE_API_KEY")
if api_key is None:
    raise ValueError("API_KEY environment variable not set.")
genai.configure(api_key=api_key)
print(f"API Key: {os.environ.get('GOOGLE_API_KEY')}")



app = Flask(__name__)
CORS(app)  
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_section(prompt):
    response = model.generate_content(
        prompt
    )
    return response.text.strip()  # Access the generated text


@app.route('/generate-description', methods=['POST'])
def generate_description():
    data = request.json
    job_title = data.get('job_title')
    industry = data.get('industry', 'general') 
    tone = data.get('tone', 'neutral') 


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

    return jsonify(job_description)

if __name__ == '__main__':
    app.run(debug=True)
