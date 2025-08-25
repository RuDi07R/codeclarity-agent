# app.py
import streamlit as st
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from chains.vector_chain import get_vector_qa_chain
from chains.graph_chain import get_graph_qa_chain

# --- THIS IS THE FIX ---
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())
# ----------------------

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def vector_rag_node(state):
    print("---ROUTING TO VECTOR RAG NODE---")
    question = state["messages"][-1].content
    vector_chain = get_vector_qa_chain()
    result = vector_chain.invoke({"query": question})
    answer = f"**Answer from Vector Search:**\n\n{result['result']}"
    return {"messages": [HumanMessage(content=answer)]}

def graph_rag_node(state):
    print("---ROUTING TO GRAPH RAG NODE---")
    question = state["messages"][-1].content
    graph_chain = get_graph_qa_chain()
    result = graph_chain.invoke({"query": question})
    answer = f"**Answer from Graph Search:**\n\n{result['result']}"
    return {"messages": [HumanMessage(content=answer)]}

def should_route(state):
    last_message = state["messages"][-1].content.lower()
    if "call" in last_message or "return" in last_message or "relationship" in last_message:
        return "graph_rag"
    else:
        return "vector_rag"

workflow = StateGraph(AgentState)
workflow.add_node("vector_rag", vector_rag_node)
workflow.add_node("graph_rag", graph_rag_node)
workflow.set_conditional_entry_point(
    should_route,
    {"vector_rag": "vector_rag", "graph_rag": "graph_rag"},
)
workflow.add_edge("vector_rag", END)
workflow.add_edge("graph_rag", END)
app = workflow.compile()

st.title("CodeClarity Agent 🤖")
st.markdown("Ask complex questions about the Redux.js codebase!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# This loop is now safe because we won't add None to the list
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- THIS BLOCK IS CORRECTED ---
if prompt := st.chat_input("e.g., What does the createStore function return?"):
    # First, save the user's message to the history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Then, display the user's message on the screen
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            inputs = {"messages": [HumanMessage(content=prompt)]}
            result = app.invoke(inputs)
            response = result["messages"][-1].content
            st.markdown(response)

    # Finally, save the assistant's message to the history
    st.session_state.messages.append({"role": "assistant", "content": response})