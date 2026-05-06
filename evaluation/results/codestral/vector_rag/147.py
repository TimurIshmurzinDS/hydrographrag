python
   import pandas as pd

   # Предположим, что у нас есть DataFrame с информацией о датчиках в районе рек Бутак и Сарыкан
   sensors_data = pd.DataFrame({
       'Sensor_ID': ['S1', 'S2', 'S3'],
       'River': ['Butak', 'Butak', 'Sarykan'],
       'Status': ['OK', 'Error', 'OK']
   })

   # Проверяем статус передачи данных датчиков в районе рек Бутак и Сарыкан
   butak_sensors = sensors_data[sensors_data['River'] == 'Butak']
   sarykan_sensors = sensors_data[sensors_data['River'] == 'Sarykan']

   # Проверяем, есть ли ошибки в передаче данных датчиков в районе рек Бутак и Сарыкан
   butak_errors = butak_sensors[butak_sensors['Status'] != 'OK'].shape[0]
   sarykan_errors = sarykan_sensors[sarykan_sensors['Status'] != 'OK'].shape[0]

   if butak_errors == 0 and sarykan_errors == 0:
       print("Все датчики в районе рек Бутак и Сарыкан передают данные без ошибок.")
   else:
       print("Не все датчики в районе рек Бутак и Сарыкан передают данные без ошибок.")