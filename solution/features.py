import numpy as np
from typing import Optional
from datetime import datetime, date

def _days_since(date_str: str) -> float:
    """Days since a date string like '2026-05-20'."""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (date.today() - d).days
    except:
        return 999

def e_f_s(c) -> float:
    y = c.get("profile", {}).get("years_of_experience", 0)
    try: y = float(y)
    except: y = 0.0
    return min((y / 6.0) ** 0.85, 1.0)

def n_p_s(c) -> float:
    """Signal 12: notice_period_days — lower is better."""
    n = c.get("redrob_signals", {}).get("notice_period_days", 30)
    try: n = float(n)
    except: n = 30.0
    return max(0.0, 1.0 - (n / 90.0))

def semantic_match(h_score: Optional[float]) -> float:
    if h_score is None: return 0.0
    return float(np.clip(h_score, 0.0, 1.0))

def assessment_score(c) -> float:
    """Signal 9: skill_assessment_scores — weighted by tech relevance."""
    sig = c.get("redrob_signals", {})
    assessments = sig.get("skill_assessment_scores", {})
    if not assessments: return 0.0
    tech_kw = ["python", "nlp", "ml", "llm", "sql", "java",
               "classification", "fine-tuning", "deep learning",
               "speech", "backend", "api", "docker", "react"]
    weighted, total_w = 0.0, 0.0
    for skill, score in assessments.items():
        w = 2.0 if any(k in skill.lower() for k in tech_kw) else 1.0
        weighted += score * w
        total_w  += w * 100.0
    return weighted / total_w if total_w else 0.0

def github_talent(c) -> float:
    """Signal 16: github_activity_score. -1 means no GitHub linked."""
    sig = c.get("redrob_signals", {})
    g = sig.get("github_activity_score", -1)
    if g == -1: return 0.1  # penalize slightly for no GitHub
    return min(g / 100.0, 1.0)

def availability_score(c) -> float:
    """
    Signals 4, 12, 14, 15 combined.
    open_to_work, notice_period, preferred_work_mode, willing_to_relocate
    """
    sig = c.get("redrob_signals", {})
    score = 0.0

    # Signal 4: open_to_work_flag
    score += 0.40 if sig.get("open_to_work_flag", False) else 0.0

    # Signal 12: notice period
    notice = float(sig.get("notice_period_days", 90))
    score += max(0.0, 1.0 - notice / 90.0) * 0.30

    # Signal 14: preferred_work_mode
    mode = sig.get("preferred_work_mode", "").lower()
    mode_score = {"remote": 1.0, "flexible": 0.9, "hybrid": 0.7, "onsite": 0.5}.get(mode, 0.5)
    score += mode_score * 0.15

    # Signal 15: willing_to_relocate
    score += 0.15 if sig.get("willing_to_relocate", False) else 0.05

    return min(score, 1.0)

def recency_score(c) -> float:
    """
    Signals 2, 3: signup_date, last_active_date.
    Recent activity = candidate is actually reachable.
    """
    sig = c.get("redrob_signals", {})

    # Signal 3: last_active_date — most important
    days_active = _days_since(sig.get("last_active_date", "2020-01-01"))
    if days_active <= 7:    active = 1.0
    elif days_active <= 30: active = 0.8
    elif days_active <= 90: active = 0.5
    elif days_active <= 180: active = 0.3
    else:                   active = 0.1

    # Signal 2: signup_date — longer tenure on platform = more serious
    days_signed = _days_since(sig.get("signup_date", "2025-01-01"))
    tenure = min(days_signed / 365.0, 1.0)  # up to 1 year = full score

    return active * 0.75 + tenure * 0.25

def engagement_quality(c) -> float:
    """
    Signals 7, 8, 19, 20: recruiter_response_rate, avg_response_time,
    interview_completion_rate, offer_acceptance_rate.
    """
    sig = c.get("redrob_signals", {})

    icr = sig.get("interview_completion_rate", 0)
    oar = sig.get("offer_acceptance_rate", -1)
    rr  = sig.get("recruiter_response_rate", 0)
    rt  = sig.get("avg_response_time_hours", 999)

    # Signal 20: offer_acceptance_rate — -1 means no prior offers
    oar_score = oar if oar >= 0 else 0.5  # neutral if no history

    responsiveness = max(0.0, 1.0 - (rt / 200.0))

    return (icr * 0.35 + oar_score * 0.25 + rr * 0.25 + responsiveness * 0.15)

