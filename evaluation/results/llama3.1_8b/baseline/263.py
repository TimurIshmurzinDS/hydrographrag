import folium
from folium.plugins import HeatMap

# Данные о реке Талгар (предположительно)
talgar_river = {
    'lat': 42.5,
    'lon': 76.7,
    'water_volume': 1000  # в кубических метрах
}

# Данные о Марсе (предположительно)
mars_data = {
    'temperature_range': (-125, 20),  # в градусах Цельсия
    'atmospheric_pressure': 6.1e-3,  # в Паскалях
    'soil_type': ['rocky', 'sand']  # тип почвы
}

# Функция для определения потенциальных мест для выращивания картофеля на Марсе
def find_potential_sites(mars_data):
    potential_sites = []
    for i in range(-90, 91):
        for j in range(-180, 181):
            if mars_data['temperature_range'][0] <= i <= mars_data['temperature_range'][1]:
                if mars_data['atmospheric_pressure'] > 6.1e-3:
                    potential_sites.append((i, j))
    return potential_sites

# Функция для создания карты потенциальных мест для выращивания картофеля на Марсе
def create_map(potential_sites):
    m = folium.Map(location=[0, 0], zoom_start=2)
    HeatMap(potential_sites, radius=10).add_to(m)
    return m

# Основная функция
def main():
    potential_sites = find_potential_sites(mars_data)
    m = create_map(potential_sites)
    m.save("263.html")

if __name__ == "__main__":
    main()