# Razorpay AI Commerce Agent

AI-powered commerce agent built for the Razorpay AI Builder Internship 2026 — Track 1: AI Growth & Agentic Commerce.

The project focuses on helping merchants increase basket value through contextual product recommendations and relevant cross-selling while keeping payment actions user-confirmed, bounded, and auditable.

## Overview

The agent works as a conversational shopping assistant.

A user can describe what they are looking for in natural language, for example:

> I need running shoes under ₹2000

The agent then:

1. Understands the user's product intent and budget.
2. Retrieves matching products.
3. Ranks the available products.
4. Selects a suitable product.
5. Identifies a relevant complementary product for cross-selling.
6. Creates a cart.
7. Shows the final cart amount and asks for user confirmation.
8. Creates a Razorpay Test Mode payment order after confirmation.
9. Verifies the payment signature on the backend.
10. Records important actions in an audit trail.
11. Provides a merchant dashboard for revenue and agent activity.

## Example Flow

### User Request

> I need running shoes under ₹2000

### Available Products

- ProRun X1 — ₹1699
- RunFlex Pro — ₹1899

### Recommended Product

- ProRun X1 — ₹1699

### Relevant Cross-sell

- RunGrip Socks — ₹299

### Cart

```text
ProRun X1       ₹1699
RunGrip Socks    ₹299
----------------------
Total           ₹1998
```

Potential incremental basket value: ₹299.

The cross-sell is presented as a recommendation rather than being silently added to the payment. The user must confirm before the payment flow proceeds.

## Architecture

```text
User
 |
 v
Commerce Agent
 |
 +--> Intent Understanding
 |
 +--> Product Retrieval
 |
 +--> Product Ranking
 |
 +--> Revenue / Cross-sell Decision
 |
 +--> Cart Creation
 |
 +--> User Confirmation
 |
 +--> Razorpay Payment
 |
 +--> Payment Verification
 |
 v
Order Confirmation
 |
 v
Merchant Dashboard

All important actions
        |
        v
   Audit Trail
```

The overall workflow separates conversational reasoning from commerce operations. The agent coordinates the workflow, while backend tools perform product retrieval, inventory checks, ranking, cross-selling, cart calculations, confirmation, and payment-related operations.

## Agent and Tool Architecture

The agent coordinates the workflow through backend tools.

```text
Commerce Agent
      |
      v
   Planner
      |
      v
 Tool Registry
      |
      +-- Product Tools
      +-- Inventory Tools
      +-- Ranking Tools
      +-- Revenue Tools
      +-- Cart Tools
      +-- Confirmation Tools
      +-- Payment Tools
```

The agent is responsible for understanding the user request and coordinating the workflow. Backend tools handle product data, inventory, ranking, cart calculations, revenue decisions, confirmation, and payment operations.

This separation keeps factual commerce data and financial operations outside the LLM.

## Revenue Growth

The main business objective is to increase merchant revenue through relevant recommendations rather than generic product suggestions.

For example:

```text
Original Product
ProRun X1
₹1699

        +

Relevant Cross-sell
RunGrip Socks
₹299

        =

Potential Basket
₹1998
```

In this example, the complementary product creates a potential incremental basket value of ₹299.

The recommendation is based on product relevance. Running socks are a natural complementary product for running shoes, making the cross-sell contextual rather than arbitrary.

## Product Discovery and Ranking

The agent first identifies the user's intent and constraints.

For:

> I need running shoes under ₹2000

the extracted intent is approximately:

```text
Category: running shoes
Maximum price: ₹2000
```

The product tool retrieves products matching these constraints.

The ranking layer then evaluates the available products and selects a suitable recommendation.

This keeps product facts such as price and inventory in backend-controlled data rather than relying on the LLM to invent them.

## Cross-sell Decision

After selecting the primary product, the revenue layer checks whether a relevant complementary product exists.

Example:

```text
Primary Product:
ProRun X1
Category: running shoes

Complementary Product:
RunGrip Socks
Category: running socks
```

