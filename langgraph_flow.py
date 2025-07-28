import json
import os
from dotenv import load_dotenv
from llm import call_llm

# Load environment variables
load_dotenv()

def run_career_coach_flow(resume_text):
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

    feedback_prompt = feedback_template.replace("{{resume}}", resume_text)
    job_matching_prompt = job_match_template.replace("{{resume}}", resume_text)
    interview_prompt = interview_template.replace("{{resume}}", resume_text)

    # Get responses from LLM
    resume_feedback = call_llm(feedback_prompt)
    job_recommendations = call_llm(job_matching_prompt)
    interview_questions = call_llm(interview_prompt)

    # Combine into a single string for parsing
    formatted_output = f"""
📝 Resume Feedback
{resume_feedback}

🎯 Recommended Job Matches
{job_recommendations}

💡 Interview Preparation
{interview_questions}
"""
    return formatted_output

# --- NEW FUNCTION FOR RESUME BUILDER ---
def run_resume_builder_flow(form_data):
    """
    Processes resume form data, enhances experience descriptions using an LLM,
    and assembles the final resume text.
    """
    try:
        # MODIFIED: Path updated to look inside prompt_templates
        with open('prompt_templates/resume_builder_prompt.txt', 'r') as f:
            builder_prompt_template = f.read()
    except Exception as e:
        return f"Error: Could not load resume_builder_prompt.txt: {str(e)}"

    # Basic resume structure
    resume_parts = []
    resume_parts.append(f"# {form_data.get('full_name', '')}")
    resume_parts.append(f"{form_data.get('email', '')} | {form_data.get('phone', '')} | {form_data.get('linkedin', '')}\n")
    resume_parts.append("## Work Experience")

    # Loop through all experience entries from the form
    i = 1
    while True:
        title = form_data.get(f'experience_title_{i}')
        if not title: # Stop when we run out of experience entries
            break

        company = form_data.get(f'experience_company_{i}')
        dates = form_data.get(f'experience_dates_{i}')
        description = form_data.get(f'experience_desc_{i}')

        if company and description:
            prompt = builder_prompt_template.replace("{{job_title}}", title)
            prompt = prompt.replace("{{company}}", company)
            prompt = prompt.replace("{{description}}", description)

            enhanced_description = call_llm(prompt)

            resume_parts.append(f"\n**{title}** | {company} | {dates}")
            resume_parts.append(enhanced_description)
        i += 1
        
    # Add other sections from form data
    resume_parts.append("\n## Education")
    resume_parts.append(f"{form_data.get('education_degree_1', '')}\n{form_data.get('education_school_1', '')} | {form_data.get('education_dates_1', '')}")
    resume_parts.append("\n## Skills")
    resume_parts.append(f"{form_data.get('skills', '')}")

    return "\n\n".join(resume_parts)

# --- NEW FUNCTION FOR COVER LETTER BUILDER ---
def run_cover_letter_builder_flow(resume_text, job_description_text):
    """
    Generates a tailored cover letter using a resume and job description.
    """
    try:
        # MODIFIED: Path updated to look inside prompt_templates
        with open('prompt_templates/cover_letter_prompt.txt', 'r') as f:
            cover_letter_template = f.read()
    except Exception as e:
        return f"Error: Could not load cover_letter_prompt.txt: {str(e)}"

    prompt = cover_letter_template.replace("{{resume}}", resume_text)
    prompt = prompt.replace("{{job_description}}", job_description_text)
    
    generated_letter = call_llm(prompt)
    return generated_letter