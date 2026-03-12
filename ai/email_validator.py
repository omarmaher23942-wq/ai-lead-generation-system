import requests
import os
from dotenv import load_dotenv

load_dotenv()

def validate_email_with_ai(email: str, business_name: str, website: str) -> dict:
    if email == "N/A":
        return {"valid": False, "reason": "No email found"}

    prompt = f"""
You are an email validation expert.

Analyze this email and decide if it's a real business email or fake/placeholder.

Business Name: {business_name}
Website: {website}
Email found: {email}

Rules:
- If email looks like a placeholder (user@domain.com, test@test.com) → INVALID
- If email domain doesn't match the business website → INVALID
- If email looks real and belongs to the business → VALID

Respond in this exact format:
VALID or INVALID
REASON: (one short sentence)
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

    result = response.json()["choices"][0]["message"]["content"]
    
    is_valid = result.startswith("VALID")
    reason = result.split("REASON:")[-1].strip() if "REASON:" in result else ""

    return {
        "valid": is_valid,
        "email": email if is_valid else "N/A",
        "reason": reason
    }


if __name__ == "__main__":
    test_cases = [
        {"name": "Bushniwa", "website": "https://bushniwa.com", "email": "info@bushniwa.com"},
        {"name": "Eyval", "website": "https://www.eyvalnyc.com", "email": "user@domain.com"},
        {"name": "Vanka Cafe", "website": "https://vankacafe.com", "email": "contact@sansoxygen.com"},
    ]

    for t in test_cases:
        result = validate_email_with_ai(t["email"], t["name"], t["website"])
        status = "✅" if result["valid"] else "❌"
        print(f"{status} {t['name']} → {t['email']}")
        print(f"   Reason: {result['reason']}\n")