import geopandas as gpd
import folium

# Загрузка данных о земельных участках, используемых в сельском хозяйстве
land_use = gpd.read_file("land_use.shp")

# Загрузка данных о потреблении воды на единицу площади
water_consumption = pd.read_csv("water_consumption.csv")

# Выделение участков земли, расположенных в бассейнах рек Tekeli River и Temirlik River
rivers = gpd.read_file("rivers.shp")
tekeli_basin = rivers[rivers["name"] == "Tekeli River"].buffer(1000)
temirlik_basin = rivers[rivers["name"] == "Temirlik River"].buffer(1000)

# Расчет суммарного потребления воды
total_consumption = 0
for index, row in land_use.iterrows():
    if row.geometry.intersects(tekeli_basin) or row.geometry.intersects(temirlik_basin):
        consumption = water_consumption[water_consumption["land_use"] == row["land_use"]]["consumption"].values[0]
        total_consumption += consumption * row.area

# Визуализация данных на карте
m = folium.Map(location=[43.25, 78.1], zoom_start=9)
folium.GeoJson("rivers.shp").add_to(m)
folium.GeoJson("land_use.shp", style_geojson).add_to(m)

# Сохранение карты
m.save("107.html")

print(f"Суммарное потребление воды для нужд сельского хозяйства по рекам Tekeli River и Temirlik River: {total_consumption} единиц измерения.")```



**Важно:** 

* Данный код является примером решения и может быть адаптирован под конкретные данные и требования.
* Необходимо заменить имена файлов ("land_use.shp", "water_consumption.csv", "rivers.shp") на фактические имена файлов с данными.
* Необходимо установить библиотеки geopandas, folium и pandas: