# 🧠 Main brain

import re

from app.agent.memory import ConversationMemory
from app.agent.planner import decide_next_action
from app.agent.tool_registry import execute_tool
from app.audit.audit_logger import log_event

from app.tools.ranking_tools import (
    rank_products,
    recommend_product,
)

from app.tools.revenue_tools import (
    get_cross_sell,
)

from app.tools.cart_tools import (
    create_cart,
)

from app.tools.confirmation_tools import (
    request_payment_confirmation,
)


class CommerceAgent:

    def __init__(self):
        self.memory = ConversationMemory()

    def run(self, user_message):

        # 1. Remember user's message
        self.memory.add("user", user_message)

        # 2. Understand the request
        intent = self._extract_basic_intent(user_message)

        # Audit Trail: Intent detected
        log_event(
            "INTENT_DETECTED",
            f"User request: {user_message} | Intent: {intent}"
        )

        # 3. Decide what to do
        action = decide_next_action(intent)

        # 4. Ask clarification if intent is incomplete
        if action == "ask_clarification":

            response = "Aap kis type ka product dhoondh rahe hain?"

            self.memory.add("assistant", response)

            return {
                "action": action,
                "response": response
            }

        # 5. Check stock
        if action == "check_stock":

            stock = execute_tool(
                "check_stock",
                product_id=intent["product_id"]
            )

            response = (
                f"{intent['product_id']} mein "
                f"{stock} items available hain."
            )

            self.memory.add("assistant", response)

            return {
                "action": action,
                "product_id": intent["product_id"],
                "stock": stock,
                "response": response
            }

        # 6. Get product details
        if action == "get_product_details":

            product = execute_tool(
                "get_product_details",
                product_id=intent["product_id"]
            )

            self.memory.add("assistant", str(product))

            return {
                "action": action,
                "product": product
            }

        # 7. Search → Rank → Recommend → Cross-sell → Cart → Confirmation
        if action == "search_products":

            # Product Retrieval
            products = execute_tool(
                "search_products",
                category=intent["category"],
                max_price=intent.get("max_price")
            )

            # Product Ranking
            ranked_products = rank_products(
                products,
                max_price=intent.get("max_price")
            )

            # Recommendation
            recommended_product = recommend_product(
                ranked_products
            )

            # Revenue Decision / Cross-sell
            cross_sell = get_cross_sell(
                recommended_product
            )

            # Audit: Product selected
            if recommended_product:

                log_event(
                    "PRODUCT_SELECTED",
                    f"{recommended_product['name']} selected",
                    amount=recommended_product["price"]
                )

            # Audit: Cross-sell recommendation
            if cross_sell:

                for item in cross_sell:

                    log_event(
                        "CROSS_SELL_RECOMMENDED",
                        f"{item['name']} recommended because: {item['reason']}",
                        amount=item["price"]
                    )

            # Create Cart
            cart = create_cart(
                recommended_product,
                cross_sell
            )

            # Audit: Cart created
            log_event(
                "CART_CREATED",
                f"Cart created with {len(cart['items'])} items",
                amount=cart["subtotal"]
            )

            # Request user confirmation before payment
            confirmation = request_payment_confirmation(
                cart
            )

            # Audit: Payment confirmation required
            log_event(
                "PAYMENT_CONFIRMATION_REQUIRED",
                confirmation["message"],
                status="pending",
                amount=cart["subtotal"]
            )

            return {
                "action": "recommendation",
                "products": ranked_products,
                "recommended_product": recommended_product,
                "cross_sell": cross_sell,
                "cart": cart,
                "confirmation": confirmation
            }

    def _extract_basic_intent(self, message):

        text = message.lower()

        # --------------------------------
        # Product ID extraction
        # --------------------------------

        product_match = re.search(
            r"shoe-\d+",
            text
        )

        product_id = (
            product_match.group(0)
            if product_match
            else None
        )

        # --------------------------------
        # Stock / availability
        # --------------------------------

        if product_id and (
            "stock" in text
            or "available" in text
            or "availability" in text
        ):

            return {
                "intent": "check_stock",
                "product_id": product_id
            }

        # --------------------------------
        # Product details
        # --------------------------------

        if product_id and (
            "details" in text
            or "detail" in text
            or "information" in text
        ):

            return {
                "intent": "product_details",
                "product_id": product_id
            }

        # --------------------------------
        # Product search
        # --------------------------------

        category = None

        if "running shoe" in text:

            category = "running shoes"

        # --------------------------------
        # Price extraction
        # --------------------------------

        max_price = None

        match = re.search(
            r"(?:under|below|less than|within)\s*[₹rs.]?\s*(\d+)",
            text
        )

        if match:

            max_price = float(match.group(1))

        return {
            "category": category,
            "max_price": max_price
        }