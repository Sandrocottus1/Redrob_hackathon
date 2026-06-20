import csv
import subprocess
from . import data_loader as dl
from . import text_builder as tb
from . import retriever as rt
from . import ranker as rk
from . import config as cfg

def e_j_s(t):#extract job skills
    return set(t.lower().split())

def e_m_s(r_l):
    if not r_l: return r_l
    m_s=r_l[0][0]
    o=[]
    for s , i , c in r_l:
        m_s=min(m_s,s)
        o.append((m_s,i,c))
    return o

def w_s(r_l,p):#write scores
    with open(p,'w',newline='')as f:
        w=csv.writer(f)
        w.writerow(["candidate_id","score"])
        for s,i,c in r_l:
            w.writerow([i,s])

def r_v(p):#run visualization
    try:
        subprocess.run(["python",cfg.v_s,p])
    except FileNotFoundError:
        pass

def r_p(o_p,d_w,b_w,r_k,r_p_k):
    p=dl.p_c_f(cfg.c_j,cfg.c_j_g)
    c=dl.l_c(p)
    j = dl.l_j_t(cfg.j_t)
    j_s = e_j_s(j)
    t = [tb.b_c_t(x) for x in c]
    h = rt.HybridRetriever(cfg.d_m)
    h.fit(t)
    i_l = h.retrieve(j, r_k, r_p_k, d_w, b_w)
    p_c = [c[i] for i in i_l]
    r = rk.r_c(p_c, j_s, cfg.f_w)
    r = r[:cfg.f_t_k]
    r = e_m_s(r)
    w_s(r, o_p)
    r_v(o_p)



