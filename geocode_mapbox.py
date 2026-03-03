import urllib.parse
import requests
import pandas as pd

INPUT_CSV = "hometown_locations.csv"
OUTPUT_CSV = "hometown_locations_geocoded.csv"
ADDRESS_COLUMN = "Address"

access_token = "pk.eyJ1Ijoia2F0ZXN0cmF1Y2giLCJhIjoiY21tOXpodTFqMDA4YzJvb3BsOG1rYjgzOCJ9.hMv3BPPOCzejkbFdNUaqcA"
if not access_token:
    raise ValueError("Missing token. In terminal run: export MAPBOX_ACCESS_TOKEN=pk_...")

print("Loaded token: YES")
df = pd.read_csv(INPUT_CSV, engine="python")
print("Columns:", list(df.columns))
print("Rows/Cols:", df.shape)

if ADDRESS_COLUMN not in df.columns:
    raise ValueError(f"Missing column: '{ADDRESS_COLUMN}' not found")

def geocode(address: str):
    q = urllib.parse.quote(str(address))
    url = f"https://api.mapbox.com/search/geocode/v6/forward?q={q}&limit=1&country=US&access_token={access_token}"

    r = requests.get(url, timeout=20)
    print("Status:", r.status_code, "for address:", address)

    if r.status_code != 200:
        print("Response (first 200 chars):", r.text[:200])
        return None, None

    data = r.json()
    features = data.get("features", [])
    if not features:
        print("NO MATCH")
        return None, None

    coords = features[0].get("geometry", {}).get("coordinates")
    if not coords or len(coords) < 2:
        return None, None

    lon, lat = coords[0], coords[1]
    return lat, lon

lats, lons = [], []
for addr in df[ADDRESS_COLUMN].tolist():
    lat, lon = geocode(addr)
    lats.append(lat)
    lons.append(lon)

df["latitude"] = lats
df["longitude"] = lons

df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved: {OUTPUT_CSV}")