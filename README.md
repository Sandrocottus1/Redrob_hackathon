# 🎯 AI-Powered Candidate Ranking System

> **India RUNS Data & AI Challenge — Redrob × Hack2Skill**

<div align="center">

### Ranking **100,000+ candidates** fairly using **Semantic Search, Talent Signals, and Fraud Detection**

**⚡ Processes 100K profiles in under 5 minutes** • **🤖 Hybrid AI Ranking** • **🔍 Transparent Reasoning**

</div>

---

# 📌 Overview

Recruiters often receive **100,000+ applications** for a single job posting. Traditional Applicant Tracking Systems (ATS) primarily rely on keyword matching, making them vulnerable to:

* 📋 Massive application volume
* 🔤 Keyword stuffing
* 🎭 Fake or inflated candidate profiles
* ❌ Poor transparency in ranking decisions

This project introduces a **4-stage AI ranking pipeline** that combines semantic search, behavioral signals, objective skill assessments, and fraud detection to identify the **Top 100 best-fit candidates** while generating transparent, fact-based explanations for every ranking.

---

# 🚀 Key Features

* ✅ Hybrid Semantic Search (Sentence Transformers + FAISS + BM25)
* ✅ Scores candidates using **23 objective talent signals**
* ✅ Detects suspicious or manipulated profiles
* ✅ Generates transparent reasoning without using LLM hallucinations
* ✅ Processes **100,000 candidates in ~4.4 minutes**
* ✅ Produces competition-ready submission CSV

---

# 🏗️ Pipeline Overview

```
Candidates (100K JSONL)
          │
          ▼
Load & Parse
          │
          ▼
Structured Profile Builder
          │
          ▼
Sentence Transformer Encoding
          │
          ▼
Hybrid Retrieval
 (FAISS + BM25)
          │
          ▼
Top 5,000 Candidates
          │
          ▼
Talent Scoring
          │
          ▼
Penalty Detection
          │
          ▼
Top 100 Ranked Candidates
          │
          ▼
submission.csv
```

---

# 📂 Project Structure

```
Redrob_hackathon/

├── solution/
│   ├── config.py
│   ├── data_loader.py
│   ├── text_builder.py
│   ├── retriever.py
│   ├── features.py
│   ├── ranker.py
│   ├── pipeline.py
│   └── main.py
│
├── India_runs_data_and_ai_challenge/
│   ├── candidates.jsonl.gz
│   ├── job_description_paragraphs.txt
│   └── validate_submission.py
│
├── submission_metadata.yaml
├── app.py
└── README.md
```

---

# ⚙️ Stage 1 — Data Loading

The pipeline reads the compressed **100K candidate dataset** and extracts structured information including:

* Candidate title
* Industry
* Skills
* Career history
* Years of experience
* Education
* Skill assessment scores
* GitHub activity
* Platform engagement signals
* Availability information
* Recruiter interaction metrics

---

# 🧠 Stage 2 — Semantic Encoding

Every candidate profile is converted into structured text before being embedded using:

```
sentence-transformers/all-MiniLM-L6-v2
```

Each profile becomes a **384-dimensional vector**.

Example:

```
Title: Backend Engineer
Industry: FinTech
Experience: 3 Years
Skills:
Python
Docker
Redis

Assessment:
Python 84/100
```

↓

```
384-Dimensional Embedding
```

Both indexes are then built:

* FAISS Vector Index
* BM25 Keyword Index

---

# 🔍 Stage 3 — Hybrid Candidate Retrieval

Instead of scoring all 100K candidates, the system first retrieves the **Top 5,000 most relevant profiles**.

### Semantic Search

* FAISS Cosine Similarity
* Weight: **92%**

Captures contextual similarity instead of relying on exact keywords.

### Keyword Search

* BM25
* Weight: **8%**

Ensures important technologies and tool names are not missed.

---

# 📊 Stage 4 — Talent Scoring

