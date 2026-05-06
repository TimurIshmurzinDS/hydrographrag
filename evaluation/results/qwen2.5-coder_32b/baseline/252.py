# Шаг 1: Сбор данных (пример координат реки Дос)
import folium

# Пример координат реки Дос (в реальном проекте нужно использовать точные данные)
river_dos_coordinates = [
    [42.8503, 74.6091],
    [42.8505, 74.6093],
    [42.8508, 74.6095]
]

# Шаг 2: Определение границ (пример прямоугольной области вокруг реки)
bounds = [
    [min(coord[0] for coord in river_dos_coordinates) - 0.01, min(coord[1] for coord in river_dos_coordinates) - 0.01],
    [max(coord[0] for coord in river_dos_coordinates) + 0.01, max(coord[1] for coord in river_dos_coordinates) + 0.01]
]

# Шаг 3: Создание интерактивной карты с использованием folium
m = folium.Map(location=[42.8506, 74.6093], zoom_start=13)

# Добавление линии реки на карту
folium.PolyLine(river_dos_coordinates, color="blue", weight=2.5, opacity=1).add_to(m)

# Шаг 4: Визуализация границ зоны действия смарт-контракта (пример прямоугольной области)
folium.Rectangle(bounds=bounds, color="#ff7800", fill=True, fill_color="#ffff00", fill_opacity=0.1).add_to(m)

# Шаг 5: Сохранение карты в HTML файл
m.save("252.html")

# Пример кода смарт-контракта (Solidity)
smart_contract_code = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RiverDOSContract {
    struct Location {
        int256 latitude;
        int256 longitude;
    }

    mapping(address => Location) public userLocations;

    function setLocation(int256 _latitude, int256 _longitude) public {
        require(_latitude >= 428303 && _latitude <= 428708 && _longitude >= 746091 && _longitude <= 746095, "Location is outside the allowed area");
        userLocations[msg.sender] = Location(_latitude, _longitude);
    }

    function getLocation(address _user) public view returns (int256, int256) {
        return (userLocations[_user].latitude, userLocations[_user].longitude);
    }
}
"""

# Вывод кода смарт-контракта
print(smart_contract_code)