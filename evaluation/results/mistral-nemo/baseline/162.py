import pandas as pd
from scipy.stats import pearsonr, spearmanr
import folium

# 1. Подготовка данных
data_bayankol = pd.read_csv('bayankol_data.csv')
data_lepsy = pd.read_csv('lepsy_data.csv')

# 2. Преобразование данных
data_bayankol['date'] = pd.to_datetime(data_bayankol['date'])
data_lepsy['date'] = pd.to_datetime(data_lepsy['date'])

data_bayankol.set_index('date', inplace=True)
data_lespy.set_index('date', inplace=True)

bayankol_daily = data_bayankol.resample('D').mean()
lepsy_daily = data_lepsy.resample('D').mean()

# 3. Анализ корреляции
corr_bayankol, _ = pearsonr(bayankol_daily['snowmelt'], bayankol_daily['water_level'])
corr_lepsy, _ = spearmanr(lepsy_daily['snowmelt'], lespy_daily['water_level'])

# 4. Визуализация результатов
m = folium.Map(location=[50, 100], zoom_start=4)

folium.Marker([bayankol_coords[0], bayankol_coords[1]], popup=f'Bayankol River\nCorrelation: {corr_bayankol:.2f}').add_to(m)
folium.Marker([lepsy_coords[0], lepsy_coords[1]], popup=f'Lepsy River\nCorrelation: {corr_lepsy:.2f}').add_to(m)

m.save("162.html")