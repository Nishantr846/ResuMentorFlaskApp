# ResuMentor: AI-Powered Resume Co-Pilot

ResuMentor is a comprehensive, AI-driven career development platform built with Flask and powered by a local Large Language Model (LLM) using Ollama. It is designed to streamline and personalize the job preparation process by providing resume analysis and cover letter generation.

---

## 🎯 Key Features

* **AI Resume Analyzer**: Upload a resume in PDF format to receive instant, detailed feedback. The analysis covers:
    * Content, structure, and formatting improvements.
    * AI-powered job role recommendations based on your experience.
    * A custom number of technical, behavioral, and system design interview questions tailored to your profile.
* **AI Cover Letter Builder**: Paste a job description and upload your resume to generate a personalized and professional cover letter that bridges your experience with the employer's needs.

---

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **AI/ML**: Ollama (running the Mistral model), LangChain
* **Frontend**: HTML5, CSS3, JavaScript
* **Python Libraries**: `python-docx`, `pdfplumber`, `python-dotenv`

---

## 🚀 Setup and Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

* Python 3.10+
* Conda (or another virtual environment manager)
* [Ollama](https://ollama.com/) installed and running.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Nishantr846/ResuMentorFlaskApp.git](https://github.com/Nishantr846/ResuMentorFlaskApp.git)
    cd ResuMentorFlaskApp
    ```

2.  **Create and activate the Conda environment:**
    ```bash
    conda create --name rmenv python=3.10
    conda activate rmenv
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download the AI Model:**
    Make sure Ollama is running, and then pull the `mistral` model. This is a one-time download.
    ```bash
    ollama pull mistral
    ```

### Running the Application

1.  Ensure your Conda environment is activated (`conda activate rmenv`).
2.  Ensure the Ollama application is running in the background.
3.  Start the Flask server:
    ```bash
    flask run
    ```
4.  Open your web browser and navigate to `http://127.0.0.1:5000`.