The cross-sell recommendation is recorded in the audit trail so that the merchant can see why an additional product was recommended.

## Cart and Confirmation

Once the primary product and optional cross-sell are selected, the agent creates a cart.

Example:

```text
Items:
- ProRun X1
- RunGrip Socks

Subtotal:
₹1998
```

The agent then asks the user for explicit confirmation before proceeding to payment.

Example:

```text
Your cart total is ₹1998.
Do you want to proceed to payment?
```

This prevents the agent from silently initiating a financial action.

## Payment Flow

The payment flow is designed around Razorpay Test Mode.

```text
User Confirmation
       |
       v
Create Razorpay Order
       |
       v
Razorpay Checkout
       |
       v
Payment Attempt
       |
       +---- Failure
       |       |
       |       v
       |   Retry Available
       |
       +---- Success
               |
               v
      Backend Signature Verification
               |
               v
        Order Confirmation
```

The payment order is created server-side.

After checkout, the payment response is verified on the backend using the Razorpay payment signature before the order is marked as confirmed.

The project uses Razorpay Test Mode, so no real money is involved during development and demonstration.

## Audit Trail

Important commerce and payment actions are recorded through an audit logger.

Example events include:

```text
INTENT_DETECTED
PRODUCT_SELECTED
CROSS_SELL_RECOMMENDED
CART_CREATED
PAYMENT_CONFIRMATION_REQUIRED
PAYMENT_ORDER_CREATED
PAYMENT_VERIFIED
ORDER_CONFIRMED
PAYMENT_VERIFICATION_FAILED
```

The audit trail makes the agent's actions inspectable and provides visibility into the sequence of decisions.

This is especially important for financial workflows where actions should be explainable and traceable.

## Merchant Dashboard

The project includes a merchant dashboard that provides visibility into agent activity and revenue-related events.

The dashboard can display:

- Total confirmed revenue
- Revenue associated with cross-sell opportunities
- Revenue uplift
- Agent activity
- Audit events
- Payment and order events

Example:

```text
Merchant Revenue Dashboard

Total Revenue
₹1998

Base Product Revenue
₹1699

Incremental Cross-sell Value
₹299

Potential Uplift
17.6%
```

The dashboard is intended to help merchants understand how the commerce agent contributes to basket growth.

## Guardrails

The system is designed with bounded and user-gated commerce actions.

### 1. User Confirmation

Payment should not proceed without explicit user confirmation.

### 2. Backend-Controlled Commerce Data

Product prices, inventory, cart totals, and payment operations are handled by backend tools rather than being generated by the LLM.

### 3. Explainable Recommendations

Cross-sell recommendations are accompanied by a reason, for example:

```text
Running socks complement running shoes.
```

### 4. Payment Verification

A successful payment is only treated as confirmed after backend verification of the Razorpay payment signature.

### 5. Failure Handling

A failed payment does not mark the order as successful. The user can retry the payment flow.

## Technology Stack

- Python
- FastAPI
- Google Gemini
- Razorpay Test Mode
- HTML / JavaScript
- Python dotenv
- Custom audit logging

## Project Structure

```text
backend/
|
+-- app/
    |
    +-- agent/
    |   |
    |   +-- agent.py
    |   +-- planner.py
    |   +-- memory.py
    |   +-- tool_registry.py
    |
    +-- tools/
    |   |
    |   +-- product_tools.py
    |   +-- inventory_tools.py
    |   +-- ranking_tools.py
    |   +-- revenue_tools.py
    |   +-- cart_tools.py
    |   +-- confirmation_tools.py
    |   +-- payment_tools.py
    |
    +-- integrations/
    |   |
    |   +-- gemini.py
    |
    +-- audit/
        |
        +-- audit_logger.py
```

### Agent Layer

The `agent` package coordinates intent understanding, planning, memory, and tool execution.

### Tools Layer

The `tools` package contains the commerce operations used by the agent.

