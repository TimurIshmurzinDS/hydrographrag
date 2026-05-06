import time
import logging
import os
import pickle
import uuid
import subprocess
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Импорты твоего ядра
from core.database import HydroDatabase
from core.embeddings import EmbeddingsManager
from agents.identifier import DemandIdentifier
from agents.retriever import GraphRetriever
from planner.generator import SolutionPlanner

MODEL_NAME = "qwen2.5-coder:7b"
CACHE_FILE = "query_cache.pkl"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("GeoGraphAPI")

app_state = {}

def load_query_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_query_cache(cache_dict):
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache_dict, f)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("⏳ Инициализация ядра GeoGraphRAG...")
    app_state['db'] = HydroDatabase()
    app_state['embedder'] = EmbeddingsManager()
    app_state['identifier'] = DemandIdentifier(model_name=MODEL_NAME)
    app_state['retriever'] = GraphRetriever(app_state['db'], app_state['embedder'])
    app_state['planner'] = SolutionPlanner(model_name=MODEL_NAME)
    app_state['query_cache'] = load_query_cache()
    logger.info(f"✅ Система готова! Загружено {len(app_state['query_cache'])} запросов из кэша.")
    yield
    if 'db' in app_state:
        app_state['db'].close()

app = FastAPI(title="GeoGraphRAG API", lifespan=lifespan)

# --- Настройка CORS ---
# Разрешаем запросы со всех источников для локальной разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Схемы данных ---
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    status: str
    query: str
    category: str
    triples_extracted: int
    solution_code: str
    message: str
    map_points: list = []

# --- Основной маршрут с поддержкой слеша и без ---
@app.post("/geo/plan_and_code", response_model=QueryResponse)
@app.post("/geo/plan_and_code/", response_model=QueryResponse)
async def generate_plan_and_code(req: QueryRequest):
    logger.info(f"📥 Запрос: '{req.query}'")
    
    db = app_state['db']
    embedder = app_state['embedder']
    identifier = app_state['identifier']
    retriever = app_state['retriever']
    planner = app_state['planner']
    query_cache = app_state['query_cache']
    
    try:
        # --- PHASE I: Semantic Cache ---
        query_vec = embedder.get_embedding(req.query)
        THRESHOLD = 0.90
        
        for cached_query, data in query_cache.items():
            similarity = embedder.compute_similarity(query_vec, data['vector'])
            if similarity >= THRESHOLD:
                logger.info(f"⚡ [Cache Hit] Найдено совпадение (Сходство: {similarity:.2f})!")
                return QueryResponse(
                    status="success",
                    query=req.query,
                    category=data.get('category', 'CACHED'),
                    triples_extracted=data.get('triples_extracted', 0),
                    solution_code=data['response'],
                    message="Ответ получен из семантического кэша.",
                    map_points=data.get('map_points', [])
                )

        logger.info("[Cache Miss] Запуск полного RAG-пайплайна...")

        # --- PHASE II & III: Demand ID и Графовый поиск ---
        demand = identifier.analyze_query(req.query)
        category = demand.get('category', 'unknown')
        
        triples = retriever.find_solution_subgraph(demand)
        
        if not triples:
            return QueryResponse(
                status="rejected", query=req.query, category=category,
                triples_extracted=0, solution_code="", message="No data found in the graph for this query.",
                map_points=[]
            )

        geo_points = []
        for t in triples:
            if t.get('rel') == 'hasWKT':
                geo_points.append({"name": t['from'], "wkt": t['to']})

        # --- PHASE V: Синтез ответа ---
        api_query_id = f"api_{int(time.time())}"
        result = planner.generate_geographrag_response(req.query, triples, api_query_id)

        # Сохранение лога в GraphDB (Traceability)
        db.save_solution_graph(req.query, triples, MODEL_NAME)
        logger.info("💾 Новый SolutionGraph сохранен в GraphDB.")
        
        # --- СОХРАНЕНИЕ В КЭШ ---
        query_cache[req.query] = {
            'vector': query_vec, 
            'response': result,
            'category': category,
            'triples_extracted': len(triples),
            'map_points': geo_points
        }
        save_query_cache(query_cache)
        
        return QueryResponse(
            status="success",
            query=req.query,
            category=category,
            triples_extracted=len(triples),
            solution_code=result,
            message="Решение успешно сформировано.",
            map_points=geo_points
        )

    except Exception as e:
        logger.error(f"❌ Ошибка: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))