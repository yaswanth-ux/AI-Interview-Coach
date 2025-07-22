import google.generativeai as genai
from resume.models import Resume
from django.conf import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

def generate_interview_questions(data, round_type="technical", job_role=""):
    skills = ', '.join(data.get("skills", []))
    projects = ', '.join(data.get("projects", []))
    experience = ', '.join(data.get("experience", []))

    if round_type == "technical":
        prompt = f"""
        You are a technical interviewer hiring for the role of **{job_role}**.
        Ask 5 technical interview questions based on the candidate’s background.
        Candidate Details:
        - Skills: {skills}
        - Projects: {projects}
        - Experience: {experience}
        
        Only output 5 numbered questions. No explanations.
        """
    
    elif round_type == "hr":
        prompt = f"""
        You are an HR interviewer evaluating a candidate for the role of **{job_role}**.
        Ask 5 behavioral or personality-based HR questions to assess soft skills, motivation, and fit.
        Base the questions loosely on the following resume:
        - Skills: {skills}
        - Projects: {projects}
        - Experience: {experience}

        Only output 5 numbered questions. No explanations.
        """
    
    elif round_type == "managerial":
        prompt = f"""
        You are a managerial round interviewer for the role of **{job_role}**.
        Ask 5 situational or decision-making questions to test leadership, communication, and ownership.
        Consider this candidate background:
        - Skills: {skills}
        - Projects: {projects}
        - Experience: {experience}

        Only output 5 numbered questions. No explanations.
        """

    else:
        prompt = f"""
        Generate 5 interview questions for the role of **{job_role}**.
        Use this resume info:
        - Skills: {skills}
        - Projects: {projects}
        - Experience: {experience}

        Only output 5 numbered questions. No intro.
        """

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            lines = response.text.split("\n")
            return [line.strip() for line in lines if line.strip() and line.strip()[0].isdigit()]
        except Exception as e:
            print("❌ Error from Gemini:", e)
            return ["Error generating questions. Please try again."]



def get_resume_data(user):
    try:
        resume = Resume.objects.filter(user=user).latest('uploaded_at')
        text = resume.extracted_text  # This is your OCR/parsed text

        # Temporary mock structure — customize this to match your resume
        return {
            "skills": ["Python", "Django", "AWS", "Lambda", "OpenAI", "Generative AI"],
            "projects": ["Email Automation Bot", "Portfolio Website", "Full Stack Web App"],
            "experience": ["Intern at Techwing (AWS + GenAI)", "Built scalable APIs with Django + MongoDB"],
            "education": ["B.Tech, GIET College"]
        }

    except Resume.DoesNotExist:
        # No resume found — fallback dummy data
        return {
            "skills": ["Python", "HTML", "CSS"],
            "projects": [],
            "experience": [],
            "education": []
        }
