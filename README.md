# 🧠 TalentLens AI  
### Privacy-Preserving, Explainable AI Resume Screening System

**TalentLens AI** is a local, production-oriented AI system designed to help recruiters and hiring teams evaluate candidates objectively, fairly, and securely by matching resumes against job descriptions.

Built with **Python** and **Llama 3 (via Ollama)**, TalentLens AI goes far beyond traditional keyword-based screening. It combines **semantic reasoning**, **bias-aware anonymization**, and a **hybrid scoring engine**, while ensuring that **candidate data never leaves the local environment**.

This project is designed as a **real-world HR intelligence system**, not a demo.

---

## 🎯 Why TalentLens AI?

Modern hiring tools often suffer from:
- Black-box decisions
- Biased screening
- Cloud-based data leakage
- Shallow keyword matching

**TalentLens AI addresses these challenges** by prioritizing:
- Privacy
- Explainability
- Fairness
- Engineering rigor

---

## ✨ Key Features

- 🔒 **Privacy-first & fully local inference**  
  All processing runs locally using Ollama — no external APIs, no data leakage.

- 📄 **Robust PDF resume parsing**  
  Reliable text extraction from real-world resumes.

- ⚖️ **Bias-aware anonymization**  
  Automatically removes names, emails, and phone numbers before evaluation.

- 🧠 **LLM-powered semantic evaluation**  
  Uses Llama 3 to reason about skills, experience, and job relevance.

- 🔎 **Hybrid scoring engine**  
  Combines semantic AI reasoning with deterministic skill coverage for balanced decisions.

- 🧾 **Explainable AI outputs**  
  Every decision includes strengths, weaknesses, reasoning, and confidence signals.

- 📊 **Structured JSON results**  
  ATS-ready, auditable, and easy to integrate downstream.

- 🧩 **Clean, modular architecture**  
  Designed for extensibility, testing, and production deployment.

---

## 🏗 System Architecture

TalentLens AI follows a clear, layered processing pipeline:

1. **Resume Reader**  
   Extracts raw text from PDF resumes using layout-aware parsing.

2. **Anonymization Layer**  
   Removes bias-sensitive information (names, emails, phone numbers).

3. **Skill Normalization Engine**  
   Matches candidate skills against a predefined ontology.

4. **LLM Intelligence Layer**  
   Performs semantic reasoning between the resume and the job description.

5. **Hybrid Scoring Engine**  
   Combines AI semantic scores with deterministic skill coverage.

6. **Decision & Explanation Layer**  
   Produces a final score, recommendation, and human-readable reasoning.

---

## 📁 Project Structure

```text
TalentLens_AI/
│
├── app.py                     # Streamlit recruiter interface
├── screener/
│   ├── config.py              # Global configuration
│   ├── reader.py              # PDF extraction
│   ├── anonymizer.py          # Bias mitigation
│   ├── skills.py              # Skill ontology & normalization
│   ├── llm.py                 # LLM interaction & JSON handling
│   ├── scoring.py             # Hybrid scoring logic
│   └── pipeline.py            # End-to-end orchestration
│
├── requirements.txt
└── README.md
