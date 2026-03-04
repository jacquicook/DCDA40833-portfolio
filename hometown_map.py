import pandas as pd
import requests
import folium
import urllib.parse

# -----------------------------
# YOUR MAPBOX INFO
# -----------------------------
access_token = "pk.eyJ1IjoiamFjcXVpY29vayIsImEiOiJjbW1iYzVtZHUwNzkzMnNyMngwZHBiYWN6In0.hDZo80QIhuWIKyZLKH5toQ"
username = "jacquicook"
style_id = "cmmbccdrt007w01rybl7x8eki"

# IMPORTANT: use 512 tiles for Mapbox styles
tiles = f"https://api.mapbox.com/styles/v1/{username}/{style_id}/tiles/512/{{z}}/{{x}}/{{y}}?access_token={access_token}"

# -----------------------------
# READ CSV FILE
# -----------------------------
df = pd.read_csv("hometown_locations.csv")

# -----------------------------
# GEOCODING FUNCTION
# -----------------------------
def geocode(address):
    address_encoded = urllib.parse.quote(address)
    geocode_url = f"https://api.mapbox.com/search/geocode/v6/forward?q={address_encoded}&access_token={access_token}"
    response = requests.get(geocode_url)
    data = response.json()

    try:
        coordinates = data["features"][0]["geometry"]["coordinates"]
        lon = coordinates[0]
        lat = coordinates[1]
        return lat, lon
    except:
        return None, None

# -----------------------------
# GEOCODE ADDRESSES
# -----------------------------
df["Latitude"], df["Longitude"] = zip(*df["Address"].apply(geocode))

# -----------------------------
# CREATE MAP
# -----------------------------
center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles=None)

# Add Mapbox basemap (Leaflet needs zoomOffset when using 512 tiles)
folium.TileLayer(
    tiles=tiles,
    attr="Mapbox",
    name="Mapbox Style",
    overlay=False,
    control=False,
    tilesize=512,
    zoomOffset=-1
).add_to(m)

# -----------------------------
# MARKER COLORS
# -----------------------------
color_dict = {
    "School": "purple",
    "Landmark": "red",
    "Downtown": "blue",
    "Attraction": "green",
    "Museum": "darkpurple",
    "Restaurant": "orange",
    "Shopping Center": "cadetblue",
    "Entertainment": "pink",
    "Garden": "lightgreen"
}

# -----------------------------
# ADD MARKERS
# -----------------------------
for _, row in df.iterrows():
    color = color_dict.get(row["Type"], "gray")

    popup_html = f"""
    <b>{row['Name']}</b><br>
    {row['Description']}<br>
    <img src="{row['Image_URL']}" width="200">
    """

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color=color)
    ).add_to(m)

# -----------------------------
# SAVE MAP
# -----------------------------
m.save("hometown_map.html")
print("Map created! Open hometown_map.html")
