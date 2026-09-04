# add_to_cart(), get_cart(), calculate_total()
# 🛒 Cart tools

def create_cart(product, cross_sell=None):

    if not product:
        return {
            "items": [],
            "subtotal": 0
        }

    items = [
        {
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": 1
        }
    ]

    # Add cross-sell item only if available
    if cross_sell:
        for item in cross_sell:
            items.append({
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "quantity": 1
            })

    subtotal = sum(
        item["price"] * item["quantity"]
        for item in items
    )

    return {
        "items": items,
        "subtotal": subtotal
    }