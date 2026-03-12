import requests
import os
from dotenv import load_dotenv

load_dotenv()

def write_cold_email(name: str, position: str, company: str, company_description: str) -> str:
    
    prompt = f"""
You are an expert cold email copywriter.

Write a short, personalized cold email offering digital marketing services.

Person Info:
- Name: {name}
- Position: {position}
- Company: {company}
- Company Description: {company_description}

Rules:
- Make it personal based on their position
- If position is sales related → focus on getting more leads
- If position is SEO related → focus on improving rankings
- If position is founder/CEO → focus on business growth
- Maximum 5 lines
- Friendly and professional tone
- End with a simple question to start a conversation
- No fake statistics
- Sign as: Alex - Digital Growth Specialist

Return ONLY the email body, nothing else.
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    email_body = response.json()["choices"][0]["message"]["content"]
    return email_body


if __name__ == "__main__":
    # نجرب على 3 أشخاص مختلفين
    test_people = [
        {
            "name": "Jane Carlson",
            "position": "Sales Manager",
            "company": "WebFX",
            "company_description": "WebFX is a digital marketing agency specializing in SEO, PPC, and web design."
        },
        {
            "name": "Mai Nguyen",
            "position": "SEO Strategist",
            "company": "Disruptive Advertising",
            "company_description": "Disruptive Advertising is a performance marketing agency focused on paid ads and analytics."
        },
        {
            "name": "Matthew Goulart",
            "position": "Founder",
            "company": "Ignite Digital",
            "company_description": "Ignite Digital is a full-service digital marketing agency helping businesses grow online."
        }
    ]

    for person in test_people:
        print(f"\n{'='*50}")
        print(f"📧 Email to: {person['name']} | {person['position']} | {person['company']}")
        print(f"{'='*50}")
        email = write_cold_email(
            person["name"],
            person["position"],
            person["company"],
            person["company_description"]
        )
        print(email)