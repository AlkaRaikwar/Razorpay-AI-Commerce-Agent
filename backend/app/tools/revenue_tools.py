def get_cross_sell(product):

    if not product:
        return []

    category = product.get("category", "")

    if "running shoes" in category:

        return [
            {
                "id": "sock-001",
                "name": "RunGrip Socks",
                "price": 299,
                "reason": "Running socks complement running shoes"
            }
        ]

    return []