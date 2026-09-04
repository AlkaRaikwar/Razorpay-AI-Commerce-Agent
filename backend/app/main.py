from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.agent.agent import CommerceAgent

from app.tools.payment_tools import (
    create_payment_order,
    verify_payment_signature,
)

from app.audit.audit_logger import (
    log_event,
    get_audit_log,
)


app = FastAPI(
    title="Razorpay AI Commerce Agent",
    version="0.1.0",
)

agent = CommerceAgent()


# Store demo order information in memory
DEMO_ORDERS = {}


class AgentRequest(BaseModel):
    message: str


class PaymentVerificationRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


@app.get("/")
def root():
    return {
        "message": "Razorpay AI Commerce Agent API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/agent")
def run_agent(request: AgentRequest):

    result = agent.run(request.message)

    return result


@app.post("/create-payment-order")
def create_order():
    """
    Create Razorpay order for the demo cart.
    Payment is only initiated after user confirmation.
    """

    cart_total = 1998

    order = create_payment_order(
        amount=cart_total
    )

    # Store the original server-created order
    DEMO_ORDERS[order["order_id"]] = {
        "amount": cart_total,
        "status": "created",
    }

    # Audit Trail
    log_event(
        "PAYMENT_ORDER_CREATED",
        f"Razorpay order created: {order['order_id']}",
        status="success",
        amount=cart_total,
    )

    return order


