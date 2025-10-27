from fastapi import FastAPI, Request
from langgraph.graph import StateGraph
from utils.search_tools import get_search_results
from utils.llm_factory import get_llm
import os

app = FastAPI(title="AI Coach Backend (LangGraph)")

# === 1️⃣ Environment variables ===
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")
SERPAPI_ENGINE = os.getenv("SERPAPI_ENGINE", "google")

# === 2️⃣ Define Graph Nodes ===

# Node 1: Search node
def search_node(state: dict):
    input_text = state["input_text"]
    print(f"🔍 Searching via {SERPAPI_ENGINE}: {input_text}")
    search_results = get_search_results(input_text, SERPAPI_ENGINE)
    return {"input_text": input_text, "search_results": search_results}

# Node 2: LLM generation node
def llm_node(state: dict):
    input_text = state["input_text"]
    search_results = state["search_results"]
    llm = get_llm(MODEL_PROVIDER)
    prompt = f"""
You are an expert AI Coach.
User asked: {input_text}
Here are search results for context:
{search_results}

Answer clearly and precisely (max 300 words).
"""
    print("🧠 Generating response...")
    response = llm.invoke(prompt).content
    return {"responseText": response}

# === 3️⃣ Build LangGraph workflow ===
graph = StateGraph()

# Add nodes (like n8n blocks)
graph.add_node("search", search_node)
graph.add_node("llm", llm_node)

# Define edges (connections)
graph.add_edge("search", "llm")

# Define the entry point
graph.set_entry_point("search")

# Compile the workflow
compiled_graph = graph.compile()

# === 4️⃣ OpenAI-compatible endpoint ===
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    data = await request.json()
    user_message = data["messages"][-1]["content"]

    # Run the LangGraph flow
    print("🚀 Invoking LangGraph workflow...")
    result = compiled_graph.invoke({"input_text": user_message})

    return {
        "id": "chatcmpl-langgraph",
        "object": "chat.completion",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": result.get("responseText", "No response generated."),
                }
            }
        ],
    }

# === 5️⃣ Health check route ===
@app.get("/")
def root():
    return {"status": "AI Coach Backend (LangGraph) running ✅"}
