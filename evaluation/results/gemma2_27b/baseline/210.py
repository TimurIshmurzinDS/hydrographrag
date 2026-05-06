python
import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загрузка данных
data_lepsy = pd.read_csv("lepsy_river_data.csv")
data_aksu = pd.read_csv("aksu_river_data.csv")

# Форматирование данных
data_lepsy["datetime"] = pd.to_datetime(data_lepsy[["date", "time"]])
data_aksu["datetime"] = pd.to_datetime(data_aksu[["date", "time"]])

# Сезонное разделение
def get_season(datetime):
    month = datetime.month
    if month in [12, 1, 2]:
        return "зима"
    elif month in [3, 4, 5]:
        return "весна"
    elif month in [6, 7, 8]:
        return "лето"
    else:
        return "осень"

data_lepsy["season"] = data_lepsy["datetime"].apply(get_season)
data_aksu["season"] = data_aksu["datetime"].apply(get_season)

# Расчет статистики по сезонам
seasons = ["зима", "весна", "лето", "осень"]
for season in seasons:
    lepsy_season_data = data_lepsy[data_lepsy["season"] == season]
    aksu_season_data = data_aksu[data_aksu["season"] == season]

    print(f"Season: {season}")
    print(f"Lepsy River:")
    print(lepsy_season_data["flow"].describe())
    print(f"Aksu River:")
    print(aksu_season_data["flow"].describe())

# Визуализация

plt.figure()
plt.plot(data_lepsy[data_lepsy["season"] == "лето"]["datetime"], data_lepsy[data_lepsy["season"] == "лето"]["flow"])
plt.show()

# Карта

m = folium.Map(location=[40, 75], zoom_start=6)
folium.Marker([40.1, 75.2], popup="Lepsy River").add_to(m)
folium.Marker([40.3, 75.4], popup="Aksu River").add_to(m)

m.save("210.html")