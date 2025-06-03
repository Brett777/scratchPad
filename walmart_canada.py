import requests
import pandas as pd
from geopy.geocoders import Nominatim
from typing import List, Dict, Optional

# Overpass API endpoint
OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def query_walmart_stores(country_code: str = "CA", user_agent: str = "walmart-scraper") -> List[Dict]:
    """Query Overpass API for Walmart stores in the specified country.

    Args:
        country_code: ISO country code (default "CA" for Canada).
        user_agent: User-Agent string for HTTP requests.
    Returns:
        List of Overpass elements representing stores.
    """
    query = f"""
    [out:json][timeout:60];
    area["ISO3166-1"="{country_code}"]->.searchArea;
    (
      node["name"="Walmart"](area.searchArea);
      node["brand"="Walmart"](area.searchArea);
      way["name"="Walmart"](area.searchArea);
      way["brand"="Walmart"](area.searchArea);
    );
    out center tags;
    """

    headers = {"User-Agent": user_agent}
    try:
        resp = requests.post(OVERPASS_URL, data={"data": query}, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data.get("elements", [])
    except Exception as e:
        print(f"Error querying Overpass: {e}")
        return []


def geocode_address(address: str, geolocator: Optional[Nominatim] = None) -> Optional[Dict[str, float]]:
    """Geocode an address using Nominatim if possible."""
    if geolocator is None:
        geolocator = Nominatim(user_agent="walmart-geocoder")
    try:
        location = geolocator.geocode(address)
        if location:
            return {"lat": location.latitude, "lon": location.longitude}
    except Exception as e:
        print(f"Geocoding error for '{address}': {e}")
    return None


def build_store_record(element: Dict) -> Dict:
    tags = element.get("tags", {})
    store_name = tags.get("name") or tags.get("brand")
    store_number = tags.get("ref")
    address_parts = [
        tags.get("addr:street"),
        tags.get("addr:housenumber"),
        tags.get("addr:city"),
        tags.get("addr:province"),
        tags.get("addr:postcode"),
    ]
    address = ", ".join([p for p in address_parts if p])

    lat = element.get("lat") or element.get("center", {}).get("lat")
    lon = element.get("lon") or element.get("center", {}).get("lon")

    if lat is None or lon is None:
        geo = geocode_address(address)
        if geo:
            lat = geo["lat"]
            lon = geo["lon"]

    # Placeholder image URL - replace with real photo if available
    photo_url = tags.get("image") or "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Walmart_logo.svg/320px-Walmart_logo.svg.png"

    return {
        "store_name": store_name,
        "store_number": store_number,
        "address": address,
        "latitude": lat,
        "longitude": lon,
        "photo_url": photo_url,
    }


def fetch_walmart_canada() -> pd.DataFrame:
    elements = query_walmart_stores()
    records = [build_store_record(el) for el in elements]
    df = pd.DataFrame(records)
    return df


def main():
    df = fetch_walmart_canada()
    print(df.head())
    df.to_csv("walmart_canada_stores.csv", index=False)


if __name__ == "__main__":
    main()
