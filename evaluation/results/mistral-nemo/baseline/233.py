import geopandas as gpd
from shapely.geometry import Point, LineString
import numpy as np
import folium

# Load river Kummel geometry from data (assuming it's in a GeoPandas DataFrame)
river_data = gpd.read_file("river_kummel.shp")

# Assume we have flood height data for each point along the river
flood_heights = {
    "point1": 5,
    "point2": 3,
    # ...
}

def create_nft(river_geometry, flood_height):
    """
    Create a non-functional triangle (NFT) based on the given river geometry and flood height.
    """
    # Calculate the extent of the NFT based on flood height
    nft_extent = flood_height * 2

    # Create points for the NFT
    p1 = Point(river_geometry.coords[0][0] - nft_extent, river_geometry.coords[0][1])
    p2 = Point(river_geometry.coords[-1][0] + nft_extent, river_geometry.coords[-1][1])
    p3 = Point(river_geometry.centroid.x, river_geometry.centroid.y + nft_extent)

    # Create the NFT geometry
    nft_geometry = LineString([p1, river_geometry.boundary[0], p2, p3])

    return gpd.GeoDataFrame(geometry=[nft_geometry])

# Create NFTs for each section of the river with significant flood height
river_nfts = []
for index, row in river_data.iterrows():
    if row.name in flood_heights and flood_heights[row.name] > 0:
        nft = create_nft(row.geometry, flood_heights[row.name])
        river_nfts.append(nft)

# Combine all NFTs into a single GeoDataFrame
all_nfts = gpd.GeoDataFrame(pd.concat(river_nfts))

# Create a map with folium and add NFTs to it
m = folium.Map(location=[river_data.centroid.y, river_data.centroid.x], zoom_start=13)

for index, row in all_nfts.iterrows():
    folium.GeoJson(row.geometry, style_function=lambda x: {'fillColor': 'blue', 'color': 'black'}).add_to(m)

# Save the final map as "233.html"
m.save("233.html")