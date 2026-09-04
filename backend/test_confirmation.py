from app.tools.confirmation_tools import (
    request_payment_confirmation,
    confirm_payment
)


cart = {
    "items": [
        {
            "id": "shoe-001",
            "name": "ProRun X1",
            "price": 1699,
            "quantity": 1
        },
        {
            "id": "sock-001",
            "name": "RunGrip Socks",
            "price": 299,
            "quantity": 1
        }
    ],
    "subtotal": 1998
}


print("TEST 1:")
print(request_payment_confirmation(cart))

print("\nTEST 2:")
print(confirm_payment("Yes, proceed to payment"))

print("\nTEST 3:")
print(confirm_payment("No"))