# Architecture

The sample uses three conceptual layers:

```text
domain  <-  application  ->  infrastructure
```

## Domain

`src/domain/` contains business state and behaviour. Domain code should remain independent of delivery mechanisms and external services.

## Application

`src/application/` coordinates use cases. It may work with both domain objects and infrastructure services when orchestration is required.

## Infrastructure

`src/infrastructure/` contains delivery and integration details such as email, persistence, messaging, or external APIs.

## Dependency rule

> **Code under `src/domain/` must not import code from `src/infrastructure/`.**

An `Order` may know how to transition to `completed`, but it should not know how an email is delivered. Application code may coordinate the state transition with an email adapter.
