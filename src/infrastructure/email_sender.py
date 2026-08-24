class EmailSender:
    """Minimal infrastructure service used by the experiment."""

    def __init__(self) -> None:
        self.sent_order_ids: list[str] = []

    def send_order_completed(self, order_id: str) -> None:
        self.sent_order_ids.append(order_id)
