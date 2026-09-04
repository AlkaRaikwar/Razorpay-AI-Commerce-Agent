# #  Product-related actual actions

# # User
#  ↓
# Agent
#  ↓
# search_products()
#  ↓
# Actual product data

# av  products  hardcoded hain  bad men isi jagah database/API connect kar sakte hain.
# products = [...] 


# gemini.py
#    ↓
# Gemini understands language

# product_tools.py
#    ↓
# Actual product search



# Product-related actual actions

def search_products(
    category: str,
    max_price: int | None = None,
    keyword: str | None = None,
):
    """
    Search products by category, optional maximum price, and optional keyword.
    """

    products = [
        {
            "id": "shoe-001",
            "name": "ProRun X1",
            "category": "running shoes",
            "price": 1699,
            "stock": 20,
            "description": "Lightweight daily running shoe",
        },
        {
            "id": "shoe-002",
            "name": "RunFlex Pro",
            "category": "running shoes",
            "price": 1899,
            "stock": 8,
            "description": "Cushioned running shoe for daily training",
        },
        {
            "id": "sock-001",
            "name": "RunGrip Socks",
            "category": "running socks",
            "price": 299,
            "stock": 50,
            "description": "Breathable running socks",
        },
    ]

    results = []

    for p in products:
        if category.lower() not in p["category"].lower():
            continue

        if max_price is not None and p["price"] > max_price:
            continue

        if keyword and keyword.lower() not in (
            p["name"] + " " + p["description"]
        ).lower():
            continue

        results.append(p)

    return results


def get_product_details(product_id: str):
    """
    Get details of a product using its product ID.
    """

    products = {
        "shoe-001": {
            "id": "shoe-001",
            "name": "ProRun X1",
            "category": "running shoes",
            "price": 1699,
            "stock": 20,
            "description": "Lightweight daily running shoe",
        },
        "shoe-002": {
            "id": "shoe-002",
            "name": "RunFlex Pro",
            "category": "running shoes",
            "price": 1899,
            "stock": 8,
            "description": "Cushioned running shoe for daily training",
        },
    }

    return products.get(product_id)