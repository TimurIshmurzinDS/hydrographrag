import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
import folium

# Загрузка данных о дренажной сети и границах бассейна
drainage_network = gpd.read_file('path_to_drainage_network.shp')
basin_boundary = gpd.read_file('path_to_basin_boundary.shp')

# Определение границ бассейна
basin_polygon = basin_boundary.geometry[0]

# Разбиение бассейна на геометрические участки (например, по площади)
def split_geometry(geometry, area_threshold):
    if geometry.area < area_threshold:
        return [geometry]
    else:
        parts = []
        for part in geometry.geoms:
            parts.extend(split_geometry(part, area_threshold))
        return parts

area_threshold = 100000  # Площадь участка в квадратных метрах
basin_parts = split_geometry(basin_polygon, area_threshold)

# Подсчет длины дренажных каналов в каждом участке
def calculate_drainage_density(drainage_network, basin_parts):
    density_results = []
    for part in basin_parts:
        part_gdf = gpd.GeoDataFrame(geometry=[part])
        intersection = drainage_network.intersection(part_gdf)
        total_length = intersection.geometry.length.sum()
        area = part.area
        density = total_length / area if area > 0 else 0
        density_results.append({'geometry': part, 'density': density})
    return gpd.GeoDataFrame(density_results)

drainage_density = calculate_drainage_density(drainage_network, basin_parts)

# Визуализация результатов на карте
m = folium.Map(location=[basin_polygon.centroid.y, basin_polygon.centroid.x], zoom_start=12)

folium.GeoJson(basin_boundary.geometry[0]).add_to(m)
folium.Choropleth(
    geo_data=drainage_density,
    name="Density",
    data=drainage_density,
    columns=["geometry", "density"],
    key_on="feature.properties.density",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Drainage Density"
).add_to(m)

folium.LayerControl().add_to(m)
m.save("172.html")