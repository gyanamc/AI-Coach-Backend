from fastapi import FastAPI, Request
from langgraph.graph import Graph
from utils.search_tools import get_search_results
from utils.llm_factory import get_llm
import os

app = FastAPI(title="AI Coach Backend")

# === Environment variables ===
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")
SERPAPI_ENGINE = os.getenv("SERPAPI_ENGINE", "google")

# === LangGraph Setup ===
graph = Graph()

# Node 1: Search
def search_node(input_text):
    print(f"🔍 Searching via {SERPAPI_ENGINE}: {input_text}")
    return {"search_results": get_search_results(input_text, SERPAPI_ENGINE)}

# Node 2: LLM
def llm_node(input_text, search_results):
    llm = get_llm(MODEL_PROVIDER)
    prompt = f"""
You are an expert AI Coach.
User asked: {input_text}
Here are search results for context:
{search_results}

Answer clearly and precisely (max 300 words).
"""
    print("🧠 Generating response...")
    answer = llm.invoke(prompt).content
    return {"responseText": answer}

# Connect nodes
graph.add_node("search", search_node)
graph.add_node("llm", llm_node)
graph.add_edge("search", "llm")
graph.set_entry_point("search")

# === OpenAI-compatible endpoint ===
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    data = await request.json()
    user_message = data["messages"][-1]["content"]
    result = graph.invoke({"input_text": user_message})
    return {
        "id": "chatcmpl-langgraph",
        "object": "chat.completion",
        "choices": [
            {"message": {"role": "assistant", "content": result["llm"]["responseText"]}}
        ],
    }

@app.get("/")
def root():
    return {"status": "AI Coach Backend (LangGraph) running ✅"}
