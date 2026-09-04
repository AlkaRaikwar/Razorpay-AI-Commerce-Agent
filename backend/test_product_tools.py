from app.tools.product_tools import search_products, get_product_details

# Test 1: category search
print("TEST 1:")
print(search_products("running shoes"))

# Test 2: category + max price
print("\nTEST 2:")
print(search_products("running shoes", max_price=1800))

# Test 3: product details
print("\nTEST 3:")
print(get_product_details("shoe-001"))