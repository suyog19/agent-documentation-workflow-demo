from dataclasses import dataclass


@dataclass
class Order:
    id: str
    status: str = "pending"

    def complete(self) -> None:
        self.status = "completed"