@app.get("/checkout", response_class=HTMLResponse)
def checkout():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>AI Commerce Checkout</title>

        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>

        <style>

            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 60px auto;
                padding: 20px;
            }

            .card {
                border: 1px solid #ddd;
                border-radius: 12px;
                padding: 25px;
            }

            button {
                padding: 12px 20px;
                font-size: 16px;
                cursor: pointer;
            }

        </style>

    </head>

    <body>

        <div class="card">

            <h1>AI Commerce Agent</h1>

            <h2>Your Cart</h2>

            <p>ProRun X1 — ₹1699</p>

            <p>RunGrip Socks — ₹299</p>

            <hr>

            <h2>Total: ₹1998</h2>

            <p>
                AI Agent recommended the socks as a relevant
                running accessory.
            </p>

            <p>
                <strong>User confirmation received.</strong>
            </p>

            <button onclick="startPayment()">
                Confirm & Pay ₹1998
            </button>

        </div>


        <script>

            async function startPayment() {

                // 1. Ask backend to create a Razorpay order

                const response = await fetch(
                    "/create-payment-order",
                    {
                        method: "POST"
                    }
                );

                if (!response.ok) {

                    alert(
                        "Unable to create payment order."
                    );

                    return;
                }

                const order = await response.json();


                // 2. Open Razorpay Checkout

                const options = {

                    key: "rzp_test_TY0HkPuqUUdq60",

                    amount: order.amount_in_paise,

                    currency: order.currency,

                    name: "AI Commerce Agent",

                    description: "AI recommended commerce order",

                    order_id: order.order_id,


                    handler: async function(response) {

                        const verificationResponse =
                            await fetch(
                                "/verify-payment",
                                {
                                    method: "POST",

                                    headers: {
                                        "Content-Type":
                                            "application/json"
                                    },

                                    body: JSON.stringify({

                                        razorpay_order_id:
                                            response.razorpay_order_id,

                                        razorpay_payment_id:
                                            response.razorpay_payment_id,

                                        razorpay_signature:
                                            response.razorpay_signature

                                    })
                                }
                            );


                        const result =
                            await verificationResponse.json();


                        if (verificationResponse.ok) {

                            alert(
                                "Payment verified successfully! " +
                                "Order confirmed. " +
                                "Payment ID: " +
                                response.razorpay_payment_id
                            );

                        } else {

                            alert(
                                "Payment verification failed. " +
                                result.detail
                            );
                        }

                    },


                    theme: {
                        color: "#3399cc"
                    }

                };


                const rzp =
                    new Razorpay(options);


                // Handle checkout failure

                rzp.on(
                    "payment.failed",
                    function(response) {

                        console.log(
                            "Payment failed:",
                            response.error
                        );

                        alert(
                            "Payment failed. " +
                            "Your cart is still available for retry."
                        );

                    }
                );


                rzp.open();

            }

        </script>

    </body>

    </html>
    """


@app.post("/verify-payment")
def verify_payment(
    data: PaymentVerificationRequest
):

    # Check whether this order was actually
    # created by our backend

    stored_order = DEMO_ORDERS.get(
        data.razorpay_order_id
    )

    if not stored_order:

        log_event(
            "PAYMENT_VERIFICATION_FAILED",
            "Unknown Razorpay order ID",
            status="failed",
        )

        raise HTTPException(
            status_code=400,
            detail="Unknown payment order."
        )


    # Verify Razorpay signature

    is_valid = verify_payment_signature(
        razorpay_order_id=data.razorpay_order_id,
        razorpay_payment_id=data.razorpay_payment_id,
        razorpay_signature=data.razorpay_signature,
    )


    if not is_valid:

        stored_order["status"] = "verification_failed"

        log_event(
            "PAYMENT_VERIFICATION_FAILED",
            f"Signature verification failed for order {data.razorpay_order_id}",
            status="failed",
            amount=stored_order["amount"],
        )

        raise HTTPException(
            status_code=400,
            detail="Payment verification failed."
        )


    # Payment successfully verified

    stored_order["status"] = "paid"

    log_event(
        "PAYMENT_VERIFIED",
        f"Payment verified: {data.razorpay_payment_id}",
        status="success",
        amount=stored_order["amount"],
    )


    # Order confirmed

    log_event(
        "ORDER_CONFIRMED",
        f"Order confirmed for Razorpay order {data.razorpay_order_id}",
        status="success",
        amount=stored_order["amount"],
    )


    return {

        "success": True,

        "order_confirmed": True,

        "message":
            "Payment verified successfully. "
            "Order confirmed.",

        "payment_id":
            data.razorpay_payment_id,

        "order_id":
            data.razorpay_order_id,

    }


# =========================================================
# MERCHANT DASHBOARD
# =========================================================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    audit_log = get_audit_log()

    total_revenue = 0
    incremental_revenue = 0
    orders = 0


    for event in audit_log:

        if event["action"] == "ORDER_CONFIRMED":

            orders += 1

            if event.get("amount"):
                total_revenue += event["amount"]


        if event["action"] == "CROSS_SELL_RECOMMENDED":

            if event.get("amount"):
                incremental_revenue += event["amount"]


    base_revenue = (
        total_revenue - incremental_revenue
    )


    if base_revenue > 0:

        revenue_uplift = (
            incremental_revenue /
            base_revenue
        ) * 100

    else:

        revenue_uplift = 0


    # Build audit trail HTML

    audit_html = ""

    for event in audit_log:

        audit_html += f"""
        <div class="event">

            <strong>
                {event["action"]}
            </strong>

            <br>

            {event["details"]}

            <br>

            <small>
                {event["timestamp"]}
            </small>

            <span class="{event["status"]}">
                — {event["status"]}
            </span>

        </div>
        """


    if not audit_html:

        audit_html = "<p>No agent activity yet.</p>"


    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Merchant Dashboard</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                max-width: 1000px;
                margin: 40px auto;
                padding: 20px;
                background: #f7f7f7;
            }}

            h1 {{
                margin-bottom: 30px;
            }}

            .cards {{
                display: grid;
                grid-template-columns:
                    repeat(4, 1fr);
                gap: 15px;
            }}

            .card {{
                background: white;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #ddd;
            }}

            .value {{
                font-size: 28px;
                font-weight: bold;
                margin-top: 10px;
            }}

            .audit {{
                background: white;
                margin-top: 30px;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #ddd;
            }}

            .event {{
                padding: 12px 0;
                border-bottom: 1px solid #eee;
            }}

            .success {{
                color: green;
            }}

            .pending {{
                color: orange;
            }}

            .failed {{
                color: red;
            }}

        </style>

    </head>


    <body>

        <h1>Merchant Revenue Dashboard</h1>


        <div class="cards">

            <div class="card">

                <div>Total Orders</div>

                <div class="value">
                    {orders}
                </div>

            </div>


            <div class="card">

                <div>Total Revenue</div>

                <div class="value">
                    ₹{total_revenue}
                </div>

            </div>


            <div class="card">

                <div>AI Cross-sell Revenue</div>

                <div class="value">
                    ₹{incremental_revenue}
                </div>

            </div>


            <div class="card">

                <div>Revenue Uplift</div>

                <div class="value">
                    {revenue_uplift:.1f}%
                </div>

            </div>

        </div>


        <div class="audit">

            <h2>Agent Audit Trail</h2>

            {audit_html}

        </div>


    </body>

    </html>
    """