import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Gemini
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize the generative model
model = genai.GenerativeModel("gemini-pro")

def modelFeedback(ats_score, resume_data, job_description):
    # Create the input prompt template
    input_prompt_template = """
    You are an HR assistant reviewing resumes. The ATS score for the resume is {ats_score}.
    For each resume, provide a summary(100 words), include the strengths of the resume and if the resume is fit for the job based on the {job_description}.
    Resume Content: {resume_data}
    """
    # Format the prompt with ATS score, missing skills, and resume data
    input_prompt = input_prompt_template.format(ats_score=ats_score, resume_data=resume_data, job_description=job_description)
    
    # Generate response
    response = model.generate_content(input_prompt)
    return response.text
