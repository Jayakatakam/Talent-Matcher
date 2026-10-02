**# 🎯 TalentMatch AI — Candidate Screener Microservice**



**An intelligent talent screening tool inspired by Phenom's Talent Experience Management domain.** 

**It analyzes candidate resumes against Job Descriptions using Natural Language Processing (NLP)** 

**to calculate semantic match scores and detect skill gaps.**



**## 🚀 Architecture**

**- \*\*Backend:\*\* FastAPI (Python) - High performance asynchronous REST API**

**- \*\*Frontend:\*\* Streamlit - Clean, interactive recruiter dashboard**

**- \*\*NLP / Matching Engine:\*\* Pure Python Vectorization with Cosine Similarity math**

**- \*\*Document Parser:\*\* PyPDF (in-memory stream processing)**



**## 🛠️ Key Features**

**- \*\*In-Memory File Processing:\*\* Uses io.BytesIO to read PDFs directly in RAM without disk latency.**

**- \*\*Vector Cosine Similarity:\*\* Quantifies document similarity based on direction rather than length differences.**

**- \*\*Skill Gap Detection:\*\* Highlights matching competencies and flags missing job requirements.**

**- \*\*Interactive API Docs:\*\* Auto-generated Swagger UI at /docs.**



**## 📦 How to Run Locally**



**1. Clone the repository:**

**git clone https://github.com/Jayakatakam/Talent-Matcher.git**

**cd talent-matcher**



**2. Create and activate virtual environment:**

**py -m venv venv**

**.\\venv\\Scripts\\Activate.ps1**



**3. Install dependencies:**

**pip install -r requirements.txt**



**4. Start Backend (Terminal 1):**

**python main.py**



**5. Start Frontend (Terminal 2):**

**streamlit run app.py**

