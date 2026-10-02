from fastapi import FastAPI, UploadFile, File, Form
from pypdf import PdfReader
import io
import math
import re
from collections import Counter

# 1. Initialize FastAPI app
app = FastAPI(title="TalentMatch AI Backend")

# 2. Extract text from PDF in memory
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    pdf_file_in_memory = io.BytesIO(pdf_bytes)
    reader = PdfReader(pdf_file_in_memory)
    
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + " "
    return full_text.strip()

# 3. Pure Python Cosine Similarity (No heavy C++ library needed!)
def calculate_match_score(resume_text: str, jd_text: str) -> float:
    # Common English words to ignore
    stop_words = {"the", "and", "is", "in", "to", "of", "for", "with", "a", "an", "on", "at", "by", "from", "as", "this", "that"}
    
    # Extract clean words
    words_resume = [w for w in re.findall(r'\b[a-zA-Z]{2,}\b', resume_text.lower()) if w not in stop_words]
    words_jd = [w for w in re.findall(r'\b[a-zA-Z]{2,}\b', jd_text.lower()) if w not in stop_words]
    
    if not words_resume or not words_jd:
        return 0.0
        
    # Count frequencies of words
    tf_resume = Counter(words_resume)
    tf_jd = Counter(words_jd)
    
    # Calculate Dot Product
    vocabulary = set(tf_resume.keys()).union(set(tf_jd.keys()))
    dot_product = sum(tf_resume.get(w, 0) * tf_jd.get(w, 0) for w in vocabulary)
    
    # Calculate Magnitudes (Lengths of the arrows)
    mag_resume = math.sqrt(sum(val ** 2 for val in tf_resume.values()))
    mag_jd = math.sqrt(sum(val ** 2 for val in tf_jd.values()))
    
    if mag_resume == 0 or mag_jd == 0:
        return 0.0
        
    # Cosine Similarity Formula: (A . B) / (||A|| * ||B||)
    similarity = dot_product / (mag_resume * mag_jd)
    return round(float(similarity) * 100, 2)

# 4. The API Endpoint
@app.post("/analyze")
async def analyze_candidate(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    file_bytes = await resume.read()
    resume_text = extract_text_from_pdf(file_bytes)
    
    if not resume_text:
        return {"error": "Could not read text from uploaded PDF."}
    
    score = calculate_match_score(resume_text, job_description)
    
    skills_to_check = ["python", "java", "sql", "docker", "fastapi", "django", "aws", "git", "pytest", "selenium"]
    matched = [s for s in skills_to_check if s in resume_text.lower() and s in job_description.lower()]
    missing = [s for s in skills_to_check if s in job_description.lower() and s not in resume_text.lower()]
    
    return {
        "filename": resume.filename,
        "match_percentage": score,
        "matched_skills": matched,
        "missing_skills": missing
    }

# 5. Start Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)