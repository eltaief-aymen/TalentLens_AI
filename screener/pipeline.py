from .reader import extract_text_from_pdf
from .anonymizer import anonymize_resume
from .skills import normalize_skills
from .llm import analyze_resume
from .scoring import compute_final_score


def screen_resume(pdf_path: str, job_description: str) -> dict:

    raw_text = extract_text_from_pdf(pdf_path)
    anonymized = anonymize_resume(raw_text)

    matched_skills = normalize_skills(anonymized)
    required_skills = normalize_skills(job_description)

    llm_result = analyze_resume(anonymized, job_description)

    final_score = compute_final_score(
        llm_result["semantic_match_score"],
        matched_skills,
        required_skills
    )

    decision = "Interview" if final_score >= 70 else "Reject"

    return {
        "final_score": final_score,
        "decision": decision,
        "matched_skills": matched_skills,
        "missing_skills": list(set(required_skills) - set(matched_skills)),
        "llm_analysis": llm_result
    }
