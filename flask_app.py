import os
import re
import traceback
from flask import Flask, render_template, request, jsonify

# Import your custom functions
from resume_parser import extract_text_from_pdf
from langgraph_flow import (
    run_career_coach_flow,
    # run_resume_builder_flow has been removed
    run_cover_letter_builder_flow
)

# --- FLASK APP SETUP ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'nishantr486@8475'

# --- HELPER FUNCTIONS FOR FORMATTING AI OUTPUT ---

def parse_llm_output(raw_text):
    """
    Parses the raw LLM output string into a dictionary of sections.
    """
    sections = {}
    pattern = re.compile(r'(📝 Resume Feedback|🎯 Recommended Job Matches|💡 Interview Preparation)\n(.*?)(?=\n📝|\n🎯|\n💡|$)', re.DOTALL)
    
    matches = pattern.findall(raw_text)
    
    header_map = {
        '📝 Resume Feedback': 'resume_feedback',
        '🎯 Recommended Job Matches': 'job_matches',
        '💡 Interview Preparation': 'interview_prep'
    }

    for header, content in matches:
        key = header_map.get(header.strip())
        if key:
            sections[key] = content.strip()
            
    for key in header_map.values():
        if key not in sections:
            sections[key] = ""
            
    return sections

def format_feedback_html(text):
    """
    Formats the detailed resume feedback text into structured HTML with sections and lists.
    """
    html = '<div class="space-y-6 text-gray-800 text-left">'
    
    # Split the text into major sections (e.g., ATS Score, Overall Structure, etc.)
    sections = re.split(r'\n\*\*(\d\.\s.*?):\*\*', text)
    
    # The first part is usually empty or an intro, we skip it
    for i in range(1, len(sections), 2):
        title = sections[i].strip()
        content = sections[i+1].strip()
        
        html += f'<div class="feedback-section"><h3 class="text-lg font-bold text-blue-700 mb-3">{title}</h3>'
        
        # Process subsections like Strengths, Areas for Improvement
        subsections = re.split(r'\n\*\s*\*\*(.*?):\*\*', content)
        if len(subsections) > 1:
            for j in range(1, len(subsections), 2):
                sub_title = subsections[j].strip()
                sub_content = subsections[j+1].strip()
                html += f'<h4 class="font-semibold text-gray-800 mt-4 mb-2">{sub_title}</h4>'
                html += '<ul class="list-disc list-inside ml-4 space-y-1">'
                for item in sub_content.split('\n'):
                    if item.strip():
                        html += f'<li>{item.strip().lstrip("* ")}</li>'
                html += '</ul>'
        else:
            # If no subsections, just list the points
            html += '<ul class="list-disc list-inside ml-4 space-y-1">'
            for item in content.split('\n'):
                if item.strip():
                    html += f'<li>{item.strip().lstrip("* ")}</li>'
            html += '</ul>'
            
        html += '</div>'
        
    html += '</div>'
    return html

def format_jobs_html(text):
    """
    Formats the job matches text into a clean, single-column HTML layout,
    robustly separating titles from descriptions.
    """
    if not text:
        return "<p>No job matches available.</p>"

    html = '<div class="space-y-8 text-gray-800 text-left">'
    
    # MODIFIED: Corrected the regular expression to fix the "multiple repeat" error
    # This pattern now looks for a number, a period, "Role Recommendation", and a colon.
    job_blocks = re.split(r'\d\.\s*Role Recommendation:', text, flags=re.IGNORECASE)

    for block in job_blocks:
        if not block.strip():
            continue
            
        lines = block.strip().split('\n')
        title = lines[0].strip()
        description = " ".join(lines[1:]).strip()
        
        # Each job is a section with a bottom border
        html += f'<div class="pb-6 border-b border-gray-200">'
        html += f'<h3 class="text-xl font-bold text-blue-700 mb-3">{title}</h3>'
        
        # Add the description if it exists
        if description:
             # Find and format subsections like "Justification:"
            sub_sections = re.split(r'\*\*(.*?):\*\*', description)
            if len(sub_sections) > 1:
                for i in range(1, len(sub_sections), 2):
                    sub_title = sub_sections[i].strip()
                    sub_content = sub_sections[i+1].strip()
                    html += f'<h4 class="font-semibold text-gray-800 mt-4 mb-2">{sub_title}</h4><p class="text-gray-700 text-sm">{sub_content}</p>'
            else:
                 html += f'<p class="text-gray-700">{description}</p>'

        html += '</div>' # Close the section
        
    # Remove the last border for a cleaner look
    if html.endswith('</div>'):
        last_div_pos = html.rfind('<div class="pb-6 border-b border-gray-200">')
        if last_div_pos != -1:
            html = html[:last_div_pos] + '<div class="pb-6">' + html[last_div_pos + len('<div class="pb-6 border-b border-gray-200">'):]

    html += '</div>' # Close the container
    return html

