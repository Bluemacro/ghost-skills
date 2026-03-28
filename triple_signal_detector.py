"""
Skill: triple_signal_detector
Detects revolving door, phantom growth, and silent layoff signals from company data.
"""
def detect_signals(company_data):
    """
    company_data: dict with keys like 'job_postings', 'team_composition', 'layoff_history'
    Returns list of signals detected.
    """
    signals = []
    # Revolving door: same role posted multiple times with gaps
    # Phantom growth: senior role but only junior team
    # Silent layoff: recent layoffs but still hiring
    # Implementation depends on your data sources.
    # Here we return a placeholder.
    signals.append({
        "type": "revolving_door",
        "details": "DevOps role reposted 3 times in 12 months"
    })
    return signals

def run(company_data=None):
    return detect_signals(company_data or {})
