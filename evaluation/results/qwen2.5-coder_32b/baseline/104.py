import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Загрузка данных о реках из GeoJSON файлов (предположим, что данные уже подготовлены)
rivers = gpd.read_file('rivers.geojson')

# Фильтрация данных для получения только нужных рек
shyzyn = rivers[rivers['name'] == 'Шыжын']
dos = rivers[rivers['name'] == 'Дос']

if shyzyn.empty or dos.empty:
    raise ValueError("Одна из рек не найдена в данных.")

# Шаг 2: Анализ топологии
# Предположим, что конец притока ближе к началу основной реки
shyzyn_end = shyzyn.geometry.iloc[0].coords[-1]
dos_start = dos.geometry.iloc[0].coords[0]

# Проверка близости точек
distance_threshold = 1000  # пороговое расстояние в метрах

if Point(shyzyn_end).distance(Point(dos_start)) < distance_threshold:
    print("Река Шыжын является притоком реки Дос.")
else:
    raise ValueError("Река Шыжын не является притоком реки Дос.")

# Шаг 3: Расчет расстояния между точками слияния
# Предположим, что точки слияния совпадают с найденными концом и началом
distance = Point(shyzyn_end).distance(Point(dos_start))
print(f"Расстояние до слияния рек составляет: {distance} метров")

# Шаг 4: Визуализация на карте
m = folium.Map(location=[(shyzyn.geometry.iloc[0].centroid.y + dos.geometry.iloc[0].centroid.y) / 2,
                        (shyzyn.geometry.iloc[0].centroid.x + dos.geometry.iloc[0].centroid.x) / 2], zoom_start=10)

# Добавление рек на карту
folium.GeoJson(shyzyn, name='Шыжын').add_to(m)
folium.GeoJson(dos, name='Дос').add_to(m)

# Добавление маркеров для точек слияния
folium.Marker(location=[shyzyn_end[1], shyzyn_end[0]], popup='Конец Шыжын', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker(location=[dos_start[1], dos_start[0]], popup='Начало Дос', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("104.html")