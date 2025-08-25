# build_graph.py
import os
import json
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from langchain_community.graphs import Neo4jGraph
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from config import VECTOR_DB_PATH, EMBEDDING_MODEL, LLM_MODEL

load_dotenv()

def populate_graph_from_vector_db():
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
    )
    graph.query("MATCH (n) DETACH DELETE n")

    vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL)
    )
    
    docs = vector_store.get(include=["documents"])["documents"][:20] 
    print(f"Processing {len(docs)} documents to build the graph...")

    llm = ChatOllama(model=LLM_MODEL)
    
    graph_extraction_prompt = PromptTemplate.from_template(
        """
        From the following code snippet, extract entities (functions, variables, classes) 
        and relationships (e.g., CALLS, IMPORTS, RETURNS, INHERITS_FROM).
        
        Output a JSON object with "nodes" and "relationships" keys.
        Example Node: {{"id": "entity_name", "label": "EntityType"}}
        Example Relationship: {{"source": "source_entity", "target": "target_entity", "type": "RELATIONSHIP_TYPE"}}

        Code:
        {code_chunk}
        """
    )
    
    chain = graph_extraction_prompt | llm

    for i, doc in enumerate(docs):
        print(f"Processing document {i+1}/{len(docs)}...")
        try:
            graph_data_str = chain.invoke({"code_chunk": doc})
            graph_data = json.loads(graph_data_str.content)

            for node in graph_data.get("nodes", []):
                graph.query("MERGE (n:`{label}` {{id: '{id}'}})".format(label=node['label'], id=node['id']))
            
            for rel in graph_data.get("relationships", []):
                graph.query(
                    "MATCH (a {{id: '{source}'}}), (b {{id: '{target}'}}) MERGE (a)-[:`{type}`]->(b)".format(
                        source=rel['source'], target=rel['target'], type=rel['type']
                    )
                )
        except Exception as e:
            print(f"Error processing document: {e}")

    print("Graph population complete.")

if __name__ == "__main__":
    populate_graph_from_vector_db()