# 🧠 TalentLens AI  
### Privacy-Preserving AI Resume Screening System

**TalentLens AI** is a local, production-oriented AI system designed to help recruiters and hiring teams objectively evaluate candidates by matching resumes against job descriptions.

Built with **Python** and **Llama 3 (via Ollama)**, the system goes beyond keyword matching by combining **semantic analysis**, **bias-aware anonymization**, and **hybrid scoring**, while ensuring that sensitive candidate data never leaves the local machine.

---

## ✨ Key Features

- 🔒 **Privacy-first & fully local inference** (GDPR-friendly)
- 📄 **Robust PDF resume parsing**
- 🧠 **LLM-powered semantic candidate evaluation**
- ⚖️ **Bias-aware anonymization** (removes names, emails, phone numbers)
- 🔎 **Hybrid scoring engine** (LLM reasoning + deterministic skill matching)
- 📊 **Structured JSON outputs** for downstream processing
- 🧩 Clean, modular, and extensible system design

---

## 🏗 System Architecture

TalentLens AI follows a clear and maintainable processing pipeline:

1. **Resume Reader**  
   Extracts raw text from PDF resumes using layout-aware parsing.

2. **Anonymization Layer**  
   Removes bias-sensitive information to support fair evaluation.

3. **Skill Normalization Engine**  
   Matches candidate skills using a predefined skill ontology.

4. **LLM Intelligence Layer**  
   Uses Llama 3 to perform semantic analysis against job requirements.

5. **Hybrid Scoring Engine**  
   Combines AI-based reasoning with rule-based skill coverage.

---

## 📦 Requirements

- Python **3.9+**
- [Ollama](https://ollama.com) (local LLM runtime)
- Llama 3 model
