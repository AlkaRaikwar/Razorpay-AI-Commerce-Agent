# #  Agent ko kaun-kaun se tools available hain
# Ye actually kar kya raha hai?

# Humne apne individual tools bana diye:

# product_tools.py
#     ├── search_products()
#     └── get_product_details()

# inventory_tools.py
#     └── check_stock()

# Ab Registry un sabko ek central place par register kar raha hai:

#                     TOOL REGISTRY
#                          │
#           ┌──────────────┼──────────────┐
#           ↓              ↓              ↓
#  search_products   get_product_details  check_stock
# Iska benefit ye hai ki Agent ko har tool ki file manually import/manage nahi karni padegi.

from app.tools.product_tools import (
    search_products,
    get_product_details,
)

from app.tools.inventory_tools import (
    check_stock,
)


TOOLS = {
    "search_products": search_products,
    "get_product_details": get_product_details,
    "check_stock": check_stock,
}


def get_tool(tool_name: str):

    return TOOLS.get(tool_name)


def execute_tool(tool_name: str, **kwargs):

    tool = get_tool(tool_name)

    if tool is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    return tool(**kwargs)