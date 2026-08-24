# Architecture

This repository is intentionally small. The architecture exists only to make one dependency rule easy to understand and verify.

## Layers

The codebase contains three conceptual layers:

```text
domain  <-  application  ->  infrastructure
```

### Domain

`src/domain/` contains business state and business behaviour. Domain code should remain independent of delivery mechanisms and external services.

### Application

`src/application/` coordinates use cases. It may work with both domain objects and infrastructure services when orchestration is required.

### Infrastructure

`src/infrastructure/` contains delivery and integration details such as email, persistence, messaging, or external APIs.

## Dependency rule

The rule that matters for this experiment is:

> **Code under `src/domain/` must not import code from `src/infrastructure/`.**

A domain object may expose a state transition such as `Order.complete()`, but it should not know how an email is delivered.

For example, this is a boundary violation:

```python
# src/domain/order.py
from src.infrastructure.email_sender import EmailSender

class Order:
    def complete(self) -> None:
        self.status = "completed"
        EmailSender().send_order_completed(self.id)
```

The feature can work and unit tests can pass while the architecture is still wrong.

A compliant design keeps the domain transition separate from the delivery mechanism. Application code can coordinate the two:

```python
order.complete()
email_sender.send_order_completed(order.id)
```

The exact application API is deliberately not prescribed. The experiment is about whether the documented boundary influences implementation and whether that boundary is verified.
