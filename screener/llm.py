import json
import logging
import re
import ollama
from .config import MODEL_NAME


def extract_json_from_text(text: str) -> dict:
    """
    Extract the first valid JSON object from text.
    """
    try:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError("No JSON object found")

        return json.loads(match.group())
    except Exception as e:
        logging.error("Failed to extract JSON from LLM output")
        raise ValueError(text)


def analyze_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are a Senior Technical Recruiter with 20+ years of experience.

STRICT RULES:
- Output ONLY valid JSON
- No explanations, no comments, no markdown
- Do NOT add any text before or after JSON

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
  "recommendation": "Interview | Reject",
  "reasoning": "2 sentence justification"
}}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response["message"]["content"]

    return extract_json_from_text(raw_output)
