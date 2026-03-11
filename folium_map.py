import folium

# ----- Mapbox tile URL -----
TILES = (
"https://api.mapbox.com/styles/v1/katestrauch/"
"cmm86a95z000c01qr18i03nmc/tiles/256/{z}/{x}/{y}@2x"
"?access_token=pk.eyJ1Ijoia2F0ZXN0cmF1Y2giLCJhIjoiY21tODY2anJoMTBiYTJwb2oxMzJxM28ydiJ9.KzanJGTxXxyrGZpSEEv1jQ"
)

# ----- Create map -----
m = folium.Map(
location=[37.795122, -122.393187],
zoom_start=11,
tiles=None
)

# ----- Add Mapbox basemap -----
folium.TileLayer(
tiles=TILES,
attr="© Mapbox © OpenStreetMap",
name="Custom Mapbox Style",
overlay=False,
control=True
).add_to(m)

# ----- Save map -----
m.save("mapbox_folium_map.html")

print("SacMap saved as mapbox_folium_map.html")
print("HTML MAP SAVED")