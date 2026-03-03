import pandas as pd
import folium

# ---- FILES ----
INPUT_CSV = "hometown_locations_geocoded.csv"
OUTPUT_HTML = "hometown_map_with_markers.html"

# ---- MAPBOX BASEMAP ----
TILES = (
    "https://api.mapbox.com/styles/v1/katestrauch/"
    "cmm86a95z000c01qr18i03nmc/tiles/256/{z}/{x}/{y}@2x"
    "?access_token=pk.eyJ1Ijoia2F0ZXN0cmF1Y2giLCJhIjoiY21tODY2anJoMTBiYTJwb2oxMzJxM28ydiJ9.KzanJGTxXxyrGZpSEEv1jQ"
)

# ---- LOAD DATA ----
df = pd.read_csv(INPUT_CSV, engine="python")
df = df.dropna(subset=["latitude", "longitude"]).copy()

# ---- STYLE RULES BY TYPE ----
STYLE_BY_TYPE = {
    "Historical":     {"color": "red",       "icon": "book",       "prefix": "fa"},
    "Cultural":   {"color": "green",     "icon": "museum",         "prefix": "fa"},
    "Restaurant":    {"color": "blue",      "icon": "utensils",          "prefix": "fa"},
    "Shopping": {"color": "purple",    "icon": "shopping-bag",   "prefix": "fa"},
    "Park":     {"color": "darkgreen", "icon": "tree",           "prefix": "fa"},
}

DEFAULT_STYLE = {"color": "cadetblue", "icon": "map-marker", "prefix": "fa"}

# ---- CENTER MAP ----
center_lat = df["latitude"].mean()
center_lon = df["longitude"].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles=None)

folium.TileLayer(
    tiles=TILES,
    attr="© Mapbox © OpenStreetMap",
    name="Custom Mapbox Style",
    overlay=False,
    control=True
).add_to(m)

# ---- FEATURE GROUPS ----
groups = {}
for t in df["Type"].fillna("Other").unique():
    groups[t] = folium.FeatureGroup(name=str(t), show=True)
    groups[t].add_to(m)

# ---- ADD MARKERS ----
for _, row in df.iterrows():
    name = str(row.get("Name", ""))
    address = str(row.get("Address", ""))
    loc_type = str(row.get("Type", "Other"))
    desc = str(row.get("Description", ""))
    img = str(row.get("Image_URL", "")).strip()

    style = STYLE_BY_TYPE.get(loc_type, DEFAULT_STYLE)

    popup_html = (
        f'<div style="width:260px;">'
        f'<h4 style="margin:0 0 6px 0;">{name}</h4>'
        f'<div><b>Type:</b> {loc_type}</div>'
        f'<div><b>Address:</b> {address}</div>'
        f'<div style="margin-top:6px;">{desc}</div>'
    )

    if img and img.lower().startswith("http"):
        popup_html += f'<div style="margin-top:8px;"><a href="{img}" target="_blank">Image link</a></div>'

    popup_html += '</div>'

    marker = folium.Marker(
        location=[float(row["latitude"]), float(row["longitude"])],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{name} ({loc_type})",
        icon=folium.Icon(color=style["color"], icon=style["icon"], prefix=style["prefix"]),
    )

    groups.get(loc_type, groups[list(groups.keys())[0]]).add_child(marker)

# ---- SAVE ----
folium.LayerControl(collapsed=False).add_to(m)
m.save(OUTPUT_HTML)
print(f"Saved map: {OUTPUT_HTML}")