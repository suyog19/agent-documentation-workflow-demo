from src.domain.order import Order
from src.infrastructure.email_sender import EmailSender


def complete_order(order: Order, email_sender: EmailSender) -> None:
    order.complete()
    email_sender.send_order_completed(order.id)
