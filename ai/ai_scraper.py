import requests
import os
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

def find_contact_page(website: str, soup: BeautifulSoup) -> str:
    """بيدور على لينك صفحة الـ Contact"""
    contact_keywords = ["contact", "about", "reach", "connect", "get-in-touch"]
    
    for link in soup.find_all("a", href=True):
        href = link["href"].lower()
        text = link.text.lower()
        
        if any(kw in href or kw in text for kw in contact_keywords):
            # لو اللينك relative نضيف الـ domain
            if href.startswith("/"):
                base = website.rstrip("/")
                return base + href
            elif href.startswith("http"):
                return href
    
    return None


def scrape_page_text(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    response = requests.get(url, headers=headers, timeout=5)
    soup = BeautifulSoup(response.text, "html.parser")
    
    for tag in soup(["script", "style", "nav"]):
        tag.decompose()
    
    return soup, soup.get_text(separator=" ", strip=True)[:3000]


def ai_scrape_website(website: str, business_name: str) -> dict:
    if website == "N/A" or not website.startswith("http"):
        return {"email": "N/A", "phone": "N/A", "description": "N/A"}

    try:
        # جيب الصفحة الرئيسية
        soup, main_text = scrape_page_text(website)
        
        # دور على صفحة الـ Contact
        contact_url = find_contact_page(website, soup)
        contact_text = ""
        
        if contact_url:
            print(f"   📧 Found contact page: {contact_url}")
            try:
                _, contact_text = scrape_page_text(contact_url)
            except:
                pass
        
        # دمج النصين
        full_text = main_text + " " + contact_text

        prompt = f"""
You are a data extraction expert.

Extract contact information from this website text.

Business Name: {business_name}
Website: {website}
Website Text:
{full_text}

Extract and return ONLY a JSON object like this:
{{
    "email": "found email or N/A",
    "phone": "found phone or N/A",
    "description": "one sentence about what this business does"
}}

Rules:
- Only return real emails that belong to this business
- No placeholder emails like user@domain.com
- Return ONLY the JSON, nothing else
"""

        response_ai = requests.post(
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

        result = response_ai.json()["choices"][0]["message"]["content"]
        result = result.replace("```json", "").replace("```", "").strip()
        
        data = json.loads(result)
        print(f"✅ {business_name} → {data}")
        return data

    except Exception as e:
        print(f"❌ Error with {business_name}: {e}")
        return {"email": "N/A", "phone": "N/A", "description": "N/A"}


if __name__ == "__main__":
    test_businesses = [
        {"name": "Bushniwa", "website": "https://bushniwa.com"},
        {"name": "Tanoreen", "website": "https://tanoreen.com"},
        {"name": "Javitri", "website": "https://www.javitrinyc.com/"},
    ]

    for b in test_businesses:
        ai_scrape_website(b["website"], b["name"])