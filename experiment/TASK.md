# Feature Request: Order Completion Email

When an order is completed, send an email notification.

The repository already contains:

- an `Order` domain object with a `complete()` operation,
- an `EmailSender` infrastructure service.

Implement the feature using the existing `EmailSender`.

## Acceptance criteria

- Completing an order changes its status to `completed`.
- Exactly one order-completed email is sent for the completion operation.
- Existing behaviour remains intact.
- Add or update automated tests for the new behaviour.

Do not change unrelated functionality.
