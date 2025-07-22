def is_line_relevant(line, keywords):
    return any(kw in line.lower() for kw in keywords)

def extract_resume_data(text):
    data = {
        "skills": [],
        "education": [],
        "experience": [],
        "projects": [],
        "certifications": []
    }

    skills_keywords = ["python", "django", "react", "aws", "mongodb", "html", "css", "sql", "javascript", "node", "c++", "java", "flask"]
    education_keywords = ["b.tech", "ssc", "intermediate", "gpa", "graduation"]
    experience_keywords = ["intern", "experience", "trainee", "worked at"]
    project_keywords = ["project", "portfolio", "bot"]
    cert_keywords = ["certificate", "nptel", "coursera", "certification"]

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for line in lines:
        l = line.lower()

        if any(kw in l for kw in education_keywords):
            data["education"].append(line)
        if any(kw in l for kw in experience_keywords):
            data["experience"].append(line)
        if any(kw in l for kw in project_keywords):
            data["projects"].append(line)
        if any(kw in l for kw in cert_keywords):
            data["certifications"].append(line)

        # Smart skill matching
        found_skills = [kw for kw in skills_keywords if kw in l]
        if found_skills:
            data["skills"].extend(found_skills)

    # Remove duplicates
    for key in data:
        data[key] = list(set(data[key]))

    return data
