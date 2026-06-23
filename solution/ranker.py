from . import features as f

def r_c(c_l, j_s, f_w):
    r = []
    for c in c_l:
        s = 0.0
        s += f_w.get("skl", 0) * f.s_o_s(c, j_s)
        s += f_w.get("prd", 0) * f.p_f_s(c)
        s += f_w.get("exp", 0) * f.e_f_s(c)
        s += f_w.get("beh", 0) * f.b_s(c)
        s += f_w.get("loc", 0) * f.l_f_s(c)
        s += f_w.get("not", 0) * f.n_p_s(c)
        s+=f_w.get("sig",0)*f.r_s_score(c)
        s *= f.l_o_p(c)
        s *= f.t_p(c)
        r.append((s, c.get("candidate_id", ""), c))
    r.sort(key=lambda x: (-x[0], x[1]))
    return r