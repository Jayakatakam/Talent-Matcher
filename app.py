import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="Phenom Talent Screener", page_icon="🎯", layout="wide")

st.title("🎯 TalentMatch AI — Candidate Screener")
st.caption("Built with FastAPI + Streamlit | Designed for Talent Intelligence")

# 2. Two Columns Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Job Description")
    jd_input = st.text_area(
        "Paste the Job Description (JD):",
        height=220,
        placeholder="Looking for a Python Backend Developer skilled in FastAPI, Docker, Git, SQL, and PyTest..."
    )

with col2:
    st.subheader("2. Candidate Resume")
    uploaded_file = st.file_uploader("Upload Resume (PDF format)", type=["pdf"])

st.divider()

# 3. Analyze Button
if st.button("🚀 Analyze Candidate", type="primary"):
    if not jd_input.strip() or not uploaded_file:
        st.warning("⚠️ Please provide BOTH a Job Description and a Resume PDF.")
    else:
        with st.spinner("Processing resume with backend NLP engine..."):
            try:
                # Prepare data to send to FastAPI
                files = {"resume": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                data = {"job_description": jd_input}
                
                # Send HTTP POST request to backend
                api_url = "http://127.0.0.1:8000/analyze"
                response = requests.post(api_url, data=data, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    score = result["match_percentage"]
                    
                    st.success("✅ Analysis Complete!")
                    st.metric(label="Overall Match Score", value=f"{score}%")
                    st.progress(min(int(score), 100))
                    
                    # Display skills
                    s_col1, s_col2 = st.columns(2)
                    with s_col1:
                        st.subheader("✅ Matched Skills")
                        if result["matched_skills"]:
                            for s in result["matched_skills"]:
                                st.write(f"• **{s.upper()}**")
                        else:
                            st.write("None of the targeted common skills matched.")
                            
                    with s_col2:
                        st.subheader("⚠️ Missing Skills from JD")
                        if result["missing_skills"]:
                            for s in result["missing_skills"]:
                                st.write(f"• :red[**{s.upper()}**]")
                        else:
                            st.write("No major skill gaps identified!")
                else:
                    st.error(f"Error from server: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot reach FastAPI! Make sure `main.py` is running on Port 8000.")