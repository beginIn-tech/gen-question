"""
Gemini AI service for generating questions based on resume and job description
"""

import os
import json
from typing import Dict, Any
from fastapi import HTTPException
from google import genai
from prompt.interview_questions_prompt import get_interview_prompt


class GeminiAIService:
    """Service for generating questions using Google's Gemini AI"""
    
    def __init__(self):
        """Initialize the Gemini AI service"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise HTTPException(
                status_code=500, 
                detail="GEMINI_API_KEY environment variable is required"
            )
        
        # Create client with API key
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash-exp"
    
    def _clean_json_response(self, text: str) -> str:
        """Clean the AI response by extracting JSON from markdown code blocks"""
        # Remove markdown code block markers
        if "```json" in text:
            # Extract content between ```json and ```
            start = text.find("```json") + 7
            end = text.find("```", start)
            if end != -1:
                return text[start:end].strip()
        
        # If no code blocks found, return the text as is
        return text.strip()
    
    async def generate_questions(self, resume_text: str, jd_text: str, num_questions: int = 10) -> Dict[str, Any]:
        """Generate interview questions based on resume and job description"""
        try:
            # Calculate question distribution
            technical_questions = max(1, num_questions // 2)
            behavioral_questions = max(1, num_questions // 3)
            experience_questions = max(1, num_questions - technical_questions - behavioral_questions)
            
            # Create the prompt using the imported function
            prompt = get_interview_prompt(
                num_questions=num_questions,
                resume_text=resume_text[:2000],
                jd_text=jd_text[:2000],
                technical_questions=technical_questions,
                behavioral_questions=behavioral_questions,
                experience_questions=experience_questions
            )

            # Generate content using the client
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                
                generated_text = response.text.strip()
                
                # Clean the response to extract JSON from markdown code blocks
                cleaned_text = self._clean_json_response(generated_text)
                questions_data = json.loads(cleaned_text)
                return questions_data
                
            except (AttributeError, json.JSONDecodeError, TypeError) as e:
                print('Error:', e)
                # Error in generating/parsing the AI response
                raise HTTPException(
                    status_code=500, 
                    detail="Error in generating or parsing AI response"
                )
            
        except Exception as e:
            print('Error:', e)  
            # Global error handling
            raise HTTPException(
                status_code=500, 
                detail="Error generating questions"
            )