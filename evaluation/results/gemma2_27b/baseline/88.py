import pandas as pd
import requests
from folium import Map, Marker, GeoJson

# **1. Получение данных о постах на реке Koktal River:**
# (Предполагаем, что данные о постах хранятся в CSV-файле)
posts = pd.read_csv("posts_koktal.csv")

# **2. Получение данных о текущем уровне воды:**
def get_water_level(post_id):
    url = f"https://api.hydromet.ru/data/{post_id}/latest"
    response = requests.get(url)
    return response.json()["level"]

posts["level"] = posts["id"].apply(lambda x: get_water_level(x))

# **3. Объединение данных:**
# (Данные о постах и уровне воды уже объединены в DataFrame "posts")

# **4. Визуализация данных:**
m = Map(location=[posts["latitude"].mean(), posts["longitude"].mean()], zoom_start=12)

for index, row in posts.iterrows():
    marker = Marker(location=[row["latitude"], row["longitude"]], popup=f"Пост {row['id']}: Уровень воды {row['level']} м")
    if row["level"] < 1:
        marker.fill_color = "green"
    elif 1 <= row["level"] < 3:
        marker.fill_color = "yellow"
    else:
        marker.fill_color = "red"

    marker.add_to(m)

# **5. Сохранение карты:**
m.save("88.html")