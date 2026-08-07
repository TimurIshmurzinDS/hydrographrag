import os
import subprocess

print("⏳ Начинаем загрузку 8 моделей для масштабного Ablation Study (ICCCI 2026)...")
print("⚠️ Внимание: скачивание займет много времени (~150 ГБ)!\n")

models = [
    # --- Lightweight code-oriented models ---
    "qwen2.5-coder:7b",
    "llama3.1:8b",
    
    # --- Medium generalist reasoning model ---
    "mistral-nemo",
    
    # --- Heavyweight structured reasoning models ---
    "codestral",
    "gemma2:27b",
    "gemma4:31b",
    "qwen2.5-coder:32b",
    
    # --- Judge ---
    "qwen2.5:72b-instruct"
]

for model in models:
    print(f"{'='*50}\n📥 Скачивание модели: {model}\n{'='*50}")
    process = subprocess.run(["ollama", "pull", model])
    
    if process.returncode == 0:
        print(f"✅ Модель {model} успешно загружена!\n")
    else:
        print(f"❌ Ошибка при загрузке {model}. Проверь подключение к интернету.\n")

print("🎉 Все модели загружены! Можно запускать пайплайн.")