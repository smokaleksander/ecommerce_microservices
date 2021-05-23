import enum


class EventType(str, enum.Enum):

    product_created = 'product:created'
    ticker_updated = 'ticket:updated'

    order_created = 'order:created'
    order_cancelled = 'order:cancelled'
