# AI Interview Question Generator

A full-stack application that extracts text from resumes and job descriptions, then uses Google's Gemini AI to generate personalized interview questions.

## Features

- **File Upload Support**: Upload resume and job description files in multiple formats (.txt, .pdf, .doc, .docx)
- **Text Extraction**: Extract raw text from various document formats
- **AI Question Generation**: Generate personalized interview questions using Google Gemini AI
- **Categorized Questions**: Questions are categorized by type (technical, behavioral, experience) and difficulty
- **Clean UI**: Modern, responsive React frontend

## Setup Instructions

### Prerequisites

- Python 3.8+
- React 19.1+
- Google Gemini API Key

### Backend Setup

1. Navigate to the server directory:
   ```bash
   cd server
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

5. Start the FastAPI server:
   ```bash
   python main.py
   ```

   The server will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The React app will run on `http://localhost:5173`

### Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key to your `.env` file

## API Endpoints

- `GET /health` - Health check
- `POST /extract-text` - Upload files and generate questions (main endpoint)

## Usage

1. Open the React app in your browser
2. Upload a resume file and a job description file
3. Click "Generate Questions" 
4. The app will:
   - Extract text from both files
   - Send the extracted text to Gemini AI
   - Generate personalized interview questions
   - Display the questions with categories and difficulty levels

## File Structure

```
questions-generation/
├── server/
│   ├── services/
│   │   ├── text_extraction_service.py
│   │   └── gemini_ai_service.py
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .env
├── client/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Response Format

The main endpoint returns:

```json
{
  "resume": "extracted resume text...",
  "job_description": "extracted job description text...",
  "generated_questions": {
    "questions": [
      {
        "id": 1,
        "question": "Question text",
        "category": "technical",
        "difficulty": "medium",
        "focus_area": "Python programming"
      }
    ],
    "summary": {
      "total_questions": 10,
      "technical_questions": 4,
      "behavioral_questions": 3,
      "experience_questions": 3
    }
  },
  "success": true
}
```

## Error Handling

- If the Gemini API key is missing or invalid, the app will still extract text but won't generate questions
- Unsupported file formats will show an error message
- Network errors and parsing errors are handled gracefully

## Technologies Used

- **Backend**: FastAPI, Python, Google Generative AI
- **Frontend**: React, Vite
- **File Processing**: PyPDF2, python-docx
- **AI**: Google Gemini 1.5 Flash

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
