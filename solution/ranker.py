from . import features as f

def r_c(c_l, j_s, f_w, h_s=None):
    r = []
    for idx, c in enumerate(c_l):
        s = 0.0
        s += f_w.get("skl", 0) * f.s_o_s(c, j_s)
        s += f_w.get("prd", 0) * f.p_f_s(c)
        s += f_w.get("exp", 0) * f.e_f_s(c)
        s += f_w.get("beh", 0) * f.b_s(c)
        s += f_w.get("loc", 0) * f.l_f_s(c)
        s += f_w.get("not", 0) * f.n_p_s(c)
        s += f_w.get("sem", 0) * f.semantic_match(h_s[idx] if h_s is not None else None)
        s += f_w.get("ass", 0) * f.assessment_score(c)
        s += f_w.get("git", 0) * f.github_talent(c)
        s += f_w.get("eng", 0) * f.engagement_quality(c)
        s *= f.l_o_p(c)
        s *= f.t_p(c)
        s *= f.title_relevance(c)
        r.append((s, c.get("candidate_id", ""), c))
    r.sort(key=lambda x: (-x[0], x[1]))
    return r