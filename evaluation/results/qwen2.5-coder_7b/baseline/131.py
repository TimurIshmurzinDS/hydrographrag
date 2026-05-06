import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Пример данных (замените на реальные данные)
data_sharyn = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Flow_Rate': [10, 12, 15, 18, 20, 22, 24, 23, 21, 19, 17, 16]
}

data_kishi = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Flow_Rate': [8, 9, 10, 12, 14, 16, 17, 15, 13, 11, 9, 8]
}

# Преобразование данных в DataFrame
df_sharyn = pd.DataFrame(data_sharyn)
df_kishi = pd.DataFrame(data_kishi)

# Преобразование месяца в числовой формат для моделирования
df_sharyn['Month'] = pd.Categorical(df_sharyn['Month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
df_kishi['Month'] = pd.Categorical(df_kishi['Month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

# Преобразование категорий в числовые значения
df_sharyn['Month'] = df_sharyn['Month'].cat.codes + 1
df_kishi['Month'] = df_kishi['Month'].cat.codes + 1

# Разделение данных на признаки и целевую переменную
X_sharyn = df_sharyn[['Month']]
y_sharyn = df_sharyn['Flow_Rate']

X_kishi = df_kishi[['Month']]
y_kishi = df_kishi['Flow_Rate']

# Обучение модели линейной регрессии для Sharyn River
model_sharyn = LinearRegression()
model_sharyn.fit(X_sharyn, y_sharyn)

# Прогнозирование для Kishi Almaty River на основе тренда Sharyn River
predicted_flow_kishi = model_sharyn.predict(X_kishi)

# Объединение прогнозов в DataFrame
df_kishi['Predicted_Flow'] = predicted_flow_kishi

# Визуализация данных и прогноза на карте
m = folium.Map(location=[43.21, 76.90], zoom_start=5)

for index, row in df_kishi.iterrows():
    folium.Marker([43.21, 76.90], popup=f"Month: {row['Month']}, Actual Flow: {row['Flow_Rate']}, Predicted Flow: {row['Predicted_Flow']}").add_to(m)

m.save("131.html")