import pandas as pd
import folium

# Загрузка данных о расходах рек
df_lepsy = pd.read_csv("lepsy_river_data.csv")
df_shilik = pd.read_csv("shilik_river_data.csv")

# Определение границ сезона (пример)
seasons = {
    "весна": ("2023-03-1", "2023-5-31"),
    "лето": ("2023-6-1", "2023-8-31"),
    "осень": ("2023-9-1", "2023-11-30"),
    "зима": ("2023-12-1", "2023-2-28")
}

# Расчет среднего расхода по сезону
for season, dates in seasons.items():
    df_lepsy[season] = df_lepsy[(df_lepsy["date"] >= pd.to_datetime(dates[0])) & (df_lepsy["date"] <= pd.to_datetime(dates[1]))]["flow"].mean()

# Расчет объема стока
for season, dates in seasons.items():
    df_lepsy[f"{season}_volume"] = df_lepsy[season] * len(pd.date_range(start=pd.to_datetime(dates[0]), end=pd.to_datetime(dates[1])))

# Создание карты с folium
m = folium.Map(location=[df_lepsy["latitude"].mean(), df_lepsy["longitude"].mean()], zoom_start=8)

# Добавление рек на карту (пример)
folium.GeoJson("river_shapefile.geojson", name="Lepsy River").add_to(m)
folium.GeoJson("river_shapefile.geojson", name="Shilik River").add_to(m)

# Сохранение карты
m.save("152.html")