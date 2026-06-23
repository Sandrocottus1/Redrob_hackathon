import numpy as np
from typing import Optional

def s_o_s(c, j_s):
    c_s = set(
        s.get("name", "").lower().strip()
        for s in c.get("skills", [])
        if isinstance(s, dict)
    )
    sig = c.get("redrob_signals", {})
    assessed = set(k.lower() for k in sig.get("skill_assessment_scores", {}).keys())
    c_s = c_s | assessed
    if not j_s:
        return 0.0
    return (len(c_s & j_s) / len(j_s)) ** 0.4

def p_f_s(c):
    t = str(c).lower()
    w = ["production", "scale", "deployed", "architecture", "lead", "optimized", "built", "designed"]
    return min(sum(1 for x in w if x in t) / 3.0, 1.0)

def e_f_s(c):
    y = c.get("profile", {}).get("years_of_experience", 0)
    try:
        y = float(y)
    except (TypeError, ValueError):
        y = 0.0
    return min((y / 6.0) ** 0.85, 1.0)

def b_s(c):
    t = str(c).lower()
    w = ["team", "mentored", "collaborated", "agile", "delivered", "cross-functional", "sprint", "communicated"]
    return min(sum(1 for x in w if x in t) / 3.0, 1.0)

def l_f_s(c):
    profile = c.get("profile", {})
    sig = c.get("redrob_signals", {})
    loc = str(profile.get("location", "")).lower()
    country = str(profile.get("country", "")).lower()
    work_mode = str(sig.get("preferred_work_mode", "")).lower()
    willing = sig.get("willing_to_relocate", False)
    if "remote" in work_mode:
        return 1.0
    if "india" in country or "india" in loc:
        return 1.0 if willing else 0.7
    return 0.3

def n_p_s(c):
    n = c.get("redrob_signals", {}).get("notice_period_days", 30)
    try:
        n = float(n)
    except (TypeError, ValueError):
        n = 30.0
    return max(0.0, 1.0 - (n / 90.0))

def semantic_match(h_score: Optional[float]) -> float:
    """Semantic similarity to JD via embeddings — pure talent/fit signal."""
    if h_score is None:
        return 0.0
    return float(np.clip(h_score, 0.0, 1.0))

def assessment_score(c) -> float:
    """Actual test scores from redrob_signals — most objective talent signal."""
    sig = c.get("redrob_signals", {})
    assessments = sig.get("skill_assessment_scores", {})
    if not assessments:
        return 0.0
    tech_keywords = ["python", "nlp", "ml", "llm", "sql", "java",
                     "classification", "fine-tuning", "deep learning", "speech"]
    weighted, total_w = 0.0, 0.0
    for skill, score in assessments.items():
        w = 2.0 if any(k in skill.lower() for k in tech_keywords) else 1.0
        weighted += score * w
        total_w += w * 100.0
    return weighted / total_w if total_w else 0.0

def github_talent(c) -> float:
    """GitHub activity as proxy for actual coding ability."""
    sig = c.get("redrob_signals", {})
    return min(sig.get("github_activity_score", 0) / 100.0, 1.0)

def engagement_quality(c) -> float:
    """Candidate seriousness — completes interviews, accepts offers, responds fast."""
    sig = c.get("redrob_signals", {})
    icr = sig.get("interview_completion_rate", 0)
    oar = sig.get("offer_acceptance_rate", 0)
    rr = sig.get("recruiter_response_rate", 0)
    rt = sig.get("avg_response_time_hours", 999)
    responsiveness = max(0.0, 1.0 - (rt / 200.0))
    return (icr * 0.4 + oar * 0.3 + rr * 0.2 + responsiveness * 0.1)

def l_o_p(c):
    t = str(c).lower()
    return 0.7 if ("langchain" in t or "wrapper" in t) and "python" not in t else 1.0

def t_p(c):
    t = str(c).lower()
    return 0.6 if "ai" in t and "machine learning" not in t \
        and "model" not in t and "python" not in t else 1.0

def title_relevance(c):
    title = c.get("profile", {}).get("current_title", "").lower()
    exp = c.get("profile", {}).get("years_of_experience", 0) or 0
    relevant = ["backend", "software", "developer", "engineer", "python",
                "fullstack", "sde", "programmer", "data"]
    irrelevant = ["operations", "accountant", "graphic", "mechanical",
                  "business analyst", "manager", "designer", "hr"]
    score = 1.0
    if any(w in title for w in relevant):
        score *= 1.2
    if any(w in title for w in irrelevant):
        score *= 0.4
    if exp > 3:
        score *= max(0.3, 1.0 - (exp - 3) / 20.0)
    return min(score, 1.0)