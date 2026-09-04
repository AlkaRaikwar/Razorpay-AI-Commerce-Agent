from datetime import datetime


AUDIT_LOG = []


def log_event(
    action: str,
    details: str,
    status: str = "success",
    amount: int | None = None,
):
    event = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "action": action,
        "details": details,
        "status": status,
    }

    if amount is not None:
        event["amount"] = amount

    AUDIT_LOG.append(event)

    return event


def get_audit_log():
    return AUDIT_LOG


    # iska o/p
#     {
#     "timestamp": "...",
#     "action": "PRODUCT_SELECTED",
#     "details": "ProRun X1 selected",
#     "status": "success",
#     "amount": 1699
# }