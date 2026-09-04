# User Request
#      ↓
#    plan()
#      ↓
#     Prompt
#      ↓
#    Gemini
#      ↓
#  JSON response
#      ↓
#  json.loads()
#      ↓
#  Python dictionary
# Planner decides which tool should be used

# ab exactly ye ho raha hai 
# User Request
#      ↓
#    plan()
#      ↓
#  ┌───────────────┐
#  │ "stock"?      │──Yes──→ check_stock
#  │ "available"?  │
#  └───────────────┘
#        │ No
#        ↓
#  ┌───────────────┐
#  │ shoe/product? │──Yes──→ search_products
#  └───────────────┘
#        │ No
#        ↓
#     No tool

        #      GEMINI
        # ┌──────────────┐
        # │ Understand   │
        # │ & Decide     │
        # └──────┬───────┘
        #        ↓
        #  Tool selection
        #        ↓
        #   BACKEND TOOL
        # ┌──────────────┐
        # │ Actual data  │
        # │ Actual logic │
        # └──────────────┘

from typing import Dict


def decide_next_action(intent: Dict) -> str:

    if intent.get("product_id") and intent.get("intent") == "check_stock":
        return "check_stock"

    if intent.get("product_id") and intent.get("intent") == "product_details":
        return "get_product_details"

    if intent.get("category"):
        return "search_products"

    return "ask_clarification"