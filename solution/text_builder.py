from typing import Dict,List

def _skills_text(candidate: Dict, max_items: int = 25)->str:
    skills=candidate.get("skills",[])
    names: List[str]=[]
    for item in skills:
        name=item.get("name","").strip()
        if name:
            names.append(name)
    return ", ".join(names[:max_items])

""" ...to extract career work experience """

def _career_text(candidate: Dict,  max_items: int =5)->str:
    lines: List[str]=[]
    for role in candidate.get("career_history",[])[:max_items]:
        title=role.get("title","")
        company=role.get("company","")
        industry=role.get("industry","")
        duration=role.get("duration_months",0)
        description=role.get("description","")
        lines.append(
            f"{title} at {company}. Industry: {industry}. Duration:{duration} months. {description}"
        )
    return " | ".join(lines)

def _education_text(candidate: Dict , max_items: int=3)->str:
    lines: List[str]=[]
    for edu in candidate.get("education",[])[:max_items]:
        lines.append(
            f"{edu.get('degree', '')} in {edu.get('field_of_study','')} from {edu.get('instruction','')}"
        )
    return " | ".join(lines)

def build_candidate_text(candidate: Dict) -> str:
    profile = candidate.get("profile", {})

    parts = [
        f"Current Title: {profile.get('current_title', '')}",
        f"Industry: {profile.get('current_industry', '')}",
        f"Experience Years: {profile.get('years_of_experience', 0)}",
        f"Headline: {profile.get('headline', '')}",
        f"Summary: {profile.get('summary', '')}",
        f"Skills: {_skills_text(candidate)}",
        f"Career: {_career_text(candidate)}",
        f"Education: {_education_text(candidate)}",
    ]

    return "\n".join(parts)