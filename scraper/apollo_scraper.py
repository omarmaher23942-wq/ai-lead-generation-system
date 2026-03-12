import requests
import os
from dotenv import load_dotenv

load_dotenv()

def find_emails_by_domain(domain: str, company_name: str):
    url = "https://api.hunter.io/v2/domain-search"
    
    params = {
        "domain": domain,
        "api_key": os.getenv("HUNTER_API_KEY"),
        "limit": 5
    }
    
    response = requests.get(url, params=params)
    result = response.json()
    
    emails = []
    
    for email_data in result.get("data", {}).get("emails", []):
        lead = {
            "email": email_data.get("value"),
            "first_name": email_data.get("first_name"),
            "last_name": email_data.get("last_name"),
            "position": email_data.get("position"),
            "company": company_name
        }
        emails.append(lead)
        print(f"✅ {lead['first_name']} {lead['last_name']} | {lead['position']} | {lead['email']}")
    
    print(f"\n🎯 Total emails found: {len(emails)}")
    return emails


if __name__ == "__main__":
    # نجرب على شركات تسويق حقيقية
    companies = [
        {"name": "WebFX", "domain": "webfx.com"},
        {"name": "Disruptive Advertising", "domain": "disruptiveadvertising.com"},
        {"name": "Ignite Digital", "domain": "ignitedigital.com"},
    ]
    
    for company in companies:
        print(f"\n🔍 Searching: {company['name']}")
        find_emails_by_domain(company["domain"], company["name"])