import csv
import subprocess
import numpy as np
from . import data_loader as dl
from . import text_builder as tb
from . import retriever as rt
from . import ranker as rk
from . import config as cfg

def e_j_s(t):
    return set(t.lower().split())

def e_m_s(r_l):
    if not r_l: return r_l
    m_s = r_l[0][0]
    o = []
    for s, i, c in r_l:
        m_s = min(m_s, s)
        o.append((m_s, i, c))
    return o

def w_s(r_l, p):
    with open(p, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["candidate_id", "rank", "score", "reasoning"])
        for rank, (s, i, c) in enumerate(r_l, start=1):
            profile = c.get("profile", {})
            reasoning = (
                f"Score:{s:.3f}. "
                f"Title:{profile.get('current_title', '')}. "
                f"Exp:{profile.get('years_of_experience', 0)}yrs. "
                f"Industry:{profile.get('current_industry', '')}."
            )
            w.writerow([i, rank, round(s, 6), reasoning])

def r_v(p):
    try:
        subprocess.run(["python", cfg.v_s, p])
    except FileNotFoundError:
        pass

def r_p(o_p, d_w, b_w, r_k, r_p_k):
    p = dl.p_c_f(cfg.c_j, cfg.c_j_g)
    c = dl.l_c(p)
    j = dl.l_j_t(cfg.j_t)
    j_s = e_j_s(j)
    t = [tb.b_c_t(x) for x in c]

    h = rt.HybridRetriever(cfg.d_m)
    h.fit(t)
    i_l, h_s = h.retrieve(j, r_k, r_p_k, d_w, b_w)
    p_c = [c[i] for i in i_l]
    p_hs = h_s[np.array(i_l)]  # fix: convert to numpy array first
    r = rk.r_c(p_c, j_s, cfg.f_w, h_s=p_hs)

    w_s(r, o_p)
    r_v(o_p)