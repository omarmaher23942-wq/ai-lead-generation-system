from scraper.website_scraper import scrape_businesses
from scraper.apollo_scraper import find_emails_by_domain
from ai.ai_scraper import ai_scrape_website
from ai.email_writer import write_cold_email
from database.db import init_db, save_lead, get_all_leads

MARKETING_AGENCIES = [
    {"name": "WebFX", "domain": "webfx.com", "website": "https://www.webfx.com"},
    {"name": "Disruptive Advertising", "domain": "disruptiveadvertising.com", "website": "https://disruptiveadvertising.com"},
    {"name": "Ignite Digital", "domain": "ignitedigital.com", "website": "https://ignitedigital.com"},
    {"name": "Thrive Agency", "domain": "thriveagency.com", "website": "https://thriveagency.com"},
    {"name": "Straight North", "domain": "straightnorth.com", "website": "https://www.straightnorth.com"},
]

def main():
    init_db()
    print("✅ Database ready\n")

    for company in MARKETING_AGENCIES:
        print(f"\n{'='*50}")
        print(f"🔍 Processing: {company['name']}")
        print(f"{'='*50}")

        print("🤖 Analyzing website...")
        company_data = ai_scrape_website(company["website"], company["name"])
        description = company_data.get("description", "A digital marketing agency")

        print("📧 Finding emails...")
        contacts = find_emails_by_domain(company["domain"], company["name"])

        if not contacts:
            print("⏭️ No contacts found, skipping...")
            continue

        for contact in contacts[:3]:
            if not contact["email"] or not contact["first_name"]:
                continue

            full_name = f"{contact['first_name']} {contact['last_name'] or ''}".strip()
            position = contact["position"] or "Team Member"

            print(f"\n✍️ Writing email for: {full_name} | {position}")

            email_body = write_cold_email(
                name=full_name,
                position=position,
                company=company["name"],
                company_description=description
            )

            print(f"\n📧 Email Preview:")
            print(f"{'-'*40}")
            print(email_body)
            print(f"{'-'*40}")

            save_lead(
                name=full_name,
                email=contact["email"],
                phone=company_data.get("phone", "N/A"),
                website=company["website"],
                description=f"{position} at {company['name']} - {description}"
            )

    print(f"\n{'='*50}")
    print(f"🎯 FINAL RESULTS")
    print(f"{'='*50}")

    leads = get_all_leads()
    print(f"\n✅ Total leads collected: {len(leads)}")
    for lead in leads:
        print(f"👤 {lead[1]} | {lead[2]}")

if __name__ == "__main__":
    main()