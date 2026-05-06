import requests
from bs4 import BeautifulSoup
import folium

# Шаг 1: Получение данных о водном уровне реки Batareyka River
# Предположим, что данные доступны на сайте службы гидрометрии в формате HTML таблицы.
url = "https://example.com/hydrology/batareyka_river_level"  # Замените URL на реальный источник данных

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Предположим, что данные находятся в первой таблице на странице
table = soup.find('table')
rows = table.find_all('tr')

# Извлечение последних данных о водном уровне (предполагается, что последняя строка содержит актуальные данные)
last_row = rows[-1]
columns = last_row.find_all('td')
water_level = float(columns[2].text.strip())  # Предположим, что уровень воды в третьей колонке

# Координаты реки Batareyka River (примерные координаты)
latitude = 53.9045
longitude = 27.5612

# Шаг 2: Создание интерактивной карты с помощью folium
m = folium.Map(location=[latitude, longitude], zoom_start=12)

# Добавление маркера с информацией о водном уровне
folium.Marker(
    [latitude, longitude],
    popup=f"Текущий уровень воды: {water_level} м",
    tooltip="Наведите курсор"
).add_to(m)

# Шаг 3: Сохранение карты в файл
m.save("7.html")

print(f"Карта сохранена как '7.html'. Текущий уровень воды: {water_level} м")