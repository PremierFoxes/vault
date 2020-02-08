from enum import Enum


class PaymentStatus(Enum):
    """Enumeration for the payment current_status and target_status fields.

    - :PAYMENT_STATUS_UNKNOWN: unknown payment status.
    - :PAYMENT_STATUS_RECEIVED: the payment has been received and is awaiting
                                requests to process it further.
    - :PAYMENT_STATUS_AWAITING_SETTLEMENT: the settlement of the payment is
                                           currently being processed.
    - :PAYMENT_STATUS_SETTLED: the payment has been finalised and the movement
                               of funds has occurred. No further action on the
                               payment is possible/necessary.
    - :PAYMENT_STATUS_CANCELLED: the payment has been stopped, for example
                                 because the payment could not be validated on
                                 creation or the debtor has insufficient funds.
    - :PAYMENT_STATUS_REJECTED: the payment has been rejected, for example
                                because of account restrictions on the creditor
                                side.
    """

    PAYMENT_STATUS_UNKNOWN = 'PAYMENT_STATUS_UNKNOWN'
    PAYMENT_STATUS_RECEIVED = 'PAYMENT_STATUS_RECEIVED'
    PAYMENT_STATUS_AWAITING_SETTLEMENT = 'PAYMENT_STATUS_AWAITING_SETTLEMENT'
    PAYMENT_STATUS_SETTLED = 'PAYMENT_STATUS_SETTLED'
    PAYMENT_STATUS_CANCELLED = 'PAYMENT_STATUS_CANCELLED'
    PAYMENT_STATUS_REJECTED = 'PAYMENT_STATUS_REJECTED'
