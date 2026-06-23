def s_o_s(c, j_s):
    # skills is a list of dicts with "name" key
    c_s = set(
        s.get("name", "").lower().strip()
        for s in c.get("skills", [])
        if isinstance(s, dict)
    )
    if not j_s:
        return 0.0
    return (len(c_s & j_s) / len(j_s)) ** 0.4

def p_f_s(c):
    t = str(c).lower()
    w = ["production", "scale", "deployed", "architecture", "lead", "optimized", "built", "designed"]
    return min(sum(1 for x in w if x in t) / 3.0, 1.0)

def e_f_s(c):
    # years_of_experience is inside profile
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
    # location is inside profile
    loc = str(c.get("profile", {}).get("location", "")).lower()
    country = str(c.get("profile", {}).get("country", "")).lower()
    if "india" in country or "india" in loc or "remote" in loc or loc == "":
        return 1.0
    return 0.3

def n_p_s(c):
    # check redrob_signals for notice period
    n = c.get("redrob_signals", {}).get("notice_period_days", 30)
    try:
        n = float(n)
    except (TypeError, ValueError):
        n = 30.0
    return max(0.0, 1.0 - (n / 90.0))

def l_o_p(c):
    t = str(c).lower()
    return 0.7 if ("langchain" in t or "wrapper" in t) and "python" not in t else 1.0

def t_p(c):
    t = str(c).lower()
    return 0.6 if "ai" in t and "machine learning" not in t \
        and "model" not in t and "python" not in t else 1.0