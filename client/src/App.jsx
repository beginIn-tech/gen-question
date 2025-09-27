import React, { useState } from 'react'
import './App.css'

function App() {
  const [resumeFile, setResumeFile] = useState(null)
  const [jdFile, setJdFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState(null)
  const [error, setError] = useState(null)

  // Function to check if file type is supported
  const isSupportedFileType = (file) => {
    const supportedTypes = ['.txt', '.pdf', '.doc', '.docx']
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
    return supportedTypes.includes(fileExtension)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setResponse(null)

    if (!resumeFile || !jdFile) {
      setError('Please select both resume and job description files.')
      return
    }

    if (!isSupportedFileType(resumeFile) || !isSupportedFileType(jdFile)) {
      setError('Please upload supported file types (.txt, .pdf, .doc, .docx)')
      return
    }

    setLoading(true)
    try {
      // Create FormData for file upload
      const formData = new FormData()
      formData.append('resume_file', resumeFile)
      formData.append('jd_file', jdFile)

      const res = await fetch('http://localhost:8000/extract-text', {
        method: 'POST',
        body: formData
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.detail || 'Failed to extract text from documents')
      }

      const data = await res.json()
      setResponse(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleFileChange = (type, file) => {
    if (type === 'resume') {
      setResumeFile(file)
    } else {
      setJdFile(file)
    }
  }



  const renderParsedData = (data) => {
    if (!data) return null

    return (
      <div className="parsed-data">
        {/* Generated Questions Section */}
        {data.generated_questions && (
          <div className="questions-section">
            <h3>🤖 AI Generated Interview Questions</h3>
            <div className="section">
              {data.generated_questions.questions && (
                <div className="questions-list">
                  {data.generated_questions.questions.map((q, idx) => (
                    <div key={idx} className="question-item">
                      <div className="question-header">
                        <span className="question-number">Q{q.id || idx + 1}</span>
                        <span className={`question-category ${q.category}`}>{q.category}</span>
                        <span className={`question-difficulty ${q.difficulty}`}>{q.difficulty}</span>
                      </div>
                      <p className="question-text">{q.question}</p>
                      {q.focus_area && <p className="focus-area">Focus: {q.focus_area}</p>}
                    </div>
                  ))}
                </div>
              )}
              
              {data.generated_questions.summary && (
                <div className="questions-summary">
                  <h4>📊 Questions Summary</h4>
                  <p>Total Questions: {data.generated_questions.summary.total_questions}</p>
                  <p>Technical: {data.generated_questions.summary.technical_questions}</p>
                  <p>Behavioral: {data.generated_questions.summary.behavioral_questions}</p>
                  <p>Experience: {data.generated_questions.summary.experience_questions}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* AI Error Message */}
        {data.ai_error && (
          <div className="ai-error">
            <h3>⚠️ AI Service Error</h3>
            <p>{data.message}</p>
            <p className="error-detail">{data.ai_error}</p>
          </div>
        )}

        {/* Raw Text Section */}
        <div className="resume-data">
          <h3>📄 Resume Content</h3>
          <div className="section">
            <div className="raw-text-container">
              <pre className="raw-text">{data.resume}</pre>
            </div>
          </div>
        </div>

        <div className="jd-data">
          <h3>💼 Job Description Content</h3>
          <div className="section">
            <div className="raw-text-container">
              <pre className="raw-text">{data.job_description}</pre>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 AI Interview Question Generator</h1>
        <p>Upload your resume and job description to generate personalized interview questions</p>
      </header>

      <main className="main-content">
        <form onSubmit={handleSubmit} className="upload-form">
          <div className="file-inputs">
            <div className="input-group">
              <label htmlFor="resume-file">Upload Resume (.txt, .pdf, .doc, .docx)</label>
              <input
                type="file"
                id="resume-file"
                accept=".txt,.pdf,.doc,.docx"
                onChange={(e) => handleFileChange('resume', e.target.files[0])}
                className="file-input"
              />
              {resumeFile && (
                <p className="file-name">
                  Selected: {resumeFile.name} 
                  {!isSupportedFileType(resumeFile) && 
                    <span className="file-error"> (Unsupported format)</span>
                  }
                </p>
              )}
            </div>

            <div className="input-group">
              <label htmlFor="jd-file">Upload Job Description (.txt, .pdf, .doc, .docx)</label>
              <input
                type="file"
                id="jd-file"
                accept=".txt,.pdf,.doc,.docx"
                onChange={(e) => handleFileChange('jd', e.target.files[0])}
                className="file-input"
              />
              {jdFile && (
                <p className="file-name">
                  Selected: {jdFile.name}
                  {!isSupportedFileType(jdFile) && 
                    <span className="file-error"> (Unsupported format)</span>
                  }
                </p>
              )}
            </div>
          </div>

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? '🔄 Extracting Text...' : '� Extract Text'}
          </button>
        </form>

        {error && (
          <div className="error">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}

        {response && (
          <div className="results">
            {renderParsedData(response)}
          </div>
        )}
      </main>
    </div>
  )
}

export default App
