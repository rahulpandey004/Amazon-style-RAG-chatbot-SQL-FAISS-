import json
import ollama

INTENT_PROMPT = """
You are a strict intent classifier for an Amazon-like chatbot.

Classify the user query into EXACTLY ONE of these intents:
- ORDER_STATUS
- PRODUCT_SEARCH
- GENERAL_RAG

Rules (follow strictly):
1. Choose ORDER_STATUS ONLY if the query explicitly mentions:
   - order
   - order id
   - delivery
   - tracking
   - shipment
   AND clearly refers to an ORDER, not a product.

2. Choose PRODUCT_SEARCH if the query is about:
   - laptop specifications
   - battery life
   - RAM, processor, storage, display
   - product features
   - comparing laptops
   - laptop numbers like "laptop 23" or "laptop 69"

3. Numbers alone do NOT mean order ID.
   - Treat numbers as product references unless "order" is explicitly mentioned.

4. Default to PRODUCT_SEARCH for product-related questions.
   Use GENERAL_RAG only for non-product informational questions.

Return ONLY valid JSON in EXACTLY this format:
{{
  "intent": "ORDER_STATUS | PRODUCT_SEARCH | GENERAL_RAG",
  "order_id": null
}}

User query:
{query}
"""

def detect_intent(message: str) -> dict:
    prompt = INTENT_PROMPT.format(query=message)

    response = ollama.generate(
        model="mistral",
        prompt=prompt
    )

    raw = response.get("response", "").strip()

    try:
        # Safely extract JSON even if model adds extra text
        start = raw.find("{")
        end = raw.rfind("}") + 1
        json_text = raw[start:end]

        data = json.loads(json_text)

        # Final guard
        if "intent" not in data:
            raise ValueError("Missing intent")

        return {
            "intent": data.get("intent", "GENERAL_RAG"),
            "order_id": data.get("order_id")
        }

    except Exception:
        # Safe fallback
        return {
            "intent": "GENERAL_RAG",
            "order_id": None
        }
