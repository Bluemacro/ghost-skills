"""
Skill: job_fetcher
Fetches open DevOps/SRE jobs from Greenhouse and Lever APIs.
"""
import requests
import json
from datetime import datetime, timedelta

def fetch_jobs(company_list=None, role_keywords=None, location="canada", days_back=30):
    if role_keywords is None:
        role_keywords = ["devops", "site reliability"]
    if company_list is None:
        company_list = {
            "greenhouse": ["shopify", "circleci", "twilio", "stripe", "wealthsimple"],
            "lever": ["lever", "dropbox", "netflix", "instacart", "doordash"]
        }

    cutoff = datetime.now() - timedelta(days=days_back)
    results = []

    for company in company_list.get("greenhouse", []):
        url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for job in data.get("jobs", []):
                    title = job.get("title", "").lower()
                    loc = job.get("location", {}).get("name", "").lower()
                    if any(kw in title for kw in role_keywords) and location.lower() in loc:
                        posted = job.get("updated_at") or job.get("created_at")
                        if posted:
                            posted_date = datetime.fromisoformat(posted.replace("Z", "+00:00"))
                            if posted_date > cutoff:
                                results.append({
                                    "source": "greenhouse",
                                    "company": company,
                                    "title": job["title"],
                                    "location": loc,
                                    "url": job.get("absolute_url"),
                                    "posted": posted
                                })
        except Exception as e:
            print(f"Greenhouse error for {company}: {e}")

    for company in company_list.get("lever", []):
        url = f"https://api.lever.co/v0/postings/{company}"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for job in data:
                    title = job.get("text", "").lower()
                    loc = job.get("categories", {}).get("location", "").lower()
                    if any(kw in title for kw in role_keywords) and location.lower() in loc:
                        created = job.get("createdAt")
                        if created:
                            created_date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                            if created_date > cutoff:
                                results.append({
                                    "source": "lever",
                                    "company": company,
                                    "title": job["text"],
                                    "location": loc,
                                    "url": job.get("hostedUrl"),
                                    "posted": created
                                })
        except Exception as e:
            print(f"Lever error for {company}: {e}")

    return results

def run(**kwargs):
    """Convenience function to be called from Antigravity."""
    return fetch_jobs(**kwargs)

if __name__ == "__main__":
    print(json.dumps(fetch_jobs(), indent=2))
