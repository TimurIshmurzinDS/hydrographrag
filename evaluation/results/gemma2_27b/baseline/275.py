python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import folium

# 1. Загрузка данных (заменить на ваш путь к файлу)
data = pd.read_csv("solar_flare_data.csv")

# 2. Предобработка данных
# Кодирование категорических переменных, если необходимо
# Разделение данных на признаки (X) и целевую переменную (y)

# 3. Обучение модели
X = data[['feature1', 'feature2', ...]]
y = data['flare_occurrence']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression()
model.fit(X_train, y_train)

# 4. Оценка модели
y_pred = model.predict_proba(X_test)[:,1] # Вероятность вспышки
auc = roc_auc_score(y_test, y_pred)
print("AUC:", auc)

# 5. Визуализация (пример)
m = folium.Map(location=[0, 0], zoom_start=2)
for index, row in data.iterrows():
    folium.Circle(location=[row['latitude'], row['longitude']], radius=10000 * row['probability'], color='red', fill=True).add_to(m)

m.save("275.html")