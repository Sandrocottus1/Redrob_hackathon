from pathlib import Path

r_d = Path(__file__).resolve().parent.parent
d_d = r_d / "India_runs_data_and_ai_challenge"

c_j = d_d / "sample_candidates.json"
c_j_g = d_d / "sample_candidates.json"
j_t = d_d / "job_description_paragraphs.txt"
v_s = d_d / "validate_submission.py"
d_o = r_d / "submission.csv"

d_m = "sentence-transformers/all-MiniLM-L6-v2"

r_k = 3000
r_p_k = 1500
f_t_k = 50

d_w = 0.92
b_w = 0.08

f_w = {
    "skl": 0.05, # keyword skill overlap
    "prd": 0.05,  # production keyword signals
    "exp": 0.05, # years experience
    "beh": 0.03,  # behavioural keywords
    "loc": 0.02,# location
    "not": 0.02,# notice period
    "sem": 0.30,# semantic JD match (embedding cosine sim)
    "ass": 0.25,    # actual assessment scores
    "git": 0.13, # github activity
    "eng": 0.10, #engagement
}