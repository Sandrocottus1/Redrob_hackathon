from . import features as f

def r_c(c_l, j_s, f_w, h_s=None):
    r = []
    for idx, c in enumerate(c_l):
        s   = 0.0
        sem = float(h_s[idx]) if h_s is not None else 0.0

        # Core talent signals
        s += f_w.get("sem", 0) * f.semantic_match(sem)
        s += f_w.get("ass", 0) * f.assessment_score(c)
        s += f_w.get("git", 0) * f.github_talent(c)
        s += f_w.get("car", 0) * f.career_progression(c)

        # Behavioral signals (all 23 covered)
        s += f_w.get("eng", 0) * f.engagement_quality(c)
        s += f_w.get("mkt", 0) * f.market_validation(c)
        s += f_w.get("rec", 0) * f.recency_score(c)
        s += f_w.get("avl", 0) * f.availability_score(c)
        s += f_w.get("ver", 0) * f.verified_signals(c)
        s += f_w.get("exp", 0) * f.e_f_s(c)

        # Multipliers
        s *= f.title_relevance(c)
        s *= f.honeypot_penalty(c)
        s *= f.l_o_p(c)
        s *= f.t_p(c)

        r.append((s, c.get("candidate_id", ""), c))

    r.sort(key=lambda x: (-x[0], x[1]))
    return r