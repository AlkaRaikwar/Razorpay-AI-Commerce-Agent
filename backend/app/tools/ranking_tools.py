def rank_products(products, max_price=None):

    if not products:
        return []

    def score(product):

        score = 0

        # Lower price gets preference
        if max_price is not None:
            if product["price"] <= max_price:
                score += 30

        # Stock availability
        if product["stock"] > 0:
            score += 20

        # Better stock gets slight preference
        if product["stock"] >= 10:
            score += 10

        return score

    ranked = sorted(
        products,
        key=score,
        reverse=True
    )

    return ranked

def recommend_product(ranked_products):

    if not ranked_products:
        return None

    return ranked_products[0]    