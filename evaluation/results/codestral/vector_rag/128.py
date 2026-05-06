python
   # Загрузите исторические данные уровня воды реки Lepsy
   lepsy_data = load_data('Lepsy_river_water_levels.csv')

   # Загрузите исторические данные паводков в реке Dos
   dos_flood_data = load_data('Dos_river_flood_events.csv')

   # Объедините данные по датам
   merged_data = merge_data(lepsy_data, dos_flood_data)

   # Проведите статистический анализ для определения связи между уровнем воды в реке Lepsy и паводками в реке Dos
   analysis_result = statistical_analysis(merged_data)

   # Используйте результаты анализа для прогнозирования вероятности паводка в реке Dos на следующий сезон
   flood_probability = predict_flood_probability(analysis_result, next_season_data)