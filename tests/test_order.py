import unittest

from src.domain.order import Order


class OrderTest(unittest.TestCase):
    def test_complete_marks_order_completed(self) -> None:
        order = Order(id="order-123")

        order.complete()

        self.assertEqual("completed", order.status)


if __name__ == "__main__":
    unittest.main()
