"""
Skill: outreach_generator
Generates personalized outreach emails for decision-makers.
"""
def generate_message(company_name, contact_name, signal_type, offer):
    """
    Returns a formatted email message.
    """
    templates = {
        "revolving_door": f"Hi {contact_name}, I noticed your DevOps role keeps reopening. We have a $500 Validation Sprint that delivers 3 pre‑vetted candidates in 48h...",
        "phantom_growth": f"Hi {contact_name}, your team is hiring a senior DevOps lead but I see mostly junior engineers. We can help you fill that leadership gap...",
        "silent_layoff": f"Hi {contact_name}, after recent changes, you're still hiring critical roles. Our $500 Validation Sprint provides immediate, vetted talent..."
    }
    return templates.get(signal_type, f"Hi {contact_name}, we can help with {company_name}'s hiring needs.")

def run(company_name="", contact_name="", signal_type="", offer="$500 Validation Sprint"):
    return generate_message(company_name, contact_name, signal_type, offer)
