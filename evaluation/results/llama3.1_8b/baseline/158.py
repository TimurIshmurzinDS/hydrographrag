import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from folium import Map, Marker

# Загрузка данных о уровнях воды в реках за различные годы
data = {
    'Year': [2010, 2011, 2012, 2013, 2014, 2015],
    'Bayankol_Level': [10.5, 11.2, 9.8, 12.1, 10.9, 11.5],
    'Sarykan_Level': [8.2, 7.5, 9.1, 6.8, 8.5, 7.2]
}
df = pd.DataFrame(data)

# Разделение данных на обучающую и проверочную выборки
X = df[['Year']]
y_Bayankol = df['Bayankol_Level']
y_Sarykan = df['Sarykan_Level']

X_train, X_test, y_train_Bayankol, y_test_Bayankol = train_test_split(X, y_Bayankol, test_size=0.2, random_state=42)
X_train, X_test, y_train_Sarykan, y_test_Sarykan = train_test_split(X, y_Sarykan, test_size=0.2, random_state=42)

# Создание и обучение модели линейной регрессии для каждого реки
model_Bayankol = LinearRegression()
model_Bayankol.fit(X_train, y_train_Bayankol)

model_Sarykan = LinearRegression()
model_Sarykan.fit(X_train, y_train_Sarykan)

# Прогнозирование наиболее опасных периодов паводка в будущем
future_years = pd.DataFrame({'Year': [2020, 2021, 2022]})
future_Bayankol_levels = model_Bayankol.predict(future_years)
future_Sarykan_levels = model_Sarykan.predict(future_years)

# Визуализация результатов на карте с помощью библиотеки Folium
m = Map(location=[50.0, 90.0], zoom_start=6)
Marker(location=[50.0, 90.0], popup='Река Баянколь').add_to(m)
Marker(location=[51.0, 91.0], popup='Река Сарыкан').add_to(m)

for i in range(len(future_Bayankol_levels)):
    Marker(location=[50.0 + (i * 1), 90.0], popup=f'Год: {future_years.iloc[i]["Year"]}, Уровень воды в реке Баянколь: {future_Bayankol_levels[i]}').add_to(m)

for i in range(len(future_Sarykan_levels)):
    Marker(location=[51.0 + (i * 1), 91.0], popup=f'Год: {future_years.iloc[i]["Year"]}, Уровень воды в реке Сарыкан: {future_Sarykan_levels[i]}').add_to(m)

m.save("158.html")