import os
import uuid
import pandas as pd
from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper, JSON, POST

load_dotenv()

class HydroDatabase:
    """
    Класс для управления доступом к GraphDB (RDF) и табличным данным.
    Реализует концепцию интеграции экспертных знаний и сохранения аудита.
    """
    def __init__(self):
        # Название репозитория в GraphDB
        repo_id = os.getenv("GRAPHDB_REPO", "waterdb")
        self.endpoint = f"http://localhost:7200/repositories/{repo_id}"
        # Для изменения данных (INSERT/DELETE) в GraphDB нужен суффикс /statements
        self.update_endpoint = f"{self.endpoint}/statements"
        
        try:
            self.sparql = SPARQLWrapper(self.endpoint)
            self.sparql_update = SPARQLWrapper(self.update_endpoint)
            print(f"✅ Соединение с GraphDB установлено ({self.endpoint}).")
        except Exception as e:
            print(f"❌ Ошибка подключения к GraphDB: {e}")
            self.sparql = None

    def _load_excel(self):
        if os.path.exists(self.excel_path):
            try:
                self.df = pd.read_excel(self.excel_path, decimal=',')
                self.df['Post_code'] = self.df['Post_code'].astype(str).str.strip()
                print(f"✅ Данные из Excel загружены: {len(self.df)} записей.")
            except Exception as e:
                print(f"❌ Ошибка чтения Excel: {e}")
        else:
            print(f"⚠️ Файл {self.excel_path} не найден.")

    def execute_query(self, query):
        """Выполнение SPARQL-запроса (SELECT) к GraphDB."""
        if not self.sparql: return []
            
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        try:
            results = self.sparql.query().convert()
            formatted_results = []
            for result in results["results"]["bindings"]:
                row = {key: value["value"] for key, value in result.items()}
                formatted_results.append(row)
            return formatted_results
        except Exception as e:
            print(f"❌ Ошибка выполнения SPARQL:\n{e}")
            return []

    def save_solution_graph(self, query_text, triples, model_name):
        """Сохраняет метаданные запроса и прокидывает связи к узлам онтологии."""
        if not self.sparql_update or not triples: return

        query_id = str(uuid.uuid4()).replace("-", "")
        query_uri = f"<http://smart-water.org/log/Query_{query_id}>"

        # Собираем уникальные имена узлов
        nodes_to_link = set()
        for t in triples:
            if len(t['from']) > 1: nodes_to_link.add(t['from'])
            if len(t['to']) > 1: nodes_to_link.add(t['to'])

        if not nodes_to_link: return

        safe_text = query_text.replace('"', '\\"').replace('\n', ' ')
        names_filter = ", ".join([f'"{n}"' for n in nodes_to_link])

        sparql_update = f"""
        PREFIX log: <http://smart-water.org/log/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wr_kz: <http://smart-water.org/data/WR_KZ/>

        INSERT {{
            {query_uri} a log:UserQuery ;
                        log:text "{safe_text}" ;
                        log:model "{model_name}" ;
                        log:utilizedNode ?target .
        }}
        WHERE {{
            ?target rdfs:label|wr_kz:Post_name ?name .
            FILTER(?name IN ({names_filter}))
        }}
        """
        
        self.sparql_update.setQuery(sparql_update)
        self.sparql_update.setMethod(POST)
        try:
            self.sparql_update.query()
            print(f"📝 [GraphDB] Лог запроса сохранен в граф (Traceability).")
        except Exception as e:
            print(f"⚠️ [GraphDB] Ошибка сохранения лога: {e}")

    def clear_solution_graphs(self):
        """Очистка базы от логов перед новым тестом."""
        if not self.sparql_update: return
        sparql_delete = """
        PREFIX log: <http://smart-water.org/log/>
        DELETE { ?q ?p ?o } WHERE { ?q a log:UserQuery ; ?p ?o }
        """
        self.sparql_update.setQuery(sparql_delete)
        self.sparql_update.setMethod(POST)
        try:
            self.sparql_update.query()
            print("🧹 [GraphDB] Логи UserQuery очищены.")
        except Exception:
            pass

    def get_excel_data_by_posts(self, post_ids):
        if self.df is not None:
            return self.df[self.df['Post_code'].isin(post_ids)]
        return pd.DataFrame()

    def close(self):
        pass