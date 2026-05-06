import os
import pickle
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingsManager:
    """
    Управляет генерацией и кэшированием эмбеддингов для ускорения Dense Graph Extraction.
    Оптимизировано для работы с GPU (RTX 5070).
    """
    def __init__(self, model_name="BAAI/bge-m3", cache_path="embeddings_cache.pkl"):
        print(f"🚀 Загрузка модели эмбеддингов: {model_name}...")
        
        # Автоматический выбор устройства (GPU если есть)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device=self.device)
        
        self.cache_path = cache_path
        self.entity_cache = {}
        
        # Загружаем существующий кэш, если он есть
        if os.path.exists(self.cache_path):
            print(f"📦 Загрузка закэшированных векторов из {self.cache_path}...")
            with open(self.cache_path, 'rb') as f:
                self.entity_cache = pickle.load(f)
            print(f"✅ Загружено векторов: {len(self.entity_cache)}")

    def get_embedding(self, text: str):
        """Превращает строку в вектор с обработкой пустых значений."""
        if not text or not isinstance(text, str) or text.strip() == "":
            return np.zeros(self.model.get_sentence_embedding_dimension())
        
        # encode возвращает numpy array по умолчанию
        return self.model.encode([text], show_progress_bar=False)[0]

    def compute_similarity(self, query_vec, entity_vec):
        """Косинусное сходство между векторами."""
        q = query_vec.reshape(1, -1)
        e = entity_vec.reshape(1, -1)
        return cosine_similarity(q, e)[0][0]

    def find_top_matches(self, query_text, entities_list, top_k=5):
        if not query_text: return []
        
        query_vec = self.get_embedding(query_text)
        
        # 1. Собираем все узлы, которых еще нет в кэше
        missing_entities = []
        for entity in entities_list:
            eid = entity['id']
            name = entity.get('name')
            if eid not in self.entity_cache and name and isinstance(name, str):
                missing_entities.append((eid, name))

        # 2. ПАКЕТНАЯ ОБРАБОТКА (Вот здесь магия RTX 5070)
        if missing_entities:
            print(f"⚡ Пакетное вычисление векторов для {len(missing_entities)} узлов (это быстро)...")
            texts_to_encode = [item[1] for item in missing_entities]
            
            # encode сам разобьет на батчи и загрузит GPU на 100%
            embeddings = self.model.encode(texts_to_encode, batch_size=256, show_progress_bar=True)
            
            for (eid, _), emb in zip(missing_entities, embeddings):
                self.entity_cache[eid] = emb
                
            print(f"💾 Сохранение кэша на диск...")
            with open(self.cache_path, 'wb') as f:
                pickle.dump(self.entity_cache, f)

        # 3. Считаем сходство (векторы уже в памяти)
        scores = []
        for entity in entities_list:
            eid = entity['id']
            if eid in self.entity_cache:
                score = self.compute_similarity(query_vec, self.entity_cache[eid])
                scores.append((entity, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def get_cache_size(self):
        return len(self.entity_cache)