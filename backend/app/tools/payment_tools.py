# create_payment_order(), check_payment_status()
# 💳 Razorpay payment tools

import os
import razorpay
from dotenv import load_dotenv

load_dotenv()


RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")


client = razorpay.Client(
    auth=(
        RAZORPAY_KEY_ID,
        RAZORPAY_KEY_SECRET
    )
)


def create_payment_order(
    amount: int,
    currency: str = "INR"
):
    """
    Create a Razorpay Test Mode order.

    amount is provided in rupees.
    Razorpay requires the amount in the smallest currency unit.
    Example: ₹1998 -> 199800 paise.
    """

    amount_in_paise = int(amount * 100)

    order_data = {
        "amount": amount_in_paise,
        "currency": currency,
        "receipt": "receipt_001",
    }

    order = client.order.create(
        data=order_data
    )

    return {
        "order_id": order["id"],
        "amount": amount,
        "amount_in_paise": amount_in_paise,
        "currency": currency,
        "status": order["status"]
    }

def verify_payment_signature(
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
):
    data = {
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "razorpay_signature": razorpay_signature,
    }

    try:
        client.utility.verify_payment_signature(data)
        return True
    except Exception:
        return False    