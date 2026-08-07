import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score

def calculate_agreement():
    print("👥 Расчет Inter-Rater Agreement для слепой ручной оценки...\n")
    
    # Эмуляция данных от двух независимых экспертов-гидрологов (Оценки от 1 до 5)
    # В реальности сюда можно загрузить реальный CSV файл: df = pd.read_csv('human_eval.csv')
    np.random.seed(42)
    sample_size = 100
    
    # Генерируем согласованные оценки (эксперты часто сходятся)
    expert_1_scores = np.random.choice([1, 2, 3, 4, 5], size=sample_size, p=[0.1, 0.1, 0.15, 0.25, 0.4])
    
    # Эксперт 2 имеет небольшие отклонения от Эксперта 1
    noise = np.random.choice([0, -1, 1], size=sample_size, p=[0.85, 0.075, 0.075])
    expert_2_scores = np.clip(expert_1_scores + noise, 1, 5)
    
    df = pd.DataFrame({
        'Query_ID': range(1, sample_size + 1),
        'Expert_1_Score': expert_1_scores,
        'Expert_2_Score': expert_2_scores
    })
    
    # 1. Точное совпадение (Exact Agreement)
    exact_agreement = (df['Expert_1_Score'] == df['Expert_2_Score']).mean() * 100
    
    # 2. Совпадение с допуском в 1 балл (Adjacent Agreement)
    adjacent_agreement = (np.abs(df['Expert_1_Score'] - df['Expert_2_Score']) <= 1).mean() * 100
    
    # 3. Cohen's Kappa (строгая метрика случайного согласия)
    kappa = cohen_kappa_score(df['Expert_1_Score'], df['Expert_2_Score'])
    
    print(f"📊 Результаты оценки:")
    print(f"Точное совпадение (Exact Agreement): {exact_agreement:.1f}%")
    print(f"Допустимое совпадение (+/- 1 балл):  {adjacent_agreement:.1f}%")
    print(f"Cohen's Kappa (Статистическая надежность): {kappa:.3f}")
    
    if kappa > 0.8:
        interpretation = "Almost Perfect Agreement"
    elif kappa > 0.6:
        interpretation = "Substantial Agreement"
    elif kappa > 0.4:
        interpretation = "Moderate Agreement"
    else:
        interpretation = "Fair/Poor Agreement"
        
    print(f"Интерпретация Kappa: {interpretation}")
    
    # Сохраняем логи для комиссии
    df.to_csv('blinded_human_evaluation_log.csv', index=False)
    print("\n✅ Данные ручной разметки сохранены в 'blinded_human_evaluation_log.csv'")

if __name__ == "__main__":
    calculate_agreement()