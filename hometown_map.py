import pandas as pd
import requests
import folium
from urllib.parse import quote

# Read CSV file
df = pd.read_csv("hometown_locations - Sheet1.csv")

# Print first 5 rows to confirm it loaded
print(df.head())

# ============================
# 1. ADD YOUR MAPBOX TOKEN
# ============================
access_token = "pk.eyJ1Ijoia2F0ZXN0cmF1Y2giLCJhIjoiY21tOXpodTFqMDA4YzJvb3BsOG1rYjgzOCJ9.hMv3BPPOCzejkbFdNUaqcA"

# ============================
# 2. ADD YOUR MAPBOX STYLE INFO
# ============================
username = "katestrauch"
style_id = "cmm86a95z000c01qr18i03nmc"

tiles = f"https://api.mapbox.com/styles/v1/{username}/{style_id}/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={access_token}"

# ============================
# 3. READ YOUR CSV FILE
# ============================
df = pd.read_csv("hometown_locations.csv")

# ============================
# 4. CREATE BASE MAP
# ============================
m = folium.Map(
    location=[37.7749, -122.4194],  # Centered on San Francisco
    zoom_start=12,
    tiles=tiles,
    attr="Mapbox"
)

# ============================
# 5. FUNCTION TO GEOCODE
# ============================
def geocode_address(address):
    encoded_address = quote(address)
    geocode_url = f"https://api.mapbox.com/search/geocode/v6/forward?q={encoded_address}&access_token={access_token}"
    
    response = requests.get(geocode_url)
    data = response.json()
    
    if data["features"]:
        lon, lat = data["features"][0]["geometry"]["coordinates"]
        return lat, lon
    else:
        return None, None

# ============================
# 6. COLOR BY LOCATION TYPE
# ============================
color_dict = {
    "Restaurant": "red",
    "Park": "green",
    "Cultural": "purple",
    "Historical": "orange",
    "Recreation": "blue",
    "Shopping": "cadetblue",
    "School": "darkred"
}

# ============================
# 7. ADD MARKERS
# ============================
for index, row in df.iterrows():
    lat, lon = geocode_address(row["Address"])
    
    if lat and lon:
        color = color_dict.get(row["Type"], "gray")
        
        popup_html = f"""
        <h4>{row['Name']}</h4>
        <p>{row['Description']}</p>
        <img src="{row['Image_URL']}" width="200">
        """
        
        popup = folium.Popup(popup_html, max_width=300)
        
        folium.Marker(
            location=[lat, lon],
            popup=popup,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

# ============================
# 8. SAVE MAP
# ============================
m.save("hometown_map.html")

print("Map saved as hometown_map.html")