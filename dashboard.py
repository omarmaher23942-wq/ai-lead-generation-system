from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from database.db import init_db, get_all_leads, save_lead
from scraper.apollo_scraper import find_emails_by_domain
from ai.ai_scraper import ai_scrape_website
from ai.email_writer import write_cold_email
import os

app = FastAPI()

MARKETING_AGENCIES = [
    {"name": "WebFX", "domain": "webfx.com", "website": "https://www.webfx.com"},
    {"name": "Disruptive Advertising", "domain": "disruptiveadvertising.com", "website": "https://disruptiveadvertising.com"},
    {"name": "Ignite Digital", "domain": "ignitedigital.com", "website": "https://ignitedigital.com"},
    {"name": "Thrive Agency", "domain": "thriveagency.com", "website": "https://thriveagency.com"},
    {"name": "Straight North", "domain": "straightnorth.com", "website": "https://www.straightnorth.com"},
]

@app.on_event("startup")
def startup():
    init_db()
    leads = get_all_leads()
    print(f"🔥 Startup: found {len(leads)} leads in DB")
    if not leads:
        print("🌱 Seeding initial data...")
        save_lead("Nolan Barger","nolan@webfx.com","888-601-5359","https://www.webfx.com","Director of Innovation at WebFX")
        save_lead("Jane Carlson","jane@webfx.com","888-601-5359","https://www.webfx.com","Sales Manager at WebFX")
        save_lead("Matthew Goulart","matthew@ignitedigital.com","1-800-831-6998","https://ignitedigital.com","Founder at Ignite Digital")
        save_lead("Aaron Whittaker","aaron@thriveagency.com","866-908-4748","https://thriveagency.com","VP of Marketing at Thrive Agency")
        save_lead("Frank Fornaris","frank@straightnorth.com","N/A","https://www.straightnorth.com","President at Straight North")
        save_lead("Chad De Lisle","chad@disruptiveadvertising.com","N/A","https://disruptiveadvertising.com","VP of Marketing at Disruptive Advertising")
        save_lead("Mai Nguyen","mnguyen@disruptiveadvertising.com","N/A","https://disruptiveadvertising.com","SEO Strategist at Disruptive Advertising")
        save_lead("Brandon George","brandon@thriveagency.com","866-908-4748","https://thriveagency.com","Content Director at Thrive Agency")
        print(f"✅ Seeded {len(get_all_leads())} leads")

@app.get("/", response_class=HTMLResponse)
def index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "static", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/leads")
def get_leads():
    leads = get_all_leads()
    return JSONResponse([{
        "id": l[0],
        "name": l[1],
        "email": l[2],
        "phone": l[3],
        "website": l[4],
        "description": l[5],
        "date": l[6]
    } for l in leads])

@app.post("/run")
def run_system():
    new_leads = []
    for company in MARKETING_AGENCIES:
        try:
            company_data = ai_scrape_website(company["website"], company["name"])
            description = company_data.get("description", "A digital marketing agency")
            contacts = find_emails_by_domain(company["domain"], company["name"])
            if not contacts:
                continue
            for contact in contacts[:3]:
                if not contact["email"] or not contact["first_name"]:
                    continue
                full_name = f"{contact['first_name']} {contact['last_name'] or ''}".strip()
                position = contact["position"] or "Team Member"
                write_cold_email(
                    name=full_name,
                    position=position,
                    company=company["name"],
                    company_description=description
                )
                save_lead(
                    name=full_name,
                    email=contact["email"],
                    phone=company_data.get("phone", "N/A"),
                    website=company["website"],
                    description=f"{position} at {company['name']} - {description}"
                )
                new_leads.append({"name": full_name, "email": contact["email"]})
        except:
            continue
    return JSONResponse({"status": "success", "new_leads": len(new_leads)})