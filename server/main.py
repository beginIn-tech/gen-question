from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.text_extraction_service import TextExtractionService
from services.gemini_ai_service import GeminiAIService
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create FastAPI instance
app = FastAPI(
    title="Raw Text Extraction API",
    description="A FastAPI server for extracting raw text from documents",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the React client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Server is running"}

# Text extraction and question generation endpoint
@app.post("/extract-text")
async def extract_text_and_generate_questions(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...),
    num_questions: int = 10
):
    """
    Extract raw text from uploaded files and generate interview questions
    Supports: .txt, .pdf, .doc, .docx files
    """
    try:
        # Validate file types
        if not TextExtractionService.is_supported_file_type(resume_file.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported resume file format. Supported formats: {', '.join(TextExtractionService.get_supported_file_types())}"
            )
        
        if not TextExtractionService.is_supported_file_type(jd_file.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported job description file format. Supported formats: {', '.join(TextExtractionService.get_supported_file_types())}"
            )
        
        # Extract raw text from files
        resume_text = await TextExtractionService.extract_text_from_file(resume_file)
        jd_text = await TextExtractionService.extract_text_from_file(jd_file)
        
        # Initialize AI service and generate questions
        try:
            ai_service = GeminiAIService()
            questions_data = await ai_service.generate_questions(resume_text, jd_text, num_questions)
            
            # Return combined response with text and questions
            return {
                "resume": resume_text,
                "job_description": jd_text,
                "generated_questions": questions_data,
                "success": True
            }
            
        except HTTPException as ai_error:
            # If AI service fails, still return the extracted text
            return {
                "resume": resume_text,
                "job_description": jd_text,
                "generated_questions": None,
                "success": False,
                "ai_error": str(ai_error.detail),
                "message": "Text extracted successfully, but question generation failed. Please check your GEMINI_API_KEY."
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
