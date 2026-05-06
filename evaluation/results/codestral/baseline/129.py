python
         import pandas as pd
         import folium
         from scipy import stats
         import matplotlib.pyplot as plt

         # Загрузка данных
         kurty_data = pd.read_csv('kurty_river_data.csv')
         tekes_data = pd.read_csv('tekes_river_data.csv')

         # Очистка и преобразование данных
         def clean_and_transform(df):
             df['date'] = pd.to_datetime(df['date'])
             df['year'] = df['date'].dt.year
             df['spring'] = (df['date'].dt.month >= 3) & (df['date'].dt.month <= 5)
             return df[df['spring']]

         kurty_data = clean_and_transform(kurty_data)
         tekes_data = clean_and_transform(tekes_data)

         # Сравнение показателей расхода воды
         ttest_result = stats.ttest_ind(kurty_data['water_flow'], tekes_data['water_flow'])

         print("T-Test Results:")
         print(f"t-statistic: {ttest_result.statistic}")
         print(f"p-value: {ttest_result.pvalue}")

         # Визуализация на карте
         m = folium.Map(location=[55, 37], zoom_start=6)

         kurty_avg = kurty_data['water_flow'].mean()
         tekes_avg = tekes_data['water_flow'].mean()

         folium.Marker([55.1287, 61.3449], popup=f"Kurty River Average Flow: {kurty_avg}").add_to(m)
         folium.Marker([54.0489, 45.1833], popup=f"Tekes River Average Flow: {tekes_avg}").add_to(m)

         m.save("129.html")

         # Гистограмма распределения расхода воды
         plt.figure(figsize=(10, 6))
         plt.hist(kurty_data['water_flow'], alpha=0.5, label='Kurty River', color='blue')
         plt.hist(tekes_data['water_flow'], alpha=0.5, label='Tekes River', color='red')
         plt.legend()
         plt.title('Water Flow Distribution in Kurty and Tekes Rivers (Spring Season)')
         plt.xlabel('Water Flow')
         plt.ylabel('Frequency')
         plt.show()