def format_interview_html(text):
    """
    Formats the interview questions into a structured HTML list with subheadings.
    """
    if not text:
        return "<p>No interview prep available.</p>"

    html = '<div class="space-y-8 text-gray-800 text-left">'
    
    sections = [s.strip() for s in text.split('###') if s.strip()]

    for section_text in sections:
        match = re.search(r'\d+\.', section_text)
        
        if not match:
            continue

        title_end_index = match.start()
        title = section_text[:title_end_index].strip()
        questions_text = section_text[title_end_index:].strip()

        if not title:
            continue

        html += f'<div><h3 class="text-xl font-bold text-blue-700 mb-4">{title}</h3>'
        html += '<ol class="list-decimal pl-5 space-y-4 text-gray-700">'
        
        questions = [q.strip() for q in re.split(r'\d+\.\s*', questions_text) if q.strip()]
        
        for question in questions:
            html += f'<li class="pl-2"><p class="font-semibold text-gray-900">{question}</p></li>'
        
        html += '</ol></div>'
        
    if '<div>' not in html:
        return '<p class="text-gray-500 text-left">Could not parse interview questions from the AI response.</p>'

    return html

# --- ROUTES FOR SERVING HTML PAGES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cover_letter_builder')
def cover_letter_builder():
    return render_template('cover_letter_builder.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

# --- API ROUTES FOR AI FEATURES ---

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})
        
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    try:
        resume_text = extract_text_from_pdf(filepath)
        
        # ADDED: Get question counts from the form data, with default values
        tech_count = request.form.get('tech_count', 5)
        behavioral_count = request.form.get('behavioral_count', 5)
        design_count = request.form.get('design_count', 2)
        
        # MODIFIED: Pass the counts to the career coach flow
        raw_llm_output = run_career_coach_flow(
            resume_text, 
            tech_count=tech_count, 
            behavioral_count=behavioral_count, 
            design_count=design_count
        )

        parsed_sections = parse_llm_output(raw_llm_output)
        
        results = {
            'resume_feedback': format_feedback_html(parsed_sections.get('resume_feedback')),
            'job_matches': format_jobs_html(parsed_sections.get('job_matches')),
            'interview_prep': format_interview_html(parsed_sections.get('interview_prep'))
        }

        return jsonify({'success': True, 'message': 'Resume analyzed successfully!', 'results': results})
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'An error occurred: {str(e)}'})

@app.route('/build_cover_letter', methods=['POST'])
def build_cover_letter_route():
    try:
        if 'resume' not in request.files:
            return jsonify({'success': False, 'message': 'No resume file uploaded'})
        
        job_description = request.form.get('job_description', '')
        if not job_description:
            return jsonify({'success': False, 'message': 'Job description is empty'})
            
        resume_file = request.files['resume']
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(filepath)
        resume_text = extract_text_from_pdf(filepath)

        generated_letter_text = run_cover_letter_builder_flow(resume_text, job_description)

        return jsonify({'success': True, 'cover_letter_text': generated_letter_text})

    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'An error occurred: {str(e)}'})

# --- MAIN EXECUTION ---

if __name__ == '__main__':
    app.run(debug=True)