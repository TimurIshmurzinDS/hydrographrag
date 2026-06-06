import os
import fitz  # Импорт библиотеки PyMuPDF

def convert_pdfs_to_png(input_dir, output_dir=None):
    # Если папка для сохранения не указана, сохраняем туда же
    if output_dir is None:
        output_dir = input_dir

    # Создаем выходную папку, если ее нет
    os.makedirs(output_dir, exist_ok=True)

    # Ищем все файлы в каталоге
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            print(f"Обработка: {filename}...")

            # Открываем PDF документ
            doc = fitz.open(pdf_path)

            # Проходимся по каждой странице
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Настройка качества (масштабирование)
                # zoom = 2.0 увеличивает разрешение (примерно соответствует 144 DPI)
                # Для еще лучшего качества ставьте 3.0 или 4.0
                zoom = 2.0
                mat = fitz.Matrix(zoom, zoom)
                
                # Генерируем изображение страницы
                pix = page.get_pixmap(matrix=mat)

                # Формируем имя для PNG: "название_файла_page_1.png"
                base_name = os.path.splitext(filename)[0]
                out_filename = f"{base_name}_page_{page_num + 1}.png"
                out_path = os.path.join(output_dir, out_filename)

                # Сохраняем изображение
                pix.save(out_path)

            print(f"Успешно: {filename} (страниц: {len(doc)})")

# --- Запуск скрипта ---
# Укажите путь к папке с вашими PDF файлами
input_directory = "C:\\Users\\Timur\\Desktop\\Diplomme\\Code\\evaluation\\M10_CognitiveGap_Explicit"  # Замените на ваш путь
output_directory = "./output_pngs"   # Папка для готовых картинок

# Если нужно тестировать прямо сейчас, просто создайте папку, 
# закиньте туда PDF и раскомментируйте вызов функции ниже:
convert_pdfs_to_png(input_directory, output_directory)