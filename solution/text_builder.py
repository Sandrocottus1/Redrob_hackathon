from typing import Dict, List

def _s_t(c: Dict, m: int = 25) -> str:
    return ", ".join([i.get("name", "").strip() for i in c.get("skills", []) if i.get("name", "").strip()][:m])

def _c_t(c: Dict, m: int = 5) -> str:
    return " | ".join([
        f"{r.get('title', '')} at {r.get('company', '')}. Industry: {r.get('industry', '')}. Duration:{r.get('duration_months', 0)} months. {r.get('description', '')}"
        for r in c.get("career_history", [])[:m]
    ])

def _e_t(c: Dict, m: int = 3) -> str:
    return " | ".join([
        f"{e.get('degree', '')} in {e.get('field_of_study', '')} from {e.get('institution', '')}"
        for e in c.get("education", [])[:m]
    ])

def b_c_t(c: Dict) -> str:
    p = c.get("profile", {})
    return "\n".join([
        f"Current Title: {p.get('current_title', '')}",
        f"Industry: {p.get('current_industry', '')}",
        f"Experience Years: {p.get('years_of_experience', 0)}",
        f"Headline: {p.get('headline', '')}",
        f"Summary: {p.get('summary', '')}",
        f"Skills: {_s_t(c)}",
        f"Career: {_c_t(c)}",
        f"Education: {_e_t(c)}"
    ])

build_candidate_text = b_c_t