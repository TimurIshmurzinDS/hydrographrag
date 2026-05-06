import folium
from folium.plugins import HeatMap
import requests
from io import BytesIO
from PIL import Image

# Функция для загрузки изображения с URL
def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

# Загрузка изображения бассейна реки Каскелен
url = "https://example.com/path/to/cascade_basin.jpg"  # Замените на реальный URL изображения
img = download_image(url)

# Создание карты
m = folium.Map(location=[43.05, -123.68], zoom_start=12)

# Добавление изображения на карту
folium.raster_layers.ImageOverlay(
    image=img,
    bounds=[[43.05, -123.7], [43.05, -123.6]],
    opacity=0.8,
).add_to(m)

# Сохранение карты
m.save("255.html")