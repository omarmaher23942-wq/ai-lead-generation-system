from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from database.db import init_db, get_all_leads, save_lead
from scraper.apollo_scraper import find_emails_by_domain
from ai.ai_scraper import ai_scrape_website
from ai.email_writer import write_cold_email
import asyncio

app = FastAPI()

MARKETING_AGENCIES = [
    {"name": "WebFX", "domain": "webfx.com", "website": "https://www.webfx.com"},
    {"name": "Disruptive Advertising", "domain": "disruptiveadvertising.com", "website": "https://disruptiveadvertising.com"},
    {"name": "Ignite Digital", "domain": "ignitedigital.com", "website": "https://ignitedigital.com"},
    {"name": "Thrive Agency", "domain": "thriveagency.com", "website": "https://thriveagency.com"},
    {"name": "Straight North", "domain": "straightnorth.com", "website": "https://www.straightnorth.com"},
]

@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/index.html", "r") as f:
        return f.read()

@app.get("/leads")
def get_leads():
    init_db()
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
    init_db()
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

                email_body = write_cold_email(
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

                new_leads.append({
                    "name": full_name,
                    "email": contact["email"],
                    "position": position,
                    "company": company["name"]
                })
        except:
            continue

    return JSONResponse({
        "status": "success",
        "new_leads": len(new_leads),
        "leads": new_leads
    })