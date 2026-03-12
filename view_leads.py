from database.db import get_all_leads, init_db

init_db()
leads = get_all_leads()

print(f"\n{'='*60}")
print(f"📊 TOTAL LEADS: {len(leads)}")
print(f"{'='*60}\n")

for lead in leads:
    print(f"🏢 Company  : {lead[1]}")
    print(f"📧 Email    : {lead[2]}")
    print(f"📞 Phone    : {lead[3]}")
    print(f"🌐 Website  : {lead[4]}")
    print(f"📝 About    : {lead[5]}")
    print(f"🕐 Saved at : {lead[6]}")
    print(f"{'-'*60}")