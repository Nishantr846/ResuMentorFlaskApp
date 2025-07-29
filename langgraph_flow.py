import json
import os
from dotenv import load_dotenv
from llm import call_llm

# Load environment variables
load_dotenv()

def run_career_coach_flow(resume_text, tech_count=5, behavioral_count=5, design_count=2):
    """
    Analyzes a resume and generates feedback, job matches, and a custom number of interview questions.
    """
    # Load sample job data
    try:
        with open('sample_jobs.json', 'r') as f:
            sample_jobs = json.load(f)
    except Exception as e:
        return f"Error: Could not load job data: {str(e)}"

    # Prepare prompts using templates from the correct folder
    try:
        with open('prompt_templates/feedback_prompt.txt', 'r') as f:
            feedback_template = f.read()
        with open('prompt_templates/job_match_prompt.txt', 'r') as f:
            job_match_template = f.read()
        with open('prompt_templates/interview_prompt.txt', 'r') as f:
            interview_template = f.read()
    except FileNotFoundError as e:
        return f"Error loading prompt file: {e}. Make sure all prompt files are inside the 'prompt_templates' folder."

    # Populate prompts with data
    feedback_prompt = feedback_template.replace("{{resume}}", resume_text)
    job_matching_prompt = job_match_template.replace("{{resume}}", resume_text)
    
    # MODIFIED: Insert the custom question counts into the interview prompt
    interview_prompt = interview_template.replace("{{resume}}", resume_text)
    interview_prompt = interview_prompt.replace("{{tech_count}}", str(tech_count))
    interview_prompt = interview_prompt.replace("{{behavioral_count}}", str(behavioral_count))
    interview_prompt = interview_prompt.replace("{{design_count}}", str(design_count))


    # Get responses from LLM
    resume_feedback = call_llm(feedback_prompt)
    job_recommendations = call_llm(job_matching_prompt)
    interview_questions = call_llm(interview_prompt)

    # Combine into a single string for the frontend to parse
    formatted_output = f"""
📝 Resume Feedback
{resume_feedback}

🎯 Recommended Job Matches
{job_recommendations}

💡 Interview Preparation
{interview_questions}
"""
    return formatted_output

# --- The run_resume_builder_flow function has been removed ---

# --- Cover Letter Builder Function ---
def run_cover_letter_builder_flow(resume_text, job_description_text):
    """
    Generates a tailored cover letter using a resume and job description.
    """
    try:
        with open('prompt_templates/cover_letter_prompt.txt', 'r') as f:
            cover_letter_template = f.read()
    except Exception as e:
        return f"Error: Could not load cover_letter_prompt.txt: {str(e)}"

    prompt = cover_letter_template.replace("{{resume}}", resume_text)
    prompt = prompt.replace("{{job_description}}", job_description_text)
    
    generated_letter = call_llm(prompt)
    return generated_letter