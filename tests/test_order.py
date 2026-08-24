import unittest

from src.application.order_completion import complete_order
from src.domain.order import Order
from src.infrastructure.email_sender import EmailSender


class OrderCompletionTest(unittest.TestCase):
    def test_completing_order_sends_one_email(self) -> None:
        order = Order(id="order-123")
        email_sender = EmailSender()

        complete_order(order, email_sender)

        self.assertEqual("completed", order.status)
        self.assertEqual(["order-123"], email_sender.sent_order_ids)


if __name__ == "__main__":
    unittest.main()
