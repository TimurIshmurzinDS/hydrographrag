import folium
from shapely.geometry import Polygon
import geopandas as gpd

# Пример данных: площадь участка для орошения (в гектарах)
area_hectares = 100

# Пример данных: потребность в воде на основе метода Батлерса (в литрах на гектар)
water_need_per_hectare = 250000  # 250 л/га

# Расчет общего объема воды, требуемого для орошения
total_water_needed_liters = area_hectares * water_need_per_hectare

# Пример данных: объем воды в реке Аягоз (в литрах)
water_in_ayakoz_m3 = 10000000  # 10 миллионов литров

# Преобразование литров в кубические метры
water_in_ayakoz_cubic_meters = water_in_ayakoz_m3 / 1000

# Выделение объема воды из реки Аягоз
water_allocated_liters = min(total_water_needed_liters, water_in_ayakoz_cubic_meters * 1000)

# Вывод результатов
print(f"Объем воды, выделяемый на орошение в реке Аягоз: {water_allocated_liters:.2f} литров")

# Создание карты с использованием folium
m = folium.Map(location=[43.05, 76.98], zoom_start=12)

# Пример данных: координаты участка для орошения
polygon_coords = [
    (43.05, 76.98),
    (43.06, 76.98),
    (43.06, 76.99),
    (43.05, 76.99)
]

# Создание полигона на карте
folium.Polygon(
    locations=polygon_coords,
    color='blue',
    fill=True,
    fill_color='blue',
    fill_opacity=0.5
).add_to(m)

# Сохранение карты
m.save("43.html")