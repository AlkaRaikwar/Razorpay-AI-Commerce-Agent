# Stock-related actual actions
# target   ---> User: "Is ProRun X1 available?"

# Agent
#  ↓
# inventory tool
#  ↓
# check_stock("shoe-001")
#  ↓
# 20 units available
# Inventory-related actual actions
# its logic 
#  check_stock("shoe-001")
#         ↓
# inventory dictionary
#         ↓
# "shoe-001" → 20
#         ↓
# return 20


def check_stock(product_id: str):
    """
    Check the available stock for a product.
    """

    inventory = {
        "shoe-001": 20,
        "shoe-002": 8,
        "sock-001": 50,
    }

    return inventory.get(product_id, 0)