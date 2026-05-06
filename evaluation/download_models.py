import os
import subprocess

print("⏳ Начинаем загрузку 8 моделей для масштабного Ablation Study (ICCCI 2026)...")
print("⚠️ Внимание: скачивание займет много времени (~150 ГБ)!\n")

models = [
    # --- Генераторы (Великолепная восьмерка) ---
    "qwen2.5-coder:7b",
    "qwen2.5-coder:32b",
    "deepseek-r1:14b",
    "deepseek-r1:32b",
    "llama3.1:8b",
    "gemma2:27b",
    "codestral",
    "mistral-nemo",
    "gemma4:26b",
    # --- Судья ---
    "llama3.3" 
]

for model in models:
    print(f"{'='*50}\n📥 Скачивание модели: {model}\n{'='*50}")
    process = subprocess.run(["ollama", "pull", model])
    
    if process.returncode == 0:
        print(f"✅ Модель {model} успешно загружена!\n")
    else:
        print(f"❌ Ошибка при загрузке {model}. Проверь подключение к интернету.\n")

print("🎉 Все модели загружены! Можно запускать пайплайн.")