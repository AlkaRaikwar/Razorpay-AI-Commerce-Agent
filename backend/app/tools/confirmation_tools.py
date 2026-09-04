# 🔐 User confirmation tools

def request_payment_confirmation(cart):

    if not cart or not cart.get("items"):
        return {
            "confirmed": False,
            "message": "Cart is empty."
        }

    total = cart["subtotal"]

    return {
        "confirmed": False,
        "requires_confirmation": True,
        "amount": total,
        "message": (
            f"Your cart total is ₹{total}. "
            "Do you want to proceed to payment?"
        )
    }


def confirm_payment(user_response):

    text = user_response.lower().strip()

    confirmation_words = [
        "yes",
        "confirm",
        "confirmed",
        "proceed",
        "pay",
        "haan",
        "ha",
        "kar do",
        "payment karo"
    ]

    return any(
        word in text
        for word in confirmation_words
    )