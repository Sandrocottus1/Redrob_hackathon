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
    "sem": 0.28,
    "ass": 0.25,
    "git": 0.12,
    "ver": 0.10,
    "car": 0.08,
    "eng": 0.08,
    "exp": 0.05,
    "not": 0.04,
}