### Integration Layer

The `integrations` package contains external AI/service integrations such as Gemini.

### Audit Layer

The `audit` package records important actions performed during the commerce workflow.

## How the Agent Works

The simplified execution flow is:

```text
User Message
     |
     v
Intent Extraction
     |
     v
Planner
     |
     v
Tool Selection
     |
     v
Product Search
     |
     v
Product Ranking
     |
     v
Recommendation
     |
     v
Cross-sell Decision
     |
     v
Cart Creation
     |
     v
User Confirmation
     |
     v
Payment
```

The architecture is intentionally tool-driven.

The LLM can assist with language understanding and reasoning, but critical commerce facts and financial actions are handled by deterministic backend logic and tools.

## Local Setup

Clone the repository and move into the backend directory:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd razorpay-ai-commerce-agent/backend
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` directory:

```env
GEMINI_API_KEY=your_gemini_api_key
RAZORPAY_KEY_ID=your_razorpay_test_key
RAZORPAY_KEY_SECRET=your_razorpay_test_secret
```

Run the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Example API Request

The commerce agent can be tested through the `/agent` endpoint.

Example request:

```json
{
  "message": "I need running shoes under ₹2000"
}
```

Example response structure:

```json
{
  "action": "recommendation",
  "recommended_product": {
    "id": "shoe-001",
    "name": "ProRun X1",
    "price": 1699
  },
  "cross_sell": [
    {
      "id": "sock-001",
      "name": "RunGrip Socks",
      "price": 299
    }
  ],
  "cart": {
    "subtotal": 1998
  },
  "confirmation": {
    "confirmed": false,
    "requires_confirmation": true,
    "amount": 1998
  }
}
```

## Build Challenges

### Reliable AI Decision Making

During development, Gemini-based planning and structured JSON generation experienced intermittent network and response-format issues.

To keep commerce operations reliable, deterministic intent extraction and backend tool selection are used as a fallback.

This prevents an unreliable LLM response from directly controlling commerce or financial operations.

### Bounded Financial Actions

Financial actions are separated from conversational reasoning.

The agent coordinates the workflow, while backend tools control cart calculations, confirmation, payment order creation, and payment verification.

### Razorpay Integration

The payment workflow requires server-side order creation and backend payment signature verification.

The project uses Razorpay Test Mode for development and demonstration.

### Payment Failure Handling

A failed payment does not result in an order being marked as successfully paid.

The cart remains available for retry.

## Current Status

Implemented:

- Conversational product intent handling
- Budget-based product search
- Product ranking
- Product recommendation
- Contextual cross-selling
- Cart creation
- User confirmation gate
- Audit logging
- Merchant dashboard
- Razorpay Test Mode payment order flow
- Backend payment signature verification
- Payment failure handling
- Gemini integration

The project is currently focused on demonstrating the core AI commerce and revenue-growth workflow for Razorpay AI Builder Internship 2026 — Track 1.

## Future Improvements

Potential extensions include:

- Persistent product/catalog database
- Real merchant catalog integration
- More advanced semantic product retrieval
- Personalized recommendations using customer history
- LLM-driven conversational intent understanding with structured tool calling
- Multi-product bundles
- Campaign orchestration
- Merchant-level revenue analytics
- Persistent order and payment storage
- Production deployment
- Authentication and role-based access

## Razorpay AI Builder Internship 2026

### Track 1 — AI Growth & Agentic Commerce

This project is built for the Razorpay AI Builder Internship 2026 Track 1 challenge.

The core objective is to demonstrate how an AI commerce agent can:

1. Understand customer intent.
2. Discover and rank relevant products.
3. Increase basket value through contextual cross-selling.
4. Guide the customer through cart and checkout.
5. Keep financial actions user-confirmed and bounded.
6. Provide an auditable record of agent actions.

The project uses Razorpay Test Mode for the payment workflow.

## License

This project is built for educational, internship, and demonstration purposes.