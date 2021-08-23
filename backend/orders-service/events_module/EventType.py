import enum


class EventType(str, enum.Enum):

    product_created = 'product:created'
    product_updated = 'ticket:updated'

    order_created = 'order:created'
    order_cancelled = 'order:cancelled'
    order_completed = 'order:completed'

    expiration_complete = 'expiration:complete'

    payment_created = 'payment:created'
