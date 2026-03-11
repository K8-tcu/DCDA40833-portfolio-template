import pandas as pd
import folium

INPUT_CSV = "hometown_locations_geocoded.csv"
OUTPUT_HTML = "hometown_map.html"

# Mapbox basemap tiles (your style)
TILES = (
   "https://api.mapbox.com/styles/v1/katestrauch/"
"cmm86a95z000c01qr18i03nmc/tiles/256/{z}/{x}/{y}@2x"
"?access_token=pk.eyJ1Ijoia2F0ZXN0cmF1Y2giLCJhIjoiY21tODY2anJoMTBiYTJwb2oxMzJxM28ydiJ9.KzanJGTxXxyrGZpSEEv1jQ"
)

# Load data
df = pd.read_csv(INPUT_CSV, engine="python")

# Make sure coords are numeric
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
df = df.dropna(subset=["latitude", "longitude"]).copy()

print("Rows with coords:", len(df))
if len(df) == 0:
    raise ValueError("No valid latitude/longitude found. Check your geocoded CSV.")

# Create map
m = folium.Map(
    location=[df["latitude"].mean(), df["longitude"].mean()],
    zoom_start=11,
    tiles=None
)

# Add Mapbox basemap
folium.TileLayer(
    tiles=TILES,
    attr="© Mapbox © OpenStreetMap",
    name="Custom Mapbox Style",
    overlay=False,
    control=True
).add_to(m)

# Add simple markers (with popups)
for _, row in df.iterrows():
    name = str(row.get("Name", ""))
    loc_type = str(row.get("Type", ""))
    desc = str(row.get("Description", ""))
    popup_html = f'<div><b>{name}</b><br>{loc_type}<br>{desc}</div>'
    folium.Marker(
        location=[float(row["latitude"]), float(row["longitude"])],
        tooltip=name,
        popup=folium.Popup(popup_html, max_width=300),
    ).add_to(m)

folium.LayerControl().add_to(m)

m.save(OUTPUT_HTML)
print(f"Saved: {OUTPUT_HTML}")