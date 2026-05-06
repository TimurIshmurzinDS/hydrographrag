import geopandas as gpd
from folium import Map, Marker
from folium.plugins import HeatMap

# Подготовка данных
river_data = gpd.read_file('river.shp')
river_coords = river_data.geometry.centroid

# Создание смарт-контракта (предположим, что мы используем Solidity)
contract_code = """
pragma solidity ^0.8.0;

contract RiverContract {
    // привязка к географическим координатам
    uint256 public longitude;
    uint256 public latitude;

    constructor(uint256 _longitude, uint256 _latitude) {
        longitude = _longitude;
        latitude = _latitude;
    }
}
"""

# Интеграция с гео-библиотекой
contract = RiverContract(river_coords.x, river_coords.y)

# Визуализация результата
m = Map(location=[river_coords.y, river_coords.x], zoom_start=10)
Marker([river_coords.y, river_coords.x], popup='Река Дос').add_to(m)
HeatMap([(river_coords.x, river_coords.y)]).add_to(m)
m.save("252.html")