Each retrieved candidate is evaluated using weighted objective signals.

| Signal             | Weight |
| ------------------ | ------ |
| Semantic Match     | 25%    |
| Skill Assessments  | 20%    |
| GitHub Activity    | 10%    |
| Engagement Quality | 10%    |
| Market Validation  | 10%    |
| Recency            | 8%     |
| Career Progression | 7%     |
| Availability       | 6%     |
| Verified Signals   | 3%     |
| Experience Fit     | 1%     |

---

# 🚨 Fraud & Honeypot Detection

The system penalizes suspicious profiles using deterministic rules.

| Detection                  | Penalty |
| -------------------------- | ------- |
| Irrelevant Job Title       | ×0.05   |
| Impossible Career Timeline | ×0.20   |
| Skill Inflation            | ×0.10   |
| Ghost Profile              | ×0.30   |
| Inactive > 1 Year          | ×0.40   |
| Buzzword-only AI Profile   | ×0.60   |

These penalties reduce ranking scores while maintaining transparency.

---

# 💬 Transparent Candidate Reasoning

Every recommendation is generated **without using an LLM**.

The reasoning engine simply formats verified structured data.

Example:

```
Search Engineer with 7 years of experience in Internet.
Key skills include SAP, Kubeflow and Embeddings.
Scored 88/100 in Embeddings assessment.
GitHub activity: 83/100.
3 out of 3 previous roles are technical.
Concern: Notice period of 120 days.
```

✔ No hallucinations

✔ No invented facts

✔ Fully traceable to source data

---

# 📈 Performance

| Metric               | Result       |
| -------------------- | ------------ |
| Candidates Processed | 100,000      |
| Runtime              | ~4.4 Minutes |
| Peak RAM             | ~3 GB        |
| Validation Errors    | 0            |
| Output Candidates    | 100          |

---

# 🛠 Technology Stack

| Tool                  | Purpose                  |
| --------------------- | ------------------------ |
| Python 3.12           | Core pipeline            |
| Sentence Transformers | Semantic embeddings      |
| FAISS                 | Vector similarity search |
| rank-bm25             | Keyword retrieval        |
| Pandas                | Data processing          |
| NumPy                 | Numerical computation    |
| Gradio                | Interactive demo         |
| Google Colab T4       | Execution environment    |

---

# 🚀 Running the Project

Clone the repository

```bash
git clone https://github.com/Sandrocottus1/Redrob_hackathon.git

cd Redrob_hackathon
```

Install dependencies

```bash
pip install -r solution/requirements.txt
```

Place

```
candidates.jsonl.gz
```

inside

```
India_runs_data_and_ai_challenge/
```

Run the pipeline

```bash
python -m solution.main --out final_submission.csv
```

Validate the submission

```bash
python India_runs_data_and_ai_challenge/validate_submission.py final_submission.csv
```

---

# ☁️ Running on Google Colab

```python
!pip install sentence-transformers faiss-cpu rank-bm25==0.2.2 pandas numpy PyYAML -q

!git clone https://github.com/Sandrocottus1/Redrob_hackathon.git

%cd Redrob_hackathon

# Upload candidates.jsonl.gz

!python -m solution.main --out final_submission.csv
```

---

# 🌐 Interactive Demo

A lightweight Gradio application allows users to:

* Upload candidate JSON files
* Paste a job description
* Generate ranked candidates instantly
* Download the resulting CSV

---

# ✅ Submission Validation

The generated output satisfies all competition requirements:

* Exactly 100 candidates
* Rank values from 1–100
* Monotonically decreasing scores
* Required output schema
* Zero validation errors
* Deterministic reasoning
* Runtime within competition limits

---

# 👨‍💻 Author

**Aryan Yadav**

B.Tech Computer Science & Engineering

National Institute of Technology Silchar (2026)

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a star!

Built for the **India RUNS Data & AI Challenge** hosted by **Redrob × Hack2Skill**

</div>
