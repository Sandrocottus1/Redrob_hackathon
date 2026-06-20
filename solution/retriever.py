import re
import faiss
import numpy as np
from typing import List, Sequence
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

def _t(t: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9_]+", t.lower())

class HybridRetriever:
    def __init__(self, m_n: str):
        self.m = SentenceTransformer(m_n)
        self.c_e = None
        self.f_i = None
        self.b = None
        
    def fit(self, c_t: Sequence[str]) -> None:
        e = self.m.encode(c_t, convert_to_numpy=True)
        faiss.normalize_L2(e)
        self.c_e = e
        self.f_i = faiss.IndexFlatIP(e.shape[1])
        self.f_i.add(e)
        self.b = BM25Okapi(list(map(_t, c_t)))

    def retrieve(self, j_t: str, r_k: int, r_p_k: int, d_w: float, b_w: float) -> List[int]:
        q = _t(j_t)
        b_s = np.array(self.b.get_scores(q))
        q_e = self.m.encode([j_t], convert_to_numpy=True)
        faiss.normalize_L2(q_e)
        n = len(b_s)
        d_v, d_i = self.f_i.search(q_e, n)
        d_s = np.zeros(n)
        d_s[d_i[0]] = d_v[0]
        f = lambda x: (x - np.min(x)) / (np.ptp(x) + 1e-8)
        h_s = d_w * f(d_s) + b_w * f(b_s)
        return np.argsort(h_s)[::-1][:r_p_k].tolist()