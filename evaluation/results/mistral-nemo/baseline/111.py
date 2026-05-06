import pandas as pd
import geopandas as gpd
from sklearn.ensemble import RandomForestClassifier
import folium

# 1. Подготовка данных
data_rivers = {
    'name': ['Aksu River', 'Temirlik River'],
    'length': [480, 275],
    'avg_flow': [36.5, 19.2]
}
df_rivers = pd.DataFrame(data_rivers)

data_factors = {
    'river_name': ['Aksu River', 'Temirlik River'],
    'avg_precipitation': [200, 250],
    'avg_temperature': [18, 22]
}
df_factors = pd.DataFrame(data_factors)

# 2. Слияние данных о реках и факторах риска
merged_df = pd.merge(df_rivers, df_factors, left_on='name', right_on='river_name')

# 3. Создание модели риска засухи (в данном примере используется простая классификация на основе длины реки)
X = merged_df[['length', 'avg_precipitation', 'avg_temperature']]
y = merged_df['name']
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# 4. Оценка риска засухи для каждой реки
risk_Aksu = clf.predict_proba([480, 200, 18])[0][1]
risk_Temirlik = clf.predict_proba([275, 250, 22])[0][1]

# 5. Визуализация результатов
m = folium.Map(location=[41.31, 69.98], zoom_start=8)

folium.Marker([41.31, 70.25], popup='Aksu River\nRisk: {:.2f}'.format(risk_Aksu)).add_to(m)
folium.Marker([40.55, 69.75], popup='Temirlik River\nRisk: {:.2f}'.format(risk_Temirlik)).add_to(m)

m.save("111.html")