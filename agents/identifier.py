import json
import os
from langchain_ollama import ChatOllama

class DemandIdentifier:

    def __init__(self, model_name="gemma4:26b"):
        # Используем температуру 0 для стабильности извлечения данных
        ollama_base_url = os.environ.get(
            "OLLAMA_BASE_URL",
            "http://127.0.0.1:11434",
        )

        self.llm = ChatOllama(
    model=model_name,
    base_url=ollama_base_url,
    temperature=0.0,
    top_p=1.0,
    num_ctx=8192,
    seed=42,
)


    def analyze_query(self, query: str):
        # Мощный промпт с правилами и примерами из Ground Truth датасета
        prompt = f"""
        SYSTEM: You are a strict Geospatial and Hydrology Expert Assistant. 
        Your task is to classify the user's query into EXACTLY ONE of four categories and extract entities.

        CRITICAL RULE FOR ENTITY EXTRACTION:
        Always translate Russian geographical names into their English equivalents for the database search.
        - "река Или" -> "Ili River"
        - "Алматинская область" -> "Almaty Region"
        - "Жетысу" -> "Jetisu Region"
        - "Киши Алматы" -> "Kishi Almaty River"
        Ignore abstract concepts (like area, risk, statistics) in 'extracted_inputs'. Put ONLY the Geographic Entities there.

        CATEGORY RULES:
        1. "explicit": Direct data lookup, prediction, or comparison for EXACTLY named rivers.
        2. "semi-explicit": Topological search. The user names a region or river and asks to find related objects inside/on it.
        3. "implicit": High-level analysis. Requires assessing risks, connectivity, ecological impact, or areas.
        4. "anomalous": Out of domain. Requests about recipes, cryptocurrency, etc.

        EXAMPLES:

        User: "Каков текущий уровень воды в реке Или?"
        Output:
        {{
            "category": "explicit",
            "extracted_inputs": ["Ili River"],
            "target_output": "water level",
            "modeling_logic": "direct lookup"
        }}

        User: "Дай информацию на все реки возле Алматы."
        Output:
        {{
            "category": "semi-explicit",
            "extracted_inputs": ["Almaty City", "Almaty Region"],
            "target_output": "rivers",
            "modeling_logic": "find rivers located in region"
        }}

        User: "Какова общая площадь посевных площадей в регионах, через которые протекает река Или?"
        Output:
        {{
            "category": "implicit",
            "extracted_inputs": ["Ili River"],
            "target_output": "arable land area",
            "modeling_logic": "find regions connected to river and extract area"
        }}

        USER QUERY: "{query}"

        Return ONLY strict JSON.
        """
        try:
            response = self.llm.invoke(prompt)
            # Очистка ответа от возможных markdown-тегов и <think> блоков (если модель reasoning)
            content = response.content
            import re
            content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
            clean_json = content.replace('```json', '').replace('```', '').strip()
            
            return json.loads(clean_json)
        except Exception as e:
            return {
                "category": "error",
                "error_details": str(e),
                "extracted_inputs": [],
                "target_output": "unknown",
                "modeling_logic": "error"
            }
if __name__ == "__main__":
    agent = DemandIdentifier()
    test_query = "Проанализируй риск паводка для реки Или на основе данных постов"
    result = agent.analyze_query(test_query)
    print(json.dumps(result, indent=4, ensure_ascii=False))