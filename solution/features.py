def s_o_s(c, j_s):
    c_s = set([str(x).lower() for x in c.get("skills", [])])
    if not j_s:
        return 0.0
    return (len(c_s & j_s) / len(j_s)) ** 0.4

def p_f_s(c):
    t = str(c).lower()
    w = ["production", "scale", "deployed", "architecture", "lead", "optimize"]
    return min(sum(1 for x in w if x in t) / 2.0, 1.0)

def e_f_s(c):
    y = c.get("years_experience", 0)
    return min((y / 6.0) ** 0.85, 1.0)

def b_s(c):
    t = str(c).lower()
    w = ["team", "mentored", "collaborated", "agile", "delivered", "cross-functional"]
    return min(sum(1 for x in w if x in t) / 2.0, 1.0)

def l_f_s(c, r="Remote"):
    return 1.0 if str(c.get("location", "")).lower() == r.lower() else 0.0

def n_p_s(c):
    n = c.get("notice_period", 90)
    return max(0.0, 1.0 - (n / 90.0))

def l_o_p(c):
    t = str(c).lower()
    return 0.2 if ("langchain" in t or "wrapper" in t) and "python" not in t else 1.0

def t_p(c):
    t = str(c).lower()
    return 0.1 if "ai" in t and "machine learning" not in t and "model" not in t else 1.0