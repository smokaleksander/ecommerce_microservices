import enum


class OrderStatus(str, enum.Enum):

    created = 'created'  # product in cartx
    cancelled = 'cancelled'
    awaiting_payment = 'awaiting_payment'
    complete = 'complete'
