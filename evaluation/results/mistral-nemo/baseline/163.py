import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Сбор данных
data = {
    'river': ['Sarykan River', 'Shyzhyn River'],
    'water_height': [5, 3],
    'flow_speed': [20, 15],
    'rainfall': [100, 80],
    'temperature': [15, 18]
}
df = pd.DataFrame(data)

# 2. Определение зон риска
risk_zones = {
    'Sarykan River': ['Zone A', 'Zone B'],
    'Shyzhyn River': ['Zone C', 'Zone D']
}

# 3. Анализ рисков (в данном примере мы просто присваиваем уровни риска, но на практике это должен быть более сложный анализ)
risk_levels = {
    'Zone A': 'High',
    'Zone B': 'Medium',
    'Zone C': 'Low',
    'Zone D': 'High'
}

# 4. Картографирование рисков
m = folium.Map(location=[50, 70], zoom_start=8)

for river in df['river']:
    for zone in risk_zones[river]:
        geometry = Point(df[df['river'] == river]['geometry'].iloc[0])
        gdf = gpd.GeoDataFrame({'risk_level': [risk_levels[zone]]}, geometry=[geometry])
        folium.Choropleth(
            geo_data=gdf,
            name='Risk Levels',
            columns=['risk_level'],
            key_on='feature',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.8,
            highlight=True
        ).add_to(m)

# 5. Рекомендации по управлению рисками (в данном примере мы просто выводим рекомендации, но на практике они должны быть более подробными и основанными на анализе рисков)
recommendations = {
    'Zone A': 'Construct protective structures and plan evacuation routes.',
    'Zone B': 'Implement flood warning system and prepare emergency response plans.',
    'Zone C': 'Strengthen river banks and monitor water levels closely.',
    'Zone D': 'Develop contingency plans for potential flooding events.'
}

# 6. Визуализация результатов
m.save("163.html")