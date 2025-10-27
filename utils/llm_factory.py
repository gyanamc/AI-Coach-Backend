import os
from langchain_openai import ChatOpenAI

def get_llm(provider="openai"):
    """Create an LLM object based on provider."""
    if provider == "openai":
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7,
        )
    elif provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model="llama3", temperature=0.7)
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model="claude-3-sonnet", temperature=0.7)
    else:
        raise ValueError(f"Unsupported provider: {provider}")
