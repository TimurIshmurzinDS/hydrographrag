import geopandas as gpd
from qgis.core import *
from PyQt5.QtCore import QFileInfo
from folium import Map, Marker, GeoJson

# Load data into QGIS
QgsApplication.initQgis()
app = QgsApplication([], True)
QgsApplication.processEvents()

river_data = "path/to/your/river_data.shp"
river_layer = QgsVectorLayer(river_data, "River", "ogr")

# Model river flow using QGIS tools
processing.run("grass7:streamnetwork@qgis", {
    'input': river_layer,
    'd8': True,
    'threshold': 100,
    'output': 'memory://'
})

# Export data to GeoJSON format
river_geojson = "path/to/your/river_data.geojson"
QgsVectorFileWriter.writeAsVectorFormat(river_layer, river_geojson, "GeoJSON")

# Load data into Folium for visualization
m = Map(location=[51.5074, -0.1278], zoom_start=13)

folium.GeoJson(
    river_geojson,
    style_function=lambda x: {
        'fillColor': '#ffffff',
        'color': '#000000',
        'weight': 2,
        'dashArray': '5, 5'
    },
    highlight_function=lambda x: {'fillColor': '#00ff00', 'color': '#00ff00'},
    tooltip=folium.GeoJsonTooltip(fields=['name'], labels=True)
).add_to(m)

# Save the final map
m.save("251.html")