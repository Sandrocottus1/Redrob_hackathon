import gzip
import json
from pathlib import Path
from typing import Dict,List

def open_json_auto(path: Path):
    if str(path).endswith(".gz"):
        return gzip.open(path,"rt",encoding="utf-8")
    return open(path,"r",encoding="utf-8")

def load_candidates(candidates_path: Path)->List[Dict]:
    candidates: List[Dict] = []
    with open_json_auto(candidates_path) as handle:
        for line in handle:
            text = line.strip()
            if not text:
                continue
            candidates.append(json.loads(text))
    return candidates

def load_jd_text(jd_path: Path) -> str:
    return jd_path.read_text(encoding="utf-8").strip()


def pick_candidates_file(jsonl_path: Path, jsonl_gz_path: Path) -> Path:
    if jsonl_path.exists():
        return jsonl_path
    if jsonl_gz_path.exists():
        return jsonl_gz_path
    raise FileNotFoundError(
        f"Neither candidates file exists: {jsonl_path} or {jsonl_gz_path}"
    )