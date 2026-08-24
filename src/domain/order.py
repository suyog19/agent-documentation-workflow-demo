from dataclasses import dataclass


@dataclass
class Order:
    id: str
    status: str = "pending"

    def complete(self) -> None:
        """Mark this order as completed."""
        self.status = "completed"
