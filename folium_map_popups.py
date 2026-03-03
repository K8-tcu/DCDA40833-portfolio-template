import pandas as pd
import folium

# Input CSV and output HTML
INPUT_CSV = "hometown_locations_geocoded.csv"
OUTPUT_HTML = "hometown_map_popups.html"

# Your Mapbox basemap tiles (style tiles URL)
TILES = (
   "https://api.mapbox.com/styles/v1/katestrauch/"
"cmm86a95z000c01qr18i03nmc/tiles/256/{z}/{x}/{y}@2x"
"?access_token=pk.eyJ1Ijoia2F0ZXN0cmF1Y2giLCJhIjoiY21tODY2anJoMTBiYTJwb2oxMzJxM28ydiJ9.KzanJGTxXxyrGZpSEEv1jQ"
)

# Marker styles by Type (updated)
STYLE_BY_TYPE = {
    "historical": {"color": "red",      "icon": "book",         "prefix": "fa"},
    "cultural":   {"color": "green",    "icon": "university",   "prefix": "fa"},
    "park":       {"color": "blue",     "icon": "tree",         "prefix": "fa"},
    "shopping":   {"color": "purple",   "icon": "shopping-bag", "prefix": "fa"},
    "restaurant": {"color": "pink",     "icon": "utensils",     "prefix": "fa"},
    "other":      {"color": "gray",     "icon": "map-marker",   "prefix": "fa"},
}
DEFAULT_STYLE = {"color": "cadetblue", "icon": "map-marker", "prefix": "fa"}

# Read CSV
df = pd.read_csv(INPUT_CSV, engine="python")

print("TYPES IN CSV:", sorted(df["Type"].dropna().unique()))

# Keep only rows with coordinates
df = df.dropna(subset=["latitude", "longitude"]).copy()

# Center map on mean coordinates
m = folium.Map(
    location=[df["latitude"].mean(), df["longitude"].mean()],
    zoom_start=11,
    tiles=None
)

# Add basemap
folium.TileLayer(
    tiles=TILES,
    attr="© Mapbox © OpenStreetMap",
    name="Custom Mapbox Style",
    overlay=False,
    control=True
).add_to(m)

# Optional: layer groups by Type
groups = {}
for t in df["Type"].fillna("other").unique():
    groups[t] = folium.FeatureGroup(name=str(t), show=True)
    groups[t].add_to(m)

# Build popup HTML function
def build_popup_html(name, desc, img_url):
    name = "" if pd.isna(name) else str(name)
    desc = "" if pd.isna(desc) else str(desc)
    img_url = "" if pd.isna(img_url) else str(img_url).strip()

    img_html = ""
    if img_url.lower().startswith("http"):
        img_html = f"""
        <div style="margin-top:8px;">
          <img src="{img_url}" style="width: 100%; max-width: 260px; border-radius: 10px;" />
        </div>
        """

    html = f"""
    <div style="width: 280px;">
      <h4 style="margin:0 0 6px 0;">{name}</h4>
      <div style="font-size: 13px; line-height: 1.3;">{desc}</div>
      {img_html}
    </div>
    """
    return html

# Add markers to map
for _, row in df.iterrows():
    name = row.get("Name", "")
    loc_type = row.get("Type", "other").lower()
    desc = row.get("Description", "")
    img_url = row.get("Image_URL", "")

    style = STYLE_BY_TYPE.get(loc_type, DEFAULT_STYLE)
    popup_html = build_popup_html(name, desc, img_url)

    marker = folium.Marker(
        location=[float(row["latitude"]), float(row["longitude"])],
        tooltip=f"{name}",
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color=style["color"], icon=style["icon"], prefix=style["prefix"]),
    )

    groups.get(loc_type, groups[list(groups.keys())[0]]).add_child(marker)

# Add layer control
folium.LayerControl(collapsed=False).add_to(m)

# Save HTML
m.save(OUTPUT_HTML)
print(f"Saved: {OUTPUT_HTML}")