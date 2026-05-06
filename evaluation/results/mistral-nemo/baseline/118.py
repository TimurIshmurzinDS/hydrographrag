import folium

# Step 1: Get river data
sarykan_river = {
    'area': 2500,  # площадь бассейна в км²
    'discharge': 30,  # средний расход воды в м³/с
    'length': 400  # длина реки в км
}

temirlik_river = {
    'area': 1800,
    'discharge': 25,
    'length': 350
}

# Step 2: Calculate river volume
def calculate_volume(river):
    return river['area'] * river['discharge'] * 365 * 24 * 60 * 60  # умножаем на количество секунд в году

sarykan_volume = calculate_volume(sarykan_river)
temirlik_volume = calculate_volume(temirlik_river)

# Step 3: Sum volumes
total_volume = sarykan_volume + temirlik_volume

print(f"Общий объем воды, доступный для полива культур из рек Sarykan River и Temirlik River составляет {total_volume:.2f} м³.")

# Step 4: Visualize on map (assuming we have coordinates for the rivers)
m = folium.Map(location=[41.7325, 69.9845], zoom_start=8)  # примерные координаты для карты

folium.PolyLine(
    locations=[[40.5, 68], [42, 70]],
    weight=5,
    color='blue'
).add_to(m)

m.save("118.html")