from dataclasses import dataclass

from src.infrastructure.email_sender import EmailSender


@dataclass
class Order:
    id: str
    status: str = "pending"

    def complete(self, email_sender: EmailSender) -> None:
        self.status = "completed"
        email_sender.send_order_completed(self.id)
