import ollama
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from router import route_query

LOCAL_MODEL = "llama3.2"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- Schema -----------
class ChatRequest(BaseModel):
    message: str

# ----------- Chat Endpoint -----------
@app.post("/chat")
def chat(req: ChatRequest):
    user_query = req.message

    routed = route_query(user_query)
    print("ROUTED:", routed)

    # -------------------------------
    # ORDER STATUS (SQL ONLY)
    # -------------------------------
    if routed["type"] == "order_status":
        prompt = f"""
You are a helpful Amazon delivery assistant.

User Question:
{user_query}

Order Data:
{routed["data"]}

Give a short, clear delivery status.
"""

    # ------------------------------------------------
    # PRODUCT SPECS USING ORDER ID (SQL → VECTOR)
    # ------------------------------------------------
    elif routed["type"] == "order_product_spec":
        prompt = f"""
You are a product expert assistant.

User Question:
{user_query}

Product Name:
{routed["product_name"]}

Product Specifications:
{routed["data"]}

Answer using ONLY the specifications above.
If something is missing, say you don't know.
"""

    # -------------------------------
    # DIRECT PRODUCT SEARCH (VECTOR)
    # -------------------------------
    elif routed["type"] == "product_search":
        prompt = f"""
You are a product expert assistant.

User Question:
{user_query}

Product Information:
{routed["data"]}

Answer using ONLY the information above.
If not found, say you don't know.
"""

    # -------------------------------
    # ERROR HANDLING
    # -------------------------------
    else:
        prompt = f"""
User Question:
{user_query}

System Message:
{routed.get("data", "Something went wrong.")}

Explain clearly to the user.
"""

    # -------------------------------
    # LLM GENERATION
    # -------------------------------
    try:
        response = ollama.generate(
            model=LOCAL_MODEL,
            prompt=prompt
        )
        reply_text = response["response"]
    except Exception as e:
        reply_text = f"LLM error: {str(e)}"

    return {"reply": reply_text}

# ----------- Serve UI -----------
app.mount(
    "/",
    StaticFiles(directory="../frontend", html=True),
    name="frontend"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
