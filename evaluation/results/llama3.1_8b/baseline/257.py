import pandas as pd
import folium

# Подготовка данных о уровне воды в реке Баянколь
data = {
    'Дата': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'Уровень воды (м)': [15, 12, 8]
}
df = pd.DataFrame(data)

# Определение критерия потребности в поливе
def calculate_water_need(level):
    if level > 10:
        return 0
    else:
        return 100 - level * 10

# Создание функции расчета потребности в поливе
def water_need_function(df):
    df['Потребность в поливе'] = df['Уровень воды (м)'].apply(calculate_water_need)
    return df

# Расчет потребности в поливе
df = water_need_function(df)

# Визуализация результатов на карте
m = folium.Map(location=[50.0, 90.0], zoom_start=10)
folium.Choropleth(
    geo_data=df,
    data=df,
    columns=['Дата', 'Потребность в поливе'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)
m.save("257.html")