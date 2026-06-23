def s_o_s(c, j_s):
    c_s = set(
        s.get("name", "").lower().strip()
        for s in c.get("skills", [])
        if isinstance(s, dict)
    )
    # also check skill_assessment_scores keys
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

def r_s_score(c):
    """Score using redrob_signals engagement and quality metrics."""
    sig = c.get("redrob_signals", {})
    score = 0.0

    # profile quality
    score += min(sig.get("profile_completeness_score", 0) / 100.0, 1.0) * 0.20

    # active and responsive
    score += (1.0 if sig.get("open_to_work_flag", False) else 0.0) * 0.10
    score += min(sig.get("interview_completion_rate", 0), 1.0) * 0.15
    score += min(sig.get("offer_acceptance_rate", 0), 1.0) * 0.10

    # responsiveness — lower avg_response_time is better
    rt = sig.get("avg_response_time_hours", 999)
    score += max(0.0, 1.0 - (rt / 200.0)) * 0.10

    # github activity
    score += min(sig.get("github_activity_score", 0) / 100.0, 1.0) * 0.15

    # skill assessment avg
    assessments = sig.get("skill_assessment_scores", {})
    if assessments:
        avg = sum(assessments.values()) / len(assessments)
        score += min(avg / 100.0, 1.0) * 0.15

    # recruiter interest signals
    score += min(sig.get("saved_by_recruiters_30d", 0) / 10.0, 1.0) * 0.05

    return min(score, 1.0)

def l_o_p(c):
    t = str(c).lower()
    return 0.7 if ("langchain" in t or "wrapper" in t) and "python" not in t else 1.0

def t_p(c):
    t = str(c).lower()
    return 0.6 if "ai" in t and "machine learning" not in t \
        and "model" not in t and "python" not in t else 1.0