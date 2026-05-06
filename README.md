
# 🌊 HydroGraphRAG

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paper](https://img.shields.io/badge/Paper-IEEE_Access-success.svg)](#citation)

**HydroGraphRAG** is an Executable Ontology-Grounded Graph Retrieval-Augmented Generation framework designed for explainable and reliable hydrological analysis. 

Unlike conventional text-based RAG systems, HydroGraphRAG integrates a domain-specific hydrological Knowledge Graph (via GraphDB) with Large Language Models (LLMs) to perform topological graph reasoning. It completely transforms natural language queries into valid geospatial analytical reports, interactive Folium maps, and **executable Python GIS scripts** with strict out-of-domain (OOD) hallucination prevention.

The framework was originally developed and evaluated for water resource monitoring and environmental hazard analysis in the **Ile-Balkhash Basin**.

---

## ✨ Key Features

- **🧠 Cognitive Demand Analysis (CDA):** Agentic intent routing that categorizes queries (Explicit, Semi-explicit, Implicit) and dynamically controls graph traversal depth.
- **🛡️ Hallucination Mitigation (OOD Rejection):** Safely blocks anomalous and non-hydrological queries before execution, preventing spatial hallucinations.
- **🕸️ 5-Phase Ontological Knowledge Retrieval:** Extracts deterministic evidence (entities, topological relations, WKT spatial literals, and environmental thresholds) rather than flat text chunks.
- **🗺️ Spatially-Aware Code Generation:** Synthesizes executable `GeoPandas` and `Folium` Python scripts constrained by fixed templates and graph-derived WKT coordinates.
- **🖥️ Tri-Modal User Interface:** A Streamlit application delivering synchronized outputs: a professional analytical report, interactive geospatial map, and the underlying source code.

---

## 🏗️ Architecture Overview

The system operates across a 5-zone computational pipeline:
1. **Semantic Input & Caching Layer:** Minimizes redundant LLM inference using prompt and embedding caches.
2. **Cognitive Demand Analysis (CDA):** Routes queries to the appropriate graph traversal strategy.
3. **Ontological Knowledge Retrieval (OKR):** Extracts a semantically bounded subgraph from the GraphDB RDF repository.
4. **Solution Synthesis & Code Generation:** A grounded LLM generates the text report and Python GIS code.
5. **Execution, Validation & GUI:** Sandboxed backend execution and Streamlit-based interactive rendering.


---

## 🛠️ Technology Stack

- **Large Language Models:** Compatible with open-weight models (e.g., Qwen2.5-Coder, Llama 3.1, Gemma) via `Ollama`.
- **Knowledge Graph:** RDF/OWL Ontology hosted on `GraphDB`.
- **Backend & GIS:** Python, `GeoPandas`, `Shapely`, `Folium`.
- **Frontend:** `Streamlit`, `streamlit-folium`.

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- GraphDB (Local or Remote instance)
- Ollama (for local LLM inference)

### 1. Clone the repository

git clone https://github.com/TimurIshmurzinDS/hydrographrag.git
cd hydrographrag


### 2. Create a virtual environment and install dependencies

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


### 3. Environment Variables
Create a `.env` file in the root directory and configure your GraphDB and LLM endpoints:
env
GRAPHDB_URL=http://localhost:7200/repositories/Water_KZ_Rules
LLM_ENDPOINT=http://localhost:11434/api/generate
MODEL_NAME=qwen2.5-coder:32b


### 4. Run the Application
Launch the Streamlit interface:

streamlit run app.py


---

## 📸 Screenshots

### Multi-Hop Implicit Reasoning
*Provide a screenshot demonstrating the UI with an implicitly routed query, showing the generated report and map.*


### Out-of-Domain (OOD) Rejection
*Provide a screenshot showing how the system safely rejects an anomalous query without generating fabricated maps.*


---

## 📂 Repository Structure


hydrographrag/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── src/
│   ├── retriever/          # GraphDB SPARQL connection and OKR logic
│   ├── cda_router/         # Cognitive Demand Analysis agent
│   ├── generator/          # LLM prompt templates and code synthesis
│   └── executor/           # Sandboxed Python code validation
├── data/                   # (Ignored in Git) Shapefiles and raw data
└── docs/                   # Architecture diagrams and screenshots


---


