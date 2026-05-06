import os
from osgeo import ogr, gdal
import folium

# Шаг 1: Подготовка данных
def prepare_data():
    # Чтение данных о сельскохозяйственных угодьях из Shapefile
    shp_path = 'selskohozyaystva.shp'
    driver = ogr.GetDriverByName('ESRI Shapefile')
    selskohozyaystva_layer = driver.Open(shp_path).GetLayer()
    
    # Чтение гидрологических данных из Shapefile
    hydrolayer_path = 'hydrolayer.shp'
    hydrolayer_driver = ogr.GetDriverByName('ESRI Shapefile')
    hydrolayer = hydrolayer_driver.Open(hydrolayer_path).GetLayer()
    
    return selskohozyaystva_layer, hydrolayer

# Шаг 2: Геопrocessing
def geoprocess(selskohozyaystva_layer, hydrolayer):
    # Вычисление площади сельскохозяйственных угодий и интенсивности использования
    selskohozyaystva_features = []
    for feature in selskohozyaystva_layer:
        area = feature.GetField('area')
        intensity = feature.GetField('intensity')
        selskohozyaystva_features.append((area, intensity))
    
    # Вычисление гидрологических характеристик
    hydrolayer_features = []
    for feature in hydrolayer:
        flow_rate = feature.GetField('flow_rate')
        depth = feature.GetField('depth')
        speed = feature.GetField('speed')
        hydrolayer_features.append((flow_rate, depth, speed))
    
    return selskohozyaystva_features, hydrolayer_features

# Шаг 3: Оценка нагрузки на водные ресурсы
def calculate_load(selskohozyaystva_features, hydrolayer_features):
    load = []
    for i in range(len(selskohozyaystva_features)):
        area, intensity = selskohozyaystva_features[i]
        flow_rate, depth, speed = hydrolayer_features[i]
        load.append((area * intensity) / (flow_rate + depth + speed))
    
    return load

# Шаг 4: Визуализация результатов
def visualize_results(load):
    m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)
    for i in range(len(load)):
        area, intensity = selskohozyaystva_features[i]
        flow_rate, depth, speed = hydrolayer_features[i]
        load_value = load[i]
        folium.Marker([55.7558 + i * 0.01, 37.6173], popup=f'Загрузка: {load_value}').add_to(m)
    
    m.save("190.html")

# Основная функция
def main():
    selskohozyaystva_layer, hydrolayer = prepare_data()
    selskohozyaystva_features, hydrolayer_features = geoprocess(selskohozyaystva_layer, hydrolayer)
    load = calculate_load(selskohozyaystva_features, hydrolayer_features)
    visualize_results(load)

if __name__ == "__main__":
    main()