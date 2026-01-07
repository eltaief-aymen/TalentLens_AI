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


def normalize_skills(text: str) -> list[str]:
    text = text.lower()
    found = []

    for canonical, variants in SKILL_ONTOLOGY.items():
        if any(v in text for v in variants):
            found.append(canonical)

    return found
