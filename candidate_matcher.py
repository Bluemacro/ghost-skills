"""
Skill: candidate_matcher
Matches candidates to job descriptions using DeepSeek API.
Cost-effective and high-quality.
"""
import os
import json
import requests
from typing import List, Dict, Any

# Configuration
DEFAULT_MODEL = "deepseek-chat"  # DeepSeek V3.2
DEFAULT_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEFAULT_BASE_URL = "https://api.deepseek.com"

def match_candidates(candidates: List[Dict[str, Any]], job_description: str,
                     model: str = DEFAULT_MODEL,
                     api_key: str = DEFAULT_API_KEY,
                     base_url: str = DEFAULT_BASE_URL) -> List[Dict[str, Any]]:
    
    if not api_key:
        raise ValueError("No DEEPSEEK_API_KEY set. Get one at platform.deepseek.com")
    
    # Build prompt
    candidates_text = "\n".join([
        f"Candidate {i+1}: {c.get('name', 'Unknown')}\n"
        f"Skills: {', '.join(c.get('skills', []))}\n"
        f"Experience: {c.get('experience', 'N/A')}\n"
        f"Availability: {c.get('availability', 'N/A')}\n"
        for i, c in enumerate(candidates)
    ])
    
    prompt = f"""You are an expert technical recruiter. Given the job description and candidates below, rank the candidates by suitability.

Job description:
{job_description}

Candidates:
{candidates_text}

Return ONLY a JSON array with objects containing:
- candidate_index: number (1-based)
- score: number between 0 and 1
- reason: brief explanation of match

Example: [{{"candidate_index": 2, "score": 0.85, "reason": "Strong AWS and Kubernetes match"}}]
"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 1000
    }
    
    url = f"{base_url.rstrip('/')}/chat/completions"
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    
    content = data["choices"][0]["message"]["content"]
    
    # Parse JSON response
    try:
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        matches = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: return all candidates with equal score
        matches = [{"candidate_index": i+1, "score": 0.5, "reason": "Unable to parse match"} 
                   for i in range(len(candidates))]
    
    # Merge with candidate data
    for m in matches:
        idx = m.get("candidate_index", 0) - 1
        if 0 <= idx < len(candidates):
            m["candidate"] = candidates[idx]
    
    return matches

def run(candidates: List[Dict] = None, job_description: str = "", **kwargs) -> List[Dict]:
    return match_candidates(candidates or [], job_description, **kwargs)

if __name__ == "__main__":
    sample_candidates = [
        {"name": "Alice Chen", "skills": ["AWS", "Kubernetes", "Terraform"], "experience": "6 years", "availability": "Immediate"},
        {"name": "Bob Smith", "skills": ["Azure", "Docker", "CI/CD"], "experience": "4 years", "availability": "2 weeks"}
    ]
    sample_jd = "Looking for a Senior DevOps Engineer with AWS and Kubernetes expertise."
    result = match_candidates(sample_candidates, sample_jd)
    print(json.dumps(result, indent=2))
