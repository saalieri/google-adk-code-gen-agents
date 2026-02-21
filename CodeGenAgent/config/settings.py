from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm("ollama_chat/qwen3:8b")

SEARCH_MODEL = LiteLlm("ollama_chat/qwen3:8b", 
        allowed_openai_params=['web_search_options'], 
        web_search_options={
                "search_context_size": "medium"  
        }
)