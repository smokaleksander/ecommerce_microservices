import enum


class OrderStatus(enum.Enum):

    created = 'created'
    cancelled = 'cancelled'
    awaiting_payment = 'awaiting_payment'
    complete = 'complete'
