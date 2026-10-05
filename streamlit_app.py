import os
import tempfile
from pathlib import Path

import streamlit as st

from agent import agent as resume_agent
from job_parser import job_parser_agent
from matcher import matcher_agent
from resume_reader import extract_resume_text
    

st.set_page_config(
    page_title="Resume Match Studio",
    page_icon="R",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f4f1ea 0%, #e7eef0 100%);
    }
    .block-container {
        max-width: 1180px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3 {
        color: #1c2d35;
    }
    .eyebrow {
        color: #b45132;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid rgba(28, 45, 53, 0.12);
        border-radius: 8px;
        padding: 1rem 1.1rem;
        min-height: 110px;
    }
    .metric-label {
        color: #607078;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-value {
        color: #1c2d35;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 0.35rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="eyebrow">Candidate intelligence</div>', unsafe_allow_html=True)
st.title("Resume Match Studio")
st.write("Upload one resume, paste a role description, and inspect the match in real time.")

resume_file = st.file_uploader(
    "Resume file",
    type=["pdf", "docx", "txt", "text", "csv", "xlsx", "xls"],
)
job_description = st.text_area(
    "Job description",
    height=260,
    placeholder="Paste the complete job description here...",
)

run_analysis = st.button("Analyze resume", type="primary", use_container_width=True)

if run_analysis:
    if resume_file is None:
        st.warning("Upload a PDF, DOCX, TXT, CSV, XLSX, or XLS resume first.")
    elif not job_description.strip():
        st.warning("Paste a job description first.")
    else:
        temporary_path = None
        try:
            suffix = Path(resume_file.name).suffix.lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temporary_file:
                temporary_file.write(resume_file.getvalue())
                temporary_path = temporary_file.name

            with st.spinner("Reading and parsing the resume..."):
                resume_text = extract_resume_text(temporary_path)
                resume_response = resume_agent.run(
                    f"""
                    Parse the following resume and extract the candidate
                    information according to the required schema.

                    RESUME:
                    {resume_text}
                    """
                )
                resume = resume_response.content

            with st.spinner("Parsing the job description..."):
                job_response = job_parser_agent.run(
                    f"""
                    Parse the following job description into structured requirements.

                    JOB DESCRIPTION:
                    {job_description}
                    """
                )
                job_requirements = job_response.content

            with st.spinner("Calculating the job match..."):
                match_response = matcher_agent.run(
                    f"""
                    Compare the following candidate resume with the structured
                    job requirements. Treat required skills and preferred skills
                    separately. Do not make a hiring decision.

                    CANDIDATE RESUME:
                    {resume.model_dump_json()}

                    JOB REQUIREMENTS:
                    {job_requirements.model_dump_json()}
                    """
                )
                match = match_response.content

            st.success("Analysis complete")

            first_row = st.columns(3)
            with first_row[0]:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">Candidate</div>'
                    f'<div class="metric-value">{resume.name or "Not found"}</div></div>',
                    unsafe_allow_html=True,
                )
            with first_row[1]:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">Role</div>'
                    f'<div class="metric-value">{job_requirements.job_title or "Not found"}</div></div>',
                    unsafe_allow_html=True,
                )
            with first_row[2]:
                st.markdown(
                    f'<div class="metric-card"><div class="metric-label">Required match</div>'
                    f'<div class="metric-value">{match.matching_percentage:.1f}%</div></div>',
                    unsafe_allow_html=True,
                )

            st.divider()
            left, right = st.columns(2)
            with left:
                st.subheader("Matching skills")
                st.write(match.matching_skills or "No matching skills identified.")
                st.subheader("Candidate strengths")
                st.write(match.strengths or "No strengths identified.")
            with right:
                st.subheader("Missing skills")
                st.write(match.missing_skills or "No missing skills identified.")
                st.subheader("Skill gaps")
                st.write(match.skill_gaps or "No skill gaps identified.")

            st.subheader("Analysis")
            st.write(match.analysis or "No analysis returned.")

            with st.expander("Parsed job requirements"):
                st.json(job_requirements.model_dump())
            with st.expander("Parsed resume"):
                st.json(resume.model_dump())

        except Exception as error:
            st.error(f"Analysis failed: {error}")
            if not os.getenv("GROQ_API_KEY"):
                st.info("Add GROQ_API_KEY to your .env file before running the analysis.")
        finally:
            if temporary_path:
                Path(temporary_path).unlink(missing_ok=True)
