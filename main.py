import json
import os
import pickle
from core.database import HydroDatabase
from core.embeddings import EmbeddingsManager
from agents.identifier import DemandIdentifier
from agents.retriever import GraphRetriever
from planner.generator import SolutionPlanner

CACHE_FILE = "query_cache.pkl"
MODEL_NAME = "gemma4:26b" # Поменяй на ту модель, что у тебя установлена

def load_query_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_query_cache(cache_dict):
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache_dict, f)

def main():
    print("\n⏳ Инициализация ядра GeoGraphRAG...")
    db = HydroDatabase()
    embedder = EmbeddingsManager()
    identifier = DemandIdentifier(model_name=MODEL_NAME)
    retriever = GraphRetriever(db, embedder)
    planner = SolutionPlanner(model_name=MODEL_NAME)
    
    query_cache = load_query_cache()

    print("\n" + "="*50)
    print("🌊 Система GeoGraphRAG (GraphDB Edition) готова!")
    print("="*50)
    
    query = input("\nВведите ваш запрос по гидрологии: ")
    query_vec = embedder.get_embedding(query)

    # --- PHASE I: Semantic Cache ---
    THRESHOLD = 0.90 # Порог сходства из статьи
    for cached_query, data in query_cache.items():
        similarity = embedder.compute_similarity(query_vec, data['vector'])
        if similarity >= THRESHOLD:
            print(f"\n⚡ [Phase I: Cache Hit] Найден похожий запрос (Сходство: {similarity:.2f})!")
            print(f"Похожий запрос: '{cached_query}'")
            print("Байпас LLM и GraphDB. Мгновенный возврат решения...\n")
            print("="*50)
            print(data['response'])
            db.close()
            return

    print("\n[Phase I: Cache Miss] Запрос новый. Запуск полного пайплайна...")

    # --- PHASE II & III: Demand ID и Графовый поиск ---
    demand = identifier.analyze_query(query)
    print(f"\n🧠 [Агент-Аналитик] Категория: {demand.get('category', 'unknown').upper()}")
    
    print("\n🔍 [Graph Retriever] Обращение к GraphDB (SPARQL)...")
    triples = retriever.find_solution_subgraph(demand)
    
    # --- PHASE IV: Semantic Fallback ---
    if not triples:
        print("❌ [Semantic Fallback] Подходящие связи не найдены. Отказ (Context Rejected).")
        db.close()
        return

    print(f"✅ [Graph Retriever] Извлечено связей (триплетов): {len(triples)}")

    # --- PHASE V: Decision Planning ---
    print("\n⚙️  [Агент-Генератор] Синтез Python-кода...")
    result = planner.generate_response(query, triples)
    
    # Сохраняем граф аудита в базу (Traceability)
    db.save_solution_graph(query, triples, MODEL_NAME)

    # Сохраняем результат в кэш для будущих запросов
    query_cache[query] = {'vector': query_vec, 'response': result}
    save_query_cache(query_cache)

    print("\n" + "="*50)
    print("🚀 ФИНАЛЬНОЕ РЕШЕНИЕ:")
    print("="*50)
    print(result)

    db.close()

if __name__ == "__main__":
    main()