import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import folium

# 1. Загрузка данных
data = pd.read_csv("migration_data.csv")

# 2. Обработка данных
features = ["origin", "destination", "socioeconomic_factor"]
target = "migration_count"
X = data[features]
y = data[target]

# 3. Обучение модели (Logistic Regression)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LogisticRegression()
model.fit(X_train, y_train)

# 4. Прогнозирование
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

# 5. Визуализация (folium)
m = folium.Map()
for index, row in data.iterrows():
    folium.Marker([row["latitude"], row["longitude"]], popup=str(row["migration_count"])).add_to(m)

m.save("278.html")