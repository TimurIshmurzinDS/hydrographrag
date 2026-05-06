import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import folium

# Загрузите исторические данные обоих рек
data_lepsy = pd.read_csv('lepsy_data.csv')
data_dos = pd.read_csv('dos_data.csv')

# Объедините данные обоих рек
data = pd.merge(data_lepsy, data_dos, on='date', how='inner')

# Определите признаки и целевую переменную
X = data.drop(['pavodok'], axis=1)
y = data['pavodok']

# Разделите данные на обучающую и проверочную выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создайте случайный лес для классификации
rfc = RandomForestClassifier(n_estimators=100, random_state=42)
rfc.fit(X_train, y_train)

# Оцените точность модели на проверочной выборке
y_pred = rfc.predict(X_test)
print('Точность:', accuracy_score(y_test, y_pred))
print('Отчет о классификации:')
print(classification_report(y_test, y_pred))

# Создайте геоспациальное моделирование с помощью методов машинного обучения
model = folium.Map(location=[55.76, 49.13], zoom_start=10)
folium.Marker([55.76, 49.13], popup='Река Lepsy').add_to(model)
folium.Marker([55.77, 49.12], popup='Река Dos').add_to(model)

# Добавьте слой с вероятностью паводка
folium.Choropleth(
    geo_data='dos_boundaries.geojson',
    name='Паводок',
    data=data,
    columns=['pavodok'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(model)

# Сохраните карту в файл
model.save('128.html')