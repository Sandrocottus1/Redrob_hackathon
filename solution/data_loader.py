import gzip
import json
from pathlib import Path
from typing import Dict, List

def o_j_a(p: Path):
    return gzip.open(p, "rt", encoding="utf-8") if str(p).endswith(".gz") else open(p, "r", encoding="utf-8")

def l_c(c_p: Path) -> List[Dict]:
    with o_j_a(c_p) as h:
        return [json.loads(x.strip()) for x in h if x.strip()]

def l_j_t(j_p: Path) -> str:
    return j_p.read_text(encoding="utf-8").strip()

def p_c_f(p1: Path, p2: Path) -> Path:
    if p1.exists(): return p1
    if p2.exists(): return p2
    raise FileNotFoundError(f"Err: {p1}, {p2}")