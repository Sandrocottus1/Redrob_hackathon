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
    for s,i,c in r_l:
        m_s = min(m_s,s)
        o.append((m_s,i,c))
    return o

def build_reasoning(c, rank):
    profile  = c.get("profile",{})
    sig      = c.get("redrob_signals",{})
    title    = profile.get("current_title","Unknown")
    exp      = float(profile.get("years_of_experience",0) or 0)
    industry = profile.get("current_industry","")
    skills   = [s.get("name","") for s in c.get("skills",[]) if isinstance(s,dict)][:3]
    assessments = sig.get("skill_assessment_scores",{})
    github   = sig.get("github_activity_score",-1)
    notice   = sig.get("notice_period_days",0)
    open_work= sig.get("open_to_work_flag",False)
    icr      = sig.get("interview_completion_rate",0)
    career   = c.get("career_history",[])
    tech_kw  = ["engineer","developer","scientist","analyst","architect",
                "programmer","sde","backend","data","ml","ai","nlp"]
    tech_count = sum(1 for r in career
                     if any(t in r.get("title","").lower() for t in tech_kw))

    parts = [title + " with " + str(int(exp)) + " years of experience in " + industry]
    if skills:
        parts.append("key skills: " + ", ".join(skills))
    if assessments:
        top = max(assessments.items(), key=lambda x: x[1])
        parts.append("scored " + str(int(top[1])) + "/100 on " + top[0] + " assessment")
    if github >= 0:
        parts.append("GitHub activity " + str(int(github)) + "/100")
    if tech_count > 0:
        parts.append(str(tech_count) + "/" + str(len(career)) + " roles in tech")

    concerns = []
    if not open_work: concerns.append("not marked open to work")
    if notice > 60:   concerns.append("notice period " + str(int(notice)) + " days")
    if icr < 0.5:     concerns.append("interview completion rate " + str(round(icr*100)) + "%")
    if exp > 8 and rank <= 20: concerns.append("seniority may exceed fresher role scope")

    s1 = "; ".join(parts) + "."
    s2 = ("Concerns: " + ", ".join(concerns) + ".") if concerns          else "Strong engagement and tech background align with JD."
    return s1 + " " + s2

def w_s(r_l, p):
    with open(p,"w",newline="",encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["candidate_id","rank","score","reasoning"])
        for rank,(s,i,c) in enumerate(r_l,start=1):
            w.writerow([i, rank, round(s,6), build_reasoning(c,rank)])

def r_v(p):
    try: subprocess.run(["python", str(cfg.v_s), str(p)])
    except FileNotFoundError: pass

def r_p(o_p, d_w, b_w, r_k, r_p_k):
    p   = dl.p_c_f(cfg.c_j, cfg.c_j_g)
    c   = dl.l_c(p)
    j   = dl.l_j_t(cfg.j_t)
    j_s = e_j_s(j)
    t   = [tb.b_c_t(x) for x in c]
    h   = rt.HybridRetriever(cfg.d_m)
    h.fit(t)
    i_l, h_s = h.retrieve(j, r_k, r_p_k, d_w, b_w)
    p_c  = [c[i] for i in i_l]
    p_hs = h_s[np.array(i_l)]
    r    = rk.r_c(p_c, j_s, cfg.f_w, h_s=p_hs)
    r    = r[:cfg.f_t_k]
    r    = e_m_s(r)
    w_s(r, o_p)
    r_v(o_p)
