# Ghost Skills – Custom Skills for Ghost Protocol

This repository contains custom Python skills used by the **Ghost Protocol** recruitment engine and the **Antigravity** agent framework. Each skill is designed to be loaded on‑demand via the global skills loader.

## 📦 Included Skills

| Skill | Description |
|-------|-------------|
| `job_fetcher` | Fetches open DevOps/SRE jobs from Greenhouse and Lever APIs. Filters by location (Canada) and days since posting. |
| `candidate_matcher` | Matches candidate profiles against a job description using a cost‑effective LLM (DeepSeek). Requires an API key. |
| `triple_signal_detector` | Detects "revolving door", "phantom growth", and "silent layoff" signals from company data. (Placeholder implementation – extend with your data sources.) |
| `outreach_generator` | Generates personalized outreach emails for decision‑makers, based on the detected signal type. |

## 🚀 Quick Start

### 1. Add the skills to your global skills folder

The skills are designed to be used with the Antigravity global skills loader. To make them available:

- Ensure your global skills folder  is set up with the loader stub files.
- The manifest entry for each skill points to this repository’s raw files.

If you haven’t yet set up the global skills folder, follow the instructions in [antigravity-awesome-skills](https://github.com/Bluemacro/antigravity-awesome-skills) or use our maintenance script.

### 2. Set required environment variables

- **For `candidate_matcher`**:  
  `DEEPSEEK_API_KEY` – Get a free key from [platform.deepseek.com](https://platform.deepseek.com).  
  Optionally, `DEEPSEEK_BASE_URL` if you use a different endpoint.

- **For `job_fetcher`**:  
  No environment variables are required (public APIs are used).  

- **For `triple_signal_detector`**:  
  Placeholder; extend with your own data sources.

- **For `outreach_generator`**:  
  No environment variables required.

### 3. Use the skills in Antigravity or Python

**In Antigravity:**  
Just say “Use @job_fetcher to find DevOps jobs in Canada” – the skill will be automatically loaded.

**In Python:**  
```python
import sys

import job_fetcher

jobs = job_fetcher.fetch_jobs()
print(jobs)
🛠️ Dependencies
Each skill lists its dependencies in the manifest (and in its own code). The loader will install them automatically the first time the skill is used.

Skill	Dependencies
job_fetcher	requests
candidate_matcher	requests
triple_signal_detector	(none)
outreach_generator	(none)

📄 License
All code in this repository is licensed under the MIT License. See the LICENSE file for details.

🤝 Contributing
Feel free to open issues or pull requests for improvements. If you add new skills, please update the README and manifest accordingly.

📬 Contact
For questions about Ghost Protocol or these skills, reach out 
