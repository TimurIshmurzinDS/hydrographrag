import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загрузка данных о стоке (заменить на ваши файлы)
flow_data_urzhar = pd.read_csv("urzhar_flow.csv")
flow_data_aksu = pd.read_csv("aksu_flow.csv")

# Расчет среднегодового стока
avg_flow_urzhar = flow_data_urzhar["flow"].mean()
avg_flow_aksu = flow_data_aksu["flow"].mean()

# Определение периода анализа (заменить на ваши даты)
start_date = pd.to_datetime("2010-01-01")
end_date = pd.to_datetime("2020-12-31")

# Фильтрация данных по периоду анализа
flow_data_urzhar_filtered = flow_data_urzhar[(flow_data_urzhar["date"] >= start_date) & (flow_data_urzhar["date"] <= end_date)]
flow_data_aksu_filtered = flow_data_aksu[(flow_data_aksu["date"] >= start_date) & (flow_data_aksu["date"] <= end_date)]

# Визуализация данных на карте
m = folium.Map(location=[43.0, 78.0], zoom_start=8)

folium.Marker([43.25, 79.0], popup="Urzhar River").add_to(m)
folium.Marker([42.5, 79.5], popup="Aksu River").add_to(m)

# Добавление данных о стоке на карту (необходимо дополнить кодом для визуализации данных)

m.save("117.html")