def market_validation(c) -> float:
    """
    Signals 5, 6, 10, 11, 17, 18: external validation signals.
    profile_views, applications_submitted, connections,
    endorsements, search_appearance, saved_by_recruiters.
    """
    sig = c.get("redrob_signals", {})

    # Signal 5: profile_views_received_30d
    views = min(sig.get("profile_views_received_30d", 0) / 50.0, 1.0)

    # Signal 6: applications_submitted_30d — active job seeker
    apps = min(sig.get("applications_submitted_30d", 0) / 10.0, 1.0)

    # Signal 10: connection_count — network strength
    conns = min(sig.get("connection_count", 0) / 500.0, 1.0)

    # Signal 11: endorsements_received
    endorse = min(sig.get("endorsements_received", 0) / 50.0, 1.0)

    # Signal 17: search_appearance_30d — recruiter interest
    search = min(sig.get("search_appearance_30d", 0) / 200.0, 1.0)

    # Signal 18: saved_by_recruiters_30d — strongest external signal
    saved = min(sig.get("saved_by_recruiters_30d", 0) / 10.0, 1.0)

    return (saved * 0.30 + search * 0.20 + views * 0.15 +
            conns * 0.15 + endorse * 0.12 + apps * 0.08)

def verified_signals(c) -> float:
    """
    Signals 1, 13, 21, 22, 23: profile completeness, salary fit,
    verified email/phone, linkedin connected.
    """
    sig = c.get("redrob_signals", {})
    score = 0.0

    # Signal 1: profile_completeness_score
    score += min(sig.get("profile_completeness_score", 0) / 100.0, 1.0) * 0.25

    # Signal 21: verified_email
    score += 0.20 if sig.get("verified_email", False) else 0.0

    # Signal 22: verified_phone
    score += 0.20 if sig.get("verified_phone", False) else 0.0

    # Signal 23: linkedin_connected
    score += 0.20 if sig.get("linkedin_connected", False) else 0.0

    # Signal 13: expected_salary_range — check if reasonable for fresher role
    sal = sig.get("expected_salary_range_inr_lpa", {})
    sal_min = sal.get("min", 0) if isinstance(sal, dict) else 0
    # JD is fresher role — salary expectation 5-25 LPA is reasonable
    if 5 <= sal_min <= 25:
        score += 0.15
    elif sal_min <= 35:
        score += 0.08
    else:
        score += 0.0  # too high for fresher role

    return min(score, 1.0)

def career_progression(c) -> float:
    """Career history analysis — tech role ratio."""
    career = c.get("career_history", [])
    if not career: return 0.0
    tech_roles = ["engineer", "developer", "scientist", "analyst",
                  "architect", "programmer", "sde", "backend",
                  "data", "ml", "ai", "nlp", "devops", "cloud", "frontend"]
    tech_count = sum(1 for r in career
                     if any(t in r.get("title", "").lower() for t in tech_roles))
    return min(tech_count / len(career) * 1.2, 1.0)

def title_relevance(c) -> float:
    title = c.get("profile", {}).get("current_title", "").lower()
    exp   = float(c.get("profile", {}).get("years_of_experience", 0) or 0)
    
    relevant   = ["backend", "software", "developer", "engineer", "python",
                  "fullstack", "sde", "programmer", "data", "ml", "ai",
                  "machine learning", "nlp", "devops", "cloud", "frontend", 
                  "search", "java", "senior"]
    irrelevant = ["operations", "accountant", "graphic", "mechanical", "civil",
                  "sales", "customer support", "hr", "recruiter", "designer",
                  "manager", "business analyst", "finance", "marketing",
                  "legal", "supply chain", "logistics", "project manager"]

    score = 1.0
    if any(w in title for w in relevant):
        score *= 1.3
    if any(w in title for w in irrelevant):
        score *= 0.05  # changed from 0.15 to 0.05 — much harder penalty
    if exp > 5:
        score *= max(0.2, 1.0 - (exp - 5) / 15.0)
    return min(score, 1.0)

def honeypot_penalty(c) -> float:
    profile = c.get("profile", {})
    career  = c.get("career_history", [])
    skills  = c.get("skills", [])
    exp     = float(profile.get("years_of_experience", 0) or 0)
    sig     = c.get("redrob_signals", {})

    # Too many skills for experience level
    if len(skills) > 30 and exp < 2:
        return 0.1

    # Experience timeline inconsistency
    total_months = sum(r.get("duration_months", 0) for r in career)
    if exp > 3 and total_months > 0 and total_months < exp * 12 * 0.3:
        return 0.2

    # Ghost profile — perfect completeness, zero recruiter response
    completeness  = sig.get("profile_completeness_score", 0)
    response_rate = sig.get("recruiter_response_rate", 0)
    if completeness > 95 and response_rate < 0.05:
        return 0.3

    # Signal 3: hasn't been active in over a year — likely inactive
    days_active = _days_since(sig.get("last_active_date", "2020-01-01"))
    if days_active > 365:
        return 0.4

    return 1.0

def l_o_p(c):
    t = str(c).lower()
    return 0.7 if ("langchain" in t or "wrapper" in t) and "python" not in t else 1.0

def t_p(c):
    t = str(c).lower()
    return 0.6 if "ai" in t and "machine learning" not in t \
        and "model" not in t and "python" not in t else 1.0