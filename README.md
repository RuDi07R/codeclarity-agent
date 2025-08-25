# codeclarity-agent

🌟 Overview
CodeClarity Agent is an advanced AI-powered assistant designed to help developers and data teams navigate complex codebases through natural language conversations. The agent transforms unstructured source code into a structured knowledge base, combining semantic search with relational insights to provide accurate and context-aware answers to technical questions.

This project demonstrates expertise in Advanced RAG, Multi-Agent Systems, and AI-native development, making it a powerful tool for turning data chaos into clarity.

✨ Key Features
Hybrid Retrieval-Augmented Generation (RAG): Integrates a vector database (ChromaDB) for semantic search with a graph database (Neo4j) for structural analysis of code relationships.

Multi-Agent Orchestration: Utilizes LangGraph to build a sophisticated agentic system that intelligently routes user queries to the appropriate retrieval tool for optimal results.

Model Agnostic Architecture: Supports both cloud-based APIs (OpenAI, Google Gemini) and locally-hosted open-source models (Ollama) to provide flexibility and cost-effectiveness.

Developer-Focused UI: An intuitive web interface built with Streamlit for real-time conversational Q&A and transparent source document viewing.

End-to-End Workflow: The project includes a full pipeline for data ingestion, graph building, and live application deployment.

⚙️ Architecture
The system is built on a modular architecture that separates data processing from the agent's core logic.

Data Ingestion: Source code is loaded, chunked, and converted into embeddings stored in a vector database.

Graph Building: An LLM processes code chunks to extract entities (functions, classes) and relationships (calls, inheritance), populating a graph database.

Agentic Workflow: The LangGraph agent receives a query, routes it to either the vector or graph retrieval tool, synthesizes a response, and returns the answer to the user via the Streamlit UI.

🚀 Getting Started
Prerequisites
Python 3.10 or higher

Git

Ollama

Neo4j AuraDB account (for the graph component)

Installation
Clone the repository:

Bash

git clone https://github.com/RuDi07R/codeclarity-agent.git
Bash

cd codeclarity-agent
Create and activate a virtual environment:

Bash

python -m venv venv
Bash

venv\Scripts\activate
Install the required packages:

Bash

pip install -r requirements.txt
Configuration
Set up your local Ollama server by downloading the required models:

Bash

# Download the chat model
ollama run tinyllama
Bash

# Download the embedding model
ollama run nomic-embed-text
Create a .env file for your Neo4j credentials.

NEO4J_URI="neo4j+s://xxxxxxxx.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="YourSecretPassword"
Running the Project
Run the Ollama server in a separate command prompt:

Bash

ollama run tinyllama
Run the data preparation scripts in your project's terminal:

Bash

python ingest_data.py
Bash

python build_graph.py
Launch the application:

Bash

streamlit run app.py
🧠 Usage Examples
"What is Flask's request context and how is it used?"

"Show me all the functions that the Flask class calls."

"Explain the purpose of the _app_ctx_stack variable."

🛠️ Technologies Used
Language: Python

LLMs: Ollama (TinyLlama), OpenAI (GPT-3.5)

Frameworks: LangChain, LangGraph, Streamlit

Databases: ChromaDB, Neo4j

Tools: Git, Ollama

🤝 Contribution
Contributions are welcome! If you have suggestions or improvements, please submit a pull request.

📄 License
This project is licensed under the MIT License.
