from app.tools.payment_tools import create_payment_order


print("Creating Razorpay Test Order...")

order = create_payment_order(
    amount=1998
)

print("\nRazorpay Order:")
print(order)