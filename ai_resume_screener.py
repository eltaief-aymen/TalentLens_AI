"""
AI Resume Screener (Production-Ready, Local LLM)

Author: Eltaief Aymen
Description:
A privacy-preserving AI resume screening system using Python and Llama 3 (Ollama).
Designed for real-world HR use: structured parsing, bias-aware anonymization,
hybrid scoring, explainable outputs, and robust JSON handling.

Requirements:
- ollama
- pymupdf

Install:
pip install ollama pymupdf
"""

import json
import re
import logging
from typing import Dict, List, Any

import fitz  # PyMuPDF
import ollama

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

MODEL_NAME = "llama3.1:8b"
LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL, format="%(levelname)s | %(message)s")

# Skill normalization dictionary (extensible)
SKILL_ONTOLOGY = {
    "python": ["python"],
    "sql": ["sql", "postgresql", "mysql"],
    "machine_learning": [
        "machine learning", "ml", "random forest",
        "linear regression", "svm", "classification"
    ],
    "aws": ["aws", "amazon web services", "ec2", "s3"],
    "nlp": ["nlp", "natural language processing", "transformers"]
}

# ------------------------------------------------------------------
# 1. Resume Reader (Robust PDF extraction)
# ------------------------------------------------------------------

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract raw text from a PDF resume using PyMuPDF.
    """
    try:
        doc = fitz.open(pdf_path)
        pages = [page.get_text() for page in doc]
        text = "\n".join(pages)
        logging.info("Resume successfully extracted.")
        return text.strip()
    except Exception as e:
        logging.error(f"Failed to read PDF: {e}")
        raise

# ------------------------------------------------------------------
# 2. Anonymization (Bias mitigation)
# ------------------------------------------------------------------

def anonymize_resume(text: str) -> str:
    """
    Remove bias-sensitive information such as names and emails.
    """
    text = re.sub(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", "[REDACTED_NAME]", text)
    text = re.sub(r"\S+@\S+", "[REDACTED_EMAIL]", text)
    text = re.sub(r"\+?\d[\d\s\-]{8,}", "[REDACTED_PHONE]", text)
    return text

# ------------------------------------------------------------------
# 3. Skill Normalization (Deterministic Layer)
# ------------------------------------------------------------------

def normalize_skills(text: str) -> List[str]:
    """
    Extract normalized skills from resume text using ontology matching.
    """
    text_lower = text.lower()
    found_skills = []

    for canonical, variants in SKILL_ONTOLOGY.items():
        for variant in variants:
            if variant in text_lower:
                found_skills.append(canonical)
                break

    return found_skills

# ------------------------------------------------------------------
# 4. LLM Analysis (Semantic Reasoning Layer)
# ------------------------------------------------------------------

def llm_resume_analysis(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Uses Llama 3 to perform semantic resume-to-JD matching.
    Returns structured JSON.
    """

    prompt = f"""
You are a Senior Technical Recruiter with 20+ years of experience.

RULES:
- Be objective, strict, and fair
- Do NOT infer age, gender, nationality
- Base decisions only on skills and experience
- Output VALID JSON ONLY

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_text}

OUTPUT FORMAT:
{{
  "candidate_profile": {{
    "estimated_experience_level": "Junior | Mid | Senior",
    "relevant_domains": ["list"]
  }},
  "strengths": ["max 3"],
  "weaknesses": ["max 3"],
  "semantic_match_score": 0-100,
  "recommendation": "Interview" | "Reject",
  "reasoning": "2 sentence justification"
}}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response["message"]["content"]
    clean_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(clean_output)
    except json.JSONDecodeError:
        logging.error("LLM returned invalid JSON.")
        raise ValueError(clean_output)

# ------------------------------------------------------------------
# 5. Hybrid Scoring Engine
# ------------------------------------------------------------------

def compute_final_score(
    llm_score: int,
    matched_skills: List[str],
    required_skills: List[str]
) -> int:
    """
    Combine semantic score with deterministic skill coverage.
    """
    skill_coverage = len(set(matched_skills) & set(required_skills)) / max(len(required_skills), 1)
    skill_score = skill_coverage * 100

    final_score = int((0.6 * llm_score) + (0.4 * skill_score))
    return final_score

# ------------------------------------------------------------------
# 6. Orchestrator (Main pipeline)
# ------------------------------------------------------------------

def screen_resume(pdf_path: str, job_description: str) -> Dict[str, Any]:
    """
    End-to-end resume screening pipeline.
    """

    raw_text = extract_text_from_pdf(pdf_path)
    anonymized_text = anonymize_resume(raw_text)
    extracted_skills = normalize_skills(anonymized_text)

    llm_result = llm_resume_analysis(anonymized_text, job_description)

    required_skills = normalize_skills(job_description)

    final_score = compute_final_score(
        llm_score=llm_result["semantic_match_score"],
        matched_skills=extracted_skills,
        required_skills=required_skills
    )

    decision = "Interview" if final_score >= 70 else "Reject"

    return {
        "final_score": final_score,
        "decision": decision,
        "matched_skills": extracted_skills,
        "missing_skills": list(set(required_skills) - set(extracted_skills)),
        "llm_analysis": llm_result
    }

# ------------------------------------------------------------------
# 7. Example Execution
# ------------------------------------------------------------------

if __name__ == "__main__":

    JOB_DESCRIPTION = """
    Junior Data Scientist role.
    Required:
    - Python
    - SQL
    - Machine Learning
    Nice to have:
    - AWS
    - NLP
    """

    RESUME_PATH = "Aymen_Eltaief_AI&Data_Engineer_CV.pdf"  # Change to your resume path

    logging.info("Starting AI Resume Screening...")

    try:
        result = screen_resume(RESUME_PATH, JOB_DESCRIPTION)

        print("\n====== AI SCREENING REPORT ======")
        print(f"Final Score: {result['final_score']}/100")
        print(f"Decision: {result['decision']}")
        print(f"Matched Skills: {result['matched_skills']}")
        print(f"Missing Skills: {result['missing_skills']}")
        print("Reasoning:", result["llm_analysis"]["reasoning"])

    except Exception as e:
        logging.error(f"Screening failed: {e}")
