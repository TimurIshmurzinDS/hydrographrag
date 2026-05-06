import pandas as pd
import folium

# Загрузить данные в Pandas DataFrame
df1 = pd.read_csv('data1.csv')
df2 = pd.read_csv('data2.csv')

# Функция для сравнения двух временных рядов
def compare_series(s1, s2):
    return pd.DataFrame({'diff': s1 - s2})

# Создать DataFrame с разностью между двумя сериями
diff_df = compare_series(df1['value'], df2['value'])

# Визуализировать первый временной ряд на карте с помощью folium
m1 = folium.Map(location=[df1['lat'].mean(), df1['lon'].mean()], zoom_start=5)
for i in range(len(df1)):
    folium.CircleMarker(location=[df1.iloc[i]['lat'], df1.iloc[i]['lon']],
                        radius=df1.iloc[i]['value']/10,
                        color='blue').add_to(m1)

# Визуализировать разность между двумя временными рядами на отдельной карте с помощью folium
m2 = folium.Map(location=[diff_df['lat'].mean(), diff_df['lon'].mean()], zoom_start=5)
for i in range(len(diff_df)):
    folium.CircleMarker(location=[diff_df.iloc[i]['lat'], diff_df.iloc[i]['lon']],
                        radius=abs(diff_df.iloc[i]['diff'])/10,
                        color='red' if diff_df.iloc[i]['diff'] > 0 else 'green').add_to(m2)

# Сохранить обе карты в формате HTML
m1.save("283_1.html")
m2.save("283_2.html")