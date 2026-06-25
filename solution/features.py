import numpy as np
from typing import Optional

def s_o_s(c, j_s):
    c_s = set(s.get("name","").lower().strip() for s in c.get("skills",[]) if isinstance(s,dict))
    sig = c.get("redrob_signals",{})
    assessed = set(k.lower() for k in sig.get("skill_assessment_scores",{}).keys())
    c_s = c_s | assessed
    if not j_s: return 0.0
    return (len(c_s & j_s) / len(j_s)) ** 0.4

def e_f_s(c):
    y = c.get("profile",{}).get("years_of_experience",0)
    try: y = float(y)
    except: y = 0.0
    return min((y/6.0)**0.85, 1.0)

def n_p_s(c):
    n = c.get("redrob_signals",{}).get("notice_period_days",30)
    try: n = float(n)
    except: n = 30.0
    return max(0.0, 1.0-(n/90.0))

def semantic_match(h_score: Optional[float]) -> float:
    if h_score is None: return 0.0
    return float(np.clip(h_score, 0.0, 1.0))

def assessment_score(c) -> float:
    sig = c.get("redrob_signals",{})
    assessments = sig.get("skill_assessment_scores",{})
    if not assessments: return 0.0
    tech_kw = ["python","nlp","ml","llm","sql","java","classification","fine-tuning","deep learning","speech"]
    weighted, total_w = 0.0, 0.0
    for skill, score in assessments.items():
        w = 2.0 if any(k in skill.lower() for k in tech_kw) else 1.0
        weighted += score * w
        total_w  += w * 100.0
    return weighted/total_w if total_w else 0.0

def github_talent(c) -> float:
    return min(c.get("redrob_signals",{}).get("github_activity_score",0)/100.0, 1.0)

def engagement_quality(c) -> float:
    sig = c.get("redrob_signals",{})
    icr = sig.get("interview_completion_rate",0)
    oar = sig.get("offer_acceptance_rate",0)
    rr  = sig.get("recruiter_response_rate",0)
    rt  = sig.get("avg_response_time_hours",999)
    return icr*0.4 + oar*0.3 + rr*0.2 + max(0.0,1.0-(rt/200.0))*0.1

def career_progression(c) -> float:
    career = c.get("career_history",[])
    if not career: return 0.0
    tech_roles = ["engineer","developer","scientist","analyst","architect",
                  "programmer","sde","backend","data","ml","ai","nlp","devops","cloud","frontend"]
    tech_count = sum(1 for r in career if any(t in r.get("title","").lower() for t in tech_roles))
    return min(tech_count/len(career)*1.2, 1.0)

def verified_signals(c) -> float:
    sig = c.get("redrob_signals",{})
    score = 0.0
    assessments = sig.get("skill_assessment_scores",{})
    if assessments:
        score += (sum(assessments.values())/len(assessments)/100.0)*0.40
    score += min(sig.get("github_activity_score",0)/100.0,1.0)*0.30
    verified = int(sig.get("verified_email",False)) + int(sig.get("verified_phone",False))
    score += (verified/2.0)*0.10
    score += min(sig.get("saved_by_recruiters_30d",0)/5.0,1.0)*0.10
    score += (1.0 if sig.get("linkedin_connected",False) else 0.0)*0.10
    return min(score, 1.0)

def title_relevance(c) -> float:
    title = c.get("profile",{}).get("current_title","").lower()
    exp   = float(c.get("profile",{}).get("years_of_experience",0) or 0)
    relevant   = ["backend","software","developer","engineer","python","fullstack",
                  "sde","programmer","data","ml","ai","machine learning","nlp",
                  "devops","cloud","frontend","search"]
    irrelevant = ["operations","accountant","graphic","mechanical","civil","sales",
                  "customer support","hr","recruiter","designer","manager",
                  "business analyst","finance","marketing","legal","supply chain","logistics"]
    score = 1.0
    if any(w in title for w in relevant):   score *= 1.3
    if any(w in title for w in irrelevant): score *= 0.15
    if exp > 5: score *= max(0.2, 1.0-(exp-5)/15.0)
    return min(score, 1.0)

def honeypot_penalty(c) -> float:
    profile = c.get("profile",{})
    career  = c.get("career_history",[])
    skills  = c.get("skills",[])
    exp     = float(profile.get("years_of_experience",0) or 0)
    sig     = c.get("redrob_signals",{})
    if len(skills) > 30 and exp < 2: return 0.1
    total_months = sum(r.get("duration_months",0) for r in career)
    if exp > 3 and total_months > 0 and total_months < exp*12*0.3: return 0.2
    if sig.get("profile_completeness_score",0) > 95 and sig.get("recruiter_response_rate",0) < 0.05:
        return 0.3
    return 1.0

def l_o_p(c):
    t = str(c).lower()
    return 0.7 if ("langchain" in t or "wrapper" in t) and "python" not in t else 1.0

def t_p(c):
    t = str(c).lower()
    return 0.6 if "ai" in t and "machine learning" not in t and "model" not in t and "python" not in t else 1.0
