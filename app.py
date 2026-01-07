import streamlit as st
import tempfile
import json

from screener.pipeline import screen_resume

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("📄 AI Resume Screener")
st.caption("Privacy-Preserving • Local LLM • Bias-Aware")

# -------------------------------------------------
# Sidebar (Job Description)
# -------------------------------------------------
st.sidebar.header("🧾 Job Description")

job_description = st.sidebar.text_area(
    "Paste the job description here",
    height=300,
    placeholder="Required skills, experience, role description..."
)

run_button = st.sidebar.button("🚀 Run Screening")

# -------------------------------------------------
# Resume Upload
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Candidate Resume (PDF)",
    type=["pdf"]
)

# -------------------------------------------------
# Execution
# -------------------------------------------------
if run_button:

    if not uploaded_file or not job_description.strip():
        st.warning("Please upload a resume and provide a job description.")
        st.stop()

    with st.spinner("Analyzing resume..."):
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                resume_path = tmp.name

            result = screen_resume(resume_path, job_description)

        except Exception as e:
            st.error(f"Screening failed: {e}")
            st.stop()

    # -------------------------------------------------
    # Results
    # -------------------------------------------------
    st.success("Analysis completed")

    col1, col2, col3 = st.columns(3)

    col1.metric("Final Score", f"{result['final_score']} / 100")
    col2.metric("Decision", result["decision"])
    col3.metric("Matched Skills", len(result["matched_skills"]))

    # -------------------------------------------------
    # Skills
    # -------------------------------------------------
    st.subheader("🧠 Skills Analysis")

    st.write("**Matched Skills**")
    st.success(", ".join(result["matched_skills"]) or "None")

    st.write("**Missing Skills**")
    st.warning(", ".join(result["missing_skills"]) or "None")

    # -------------------------------------------------
    # LLM Explanation
    # -------------------------------------------------
    st.subheader("🤖 AI Recruiter Reasoning")

    st.write("**Experience Level:**",
             result["llm_analysis"]["candidate_profile"]["estimated_experience_level"])

    st.write("**Relevant Domains:**",
             ", ".join(result["llm_analysis"]["candidate_profile"]["relevant_domains"]))

    st.write("**Strengths**")
    for s in result["llm_analysis"]["strengths"]:
        st.write(f"✔️ {s}")

    st.write("**Weaknesses**")
    for w in result["llm_analysis"]["weaknesses"]:
        st.write(f"⚠️ {w}")

    st.info(result["llm_analysis"]["reasoning"])

    # -------------------------------------------------
    # JSON Export
    # -------------------------------------------------
    st.download_button(
        "📥 Download Full JSON Report",
        json.dumps(result, indent=2),
        file_name="ai_screening_report.json",
        mime="application/json"
    )
