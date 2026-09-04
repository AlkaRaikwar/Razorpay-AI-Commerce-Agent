from app.tools.cart_tools import create_cart


product = {
    "id": "shoe-001",
    "name": "ProRun X1",
    "price": 1699
}

cross_sell = [
    {
        "id": "sock-001",
        "name": "RunGrip Socks",
        "price": 299
    }
]

cart = create_cart(
    product,
    cross_sell
)

print(cart)