import json
import logging
import random
from tqdm import tqdm
from langchain_ollama import ChatOllama
from core.database import HydroDatabase

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class DatasetGenerator:
    def __init__(self, model_name="gemma4:26b"):
        self.db = HydroDatabase()
        # Температура 0.7 для креативности, чтобы OOD вопросы были разнообразными
        self.llm = ChatOllama(model=model_name, temperature=0.7) 
        self.output_file = "ground_truth.json"
        
    def fetch_real_entities(self, limit=100):
        """Вытаскиваем реальные узлы (реки, посты, бассейны) для затравки модели."""
        query = """
        PREFIX hyf: <http://www.opengis.net/ont/hy_features#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wr_kz: <http://smart-water.org/data/WR_KZ/>
        
        SELECT ?name ?type WHERE {
            ?id a ?realType .
            OPTIONAL { ?id wr_kz:Post_name ?postName }
            OPTIONAL { ?id rdfs:label ?label }
            BIND(COALESCE(?postName, ?label) AS ?name)
            BIND(REPLACE(STR(?realType), "^.*[#/](.+)$", "$1") AS ?type)
            FILTER(BOUND(?name) && ?type IN ("HY_HydroFeature", "Post", "Basin"))
        } LIMIT %d
        """ % limit
        
        records = self.db.execute_query(query)
        entities = [f"{r['name']} ({r['type']})" for r in records if r.get('name')]
        return list(set(entities))

    def generate_category_questions(self, category, entities, theme, count=15):
        prompt = f"""
        You are a hydrologist generating a test dataset for an AI system in Kazakhstan.
        Use the following real entities from our database: {', '.join(entities)}.
        
        Generate {count} UNIQUE questions for the category: "{category}".
        
        !!! CRITICAL THEME FOR THIS BATCH: {theme} !!!
        Make sure the questions focus on this specific theme to ensure variety in the dataset.

        RULES FOR EXPECTED ENTITIES:
        - The "expected_entities" list MUST include ALL entities from the provided list that are necessary to answer the question.
        - For "semi-explicit" questions, include both the River and its related Monitoring Posts if they were in the provided list.
        - Ensure names in "expected_entities" match the provided list EXACTLY.

        Rules for categories:
        - "explicit": Direct request for specific data (e.g., "Get water flow for Post X").
        - "semi-explicit": Requires 1 step of logical deduction (e.g., "Find posts on River Y and get their data").
        - "implicit": High-level analytical request (e.g., "Analyze flood risks in Basin Z").
        - "anomalous": Out-of-domain requests (recipes, crypto, space, random python scripts).
        
        Output format must be STRICT VALID JSON:
        [
            {{
                "query": "The generated question in Russian",
                "category": "{category}",
                "expected_entities": ["Full Name 1", "Full Name 2"],
                "expected_behavior": "generate_code" // use "reject" ONLY for anomalous
            }}
        ]
        """
        
        try:
            response = self.llm.invoke(prompt)
            clean_json = response.content.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except Exception as e:
            logging.error(f"Ошибка генерации для {category}: {e}")
            return []

    def run(self):
        logging.info("Извлекаем сущности из графа...")
        # Лимит 100 вытащит все твои реки и посты из базы
        real_entities = self.fetch_real_entities(limit=100) 
        logging.info(f"Извлечено {len(real_entities)} сущностей. Начинаем тематическую генерацию...")

        categories = ["explicit", "semi-explicit", "implicit", "anomalous"]
        
        # Темы для обеспечения разнообразия (чтобы вопросы не повторялись)
        themes = [
            "Current water level monitoring and sensor status",
            "Flooding risks, seasonal discharge, and spring floods",
            "Geographical topology (tributaries, distances, coordinates)",
            "Ecological impact, agriculture, and water consumption",
            "Historical data comparison and prediction modeling"
        ]
        
        full_dataset = []
        target_per_category = 75 # 75 * 4 = 300 вопросов
        batch_size = 15          # По 15 за один раз, чтобы LLM не сломала JSON

        for cat in categories:
            logging.info(f"Генерация вопросов для категории: {cat} (цель: {target_per_category})...")
            cat_questions = []
            
            # Считаем количество необходимых батчей (75 / 15 = 5 проходов)
            num_batches = target_per_category // batch_size
            
            for batch_num in range(num_batches):
                # 1. Берем тему для этого прохода
                current_theme = themes[batch_num % len(themes)]
                
                # 2. Берем небольшую случайную группу рек (до 8 штук), чтобы модель сфокусировалась на них
                sampled_entities = random.sample(real_entities, min(8, len(real_entities)))
                
                logging.info(f"  -> Проход {batch_num + 1}/{num_batches} | Тема: {current_theme}")
                
                questions = self.generate_category_questions(cat, sampled_entities, current_theme, count=batch_size)
                
                if questions:
                    cat_questions.extend(questions)
                else:
                    logging.warning(f"  ⚠️ Пустой ответ в батче {batch_num + 1}, LLM сбоит.")

            full_dataset.extend(cat_questions)

        # Переназначаем ID по порядку
        for i, item in enumerate(full_dataset):
            item['id'] = i + 1

        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(full_dataset, f, ensure_ascii=False, indent=4)
            
        logging.info(f"✅ Масштабный датасет на {len(full_dataset)} уникальных вопросов успешно сохранен в {self.output_file}")

if __name__ == "__main__":
    generator = DatasetGenerator()
    generator.run()