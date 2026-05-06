import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# Загрузить данные о сроках снеготаяния и стоке
data = pd.read_csv("lepsy_data.csv")

# Предобработать данные (например, заполнить пропуски)

# Обучить модель линейной регрессии
model = LinearRegression()
X = data["snowmelt_date"].values.reshape(-1, 1)
y = data["flow"].values
model.fit(X, y)

# Проанализировать коэффициенты модели
print("Коэффициент детерминации:", model.score(X, y))
print("Коэффициент наклона:", model.coef_)

# Создать карту с folium
m = folium.Map(location=[data["latitude"].mean(), data["longitude"].mean()], zoom_start=10)

# Нанести точки данных на карту
for index, row in data.iterrows():
    folium.Marker([row["latitude"], row["longitude"]], popup=f"Дата снеготаяния: {row['snowmelt_date']}, Сток: {row['flow']}").add_to(m)

# Сохранить карту
m.save("205.html")