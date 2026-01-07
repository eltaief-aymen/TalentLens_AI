def compute_final_score(
    llm_score: int,
    matched_skills: list[str],
    required_skills: list[str]
) -> int:

    coverage = len(set(matched_skills) & set(required_skills)) / max(len(required_skills), 1)
    skill_score = coverage * 100

    return int(0.6 * llm_score + 0.4 * skill_score)
