import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from scipy.stats import norm
import folium

# Подготовка данных
df = pd.read_csv('исторические_данные.csv')
df.dropna(inplace=True)  # Удаление пропусков
df['Дата'] = pd.to_datetime(df['Дата'])  # Преобразование типа данных для даты

# Разделение данных на обучающую и тестовую выборку
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Функция расчета эффективности стратегии трейдинга
def calculate_efficiency(strategy):
    # Расчет прибыльности
    profit = (strategy['Цена_акции'].iloc[-1] - strategy['Цена_акции'].iloc[0]) / strategy['Цена_акции'].iloc[0]
    
    # Расчет риска
    risk = mean_squared_error(strategy['Цена_акции'], strategy['Цена_акции'].shift(1))
    
    # Расчет Sharpe-коэффициента
    sharpe = (profit - 0.05) / risk
    
    return profit, risk, sharpe

# Функция сравнения эффективности различных стратегий трейдинга
def compare_strategies():
    strategies = ['Стратегия_1', 'Стратегия_2']  # Список стратегий для сравнения
    
    for strategy in strategies:
        efficiency_df = pd.DataFrame(columns=['Стратегия', 'Прибыльность', 'Риск', 'Sharpe-коэффициент'])
        
        for i in range(len(train_df)):
            train_strategy = train_df.iloc[:i+1]
            test_strategy = train_df.iloc[i:]
            
            profit, risk, sharpe = calculate_efficiency(train_strategy)
            efficiency_df.loc[len(efficiency_df)] = [strategy, profit, risk, sharpe]
        
        print(f'Эффективность {strategy}:')
        print(efficiency_df)

# Сравнение эффективности различных стратегий трейдинга
compare_strategies()

# Визуализация результатов на карте (не требуется в этом случае)
# m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)
# m.save("285.html")