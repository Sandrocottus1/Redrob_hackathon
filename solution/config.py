from pathlib import Path

r_d = Path(__file__).resolve().parent.parent
d_d = r_d / "India_runs_data_and_ai_challenge"

c_j   = d_d / "candidates.jsonl.gz"
c_j_g = d_d / "candidates.jsonl.gz"
j_t   = d_d / "job_description_paragraphs.txt"
v_s   = d_d / "validate_submission.py"
d_o   = r_d / "submission.csv"

d_m = "sentence-transformers/all-MiniLM-L6-v2"

r_k   = 3000
r_p_k = 1500
f_t_k = 100

d_w = 0.92
b_w = 0.08

f_w = {
    "sem": 0.25,  # semantic JD match
    "ass": 0.20,  # assessment scores
    "git": 0.10,  # github activity
    "car": 0.07,  # career progression
    "eng": 0.10,  # engagement (icr, oar, response rate/time)
    "mkt": 0.10,  # market validation (views, saves, connections)
    "rec": 0.08,  # recency (last active, signup tenure)
    "avl": 0.05,  # availability (open to work, notice, mode, relocate)
    "ver": 0.03,  # verified signals (email, phone, linkedin, salary, completeness)
    "exp": 0.01,  # years of experience
    "not": 0.01,  # notice period (already in avl but kept separate)
}
