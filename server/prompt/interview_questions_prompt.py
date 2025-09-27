# prompt/interview_questions_prompt.py

def get_interview_prompt(num_questions, resume_text, jd_text, technical_questions, behavioral_questions, experience_questions):
    """Generate the interview prompt with the provided parameters"""
    return f"""You are an expert interviewer. Generate exactly {num_questions} relevant interview questions based on the provided resume and job description.

RESUME:
{resume_text}

JOB DESCRIPTION:  
{jd_text}

INSTRUCTIONS:
- Analyze the candidate's skills, experience, and background from the resume
- Match them against the job requirements and responsibilities
- Generate questions that test technical skills, experience, and cultural fit
- Categories: "technical", "behavioral", "experience"
- Difficulty levels: "easy", "medium", "hard"

IMPORTANT: Respond with ONLY valid JSON, no markdown, no explanation, no extra text. Start directly with {{ and end with }}.

{{
    "questions": [
        {{
            "id": 1,
            "question": "Based on your experience with ReactJS and NodeJS mentioned in your resume, how would you architect a full-stack application for this role?",
            "category": "technical",
            "difficulty": "medium",
            "focus_area": "full-stack development"
        }}
    ],
    "summary": {{
        "total_questions": {num_questions},
        "technical_questions": {technical_questions},
        "behavioral_questions": {behavioral_questions},
        "experience_questions": {experience_questions}
    }}
}}"""
