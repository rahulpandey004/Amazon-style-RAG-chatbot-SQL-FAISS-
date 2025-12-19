from intent import detect_intent
from sql import get_order_by_id
from rag import rag_search


def route_query(message: str):
    intent_data = detect_intent(message)

    intent = intent_data.get("intent", "GENERAL_RAG")
    order_id = intent_data.get("order_id")

    # ----------------------------------
    # ORDER-BASED QUERIES
    # ----------------------------------
    if intent == "ORDER_STATUS" and order_id:
        order = get_order_by_id(order_id)

        if not order:
            return {
                "type": "error",
                "data": f"No order found for order id {order_id}"
            }

        product_name = order.get("item")

        # 🔥 IMPORTANT: check if user asked for specs/details
        wants_specs = any(
            kw in message.lower()
            for kw in ["spec", "specification","specifications", "details", "configuration"]
        )
        print(wants_specs, product_name)
        if wants_specs and product_name:
            specs = rag_search(
                query=f"all specifications/details of {product_name}",
                product_name=product_name
            )

            return {
                "type": "order_product_spec",
                "order_id": order_id,
                "product_name": product_name,
                "data": specs
            }

        # Default: normal order status response
        return {
            "type": "order_status",
            "data": order
        }

    # ----------------------------------
    # Direct product search (no order)
    # ----------------------------------
    specs = rag_search(query=message)

    return {
        "type": "product_search",
        "data": specs
    }
