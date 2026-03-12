import requests

def scrape_businesses(query: str, location: str):
    results = []
    
    # Overpass API - مجاني 100%
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    overpass_query = f"""
    [out:json];
    area[name="{location}"]->.searchArea;
    node["amenity"="{query}"](area.searchArea);
    out body;
    """
    
    response = requests.post(overpass_url, data=overpass_query)
    data = response.json()
    
    for element in data["elements"]:
        tags = element.get("tags", {})
        name = tags.get("name")
        
        if name:
            results.append({
                "name": name,
                "phone": tags.get("phone", "N/A"),
                "website": tags.get("website", "N/A"),
                "address": tags.get("addr:street", "N/A")
            })
            print(f"✅ {name} | {tags.get('phone', 'N/A')} | {tags.get('website', 'N/A')}")
    
    print(f"\nإجمالي الشركات: {len(results)}")
    return results


if __name__ == "__main__":
    scrape_businesses("restaurant", "New York")