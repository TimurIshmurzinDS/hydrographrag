import json
from langchain_ollama import ChatOllama

class DemandIdentifier:
    """
    Интеллектуальный агент для разбора естественно-языковых запросов.
    Основан на методологии идентификации трех категорий требований.
    """
    def __init__(self, model_name="gemma4:26b"):
        # Используем температуру 0 для стабильности извлечения данных
        self.llm = ChatOllama(model=model_name, temperature=0)

    def analyze_query(self, query: str):
        # Промпт составлен на основе логики категорий из статьи [cite: 217, 257]
        prompt = f"""
        SYSTEM: You are a Geospatial Expert Assistant. 
        Analyze the user's modeling demand.

        RULES:
        - Category "explicit": User asks for a specific parameter for a specific object (e.g., "Water level in River X").
        - Category "semi-explicit": User asks for data but doesn't name the source, or asks to find objects (e.g., "Find all posts on River X").
        - Category "implicit": High-level analysis, risks, or forecasts (e.g., "Analyze flood risks").
        - Category "anomalous": User asks for non-existent entities, impossible physics, or irrelevant topics (e.g., "Atlantis river", "Calculate flow on Mars").

        USER QUERY: "{query}"

        OUTPUT FORMAT (STRICT JSON):
        {{
            "category": "explicit/semi-explicit/implicit",
            "extracted_inputs": ["list", "of", "entities"],
            "target_output": "entity",
            "modeling_logic": "steps"
        }}
        """
        try:
            response = self.llm.invoke(prompt)
            # Очистка ответа от возможных markdown-тегов
            clean_json = response.content.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except Exception as e:
            return {
                "category": "error",
                "error_details": str(e),
                "inputs": [],
                "target_output": "unknown"
            }
if __name__ == "__main__":
    agent = DemandIdentifier()
    test_query = "Проанализируй риск паводка для реки Или на основе данных постов"
    result = agent.analyze_query(test_query)
    print(json.dumps(result, indent=4, ensure_ascii=False))