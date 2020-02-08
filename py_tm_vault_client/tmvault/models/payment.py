from datetime import datetime
from typing import Dict, Any

from .subsidiary import Party
from ..utils import datetime_from_timestamp_iso_string
from ..enums import PaymentStatus


class Payment:
    r"""A payment object.

    :ivar id\_: Globally unique ID for the payment.
    :vartype id\_: str
    :ivar amount: The payment amount value in string format, as an unsigned
                  number with optional floating point and arbitrary precision.
                  Valid examples: <100>, <0.1>, <5.99>, <0.23422>.
    :vartype amount: str
    :ivar currency: The denomination of the amount, e.g. GBP, EUR.
    :vartype currency: str
    :ivar reference: The reference of this payment. Max length 18 chars.
    :vartype reference: str
    :ivar current_status: The current status of the payment.
    :vartype current_status: :class:`tmvault.enums.PaymentStatus`
    :ivar status_reason: The reason for the current_status of the payment.
                         Indicates why a payment was rejected or cancelled.
    :vartype status_reason: str
    :ivar target_status: The target status of the payment, set to trigger
                         payment processing and financial operations, e.g.
                         PAYMENT_STATUS_SETTLED.
    :vartype target_status: str
    :ivar debtor_party: The details of the party sending the payment.
    :vartype debtor_party: :class:`tmvault.models.subsidiary.Party`
    :ivar creditor_party: The details of the party receiving the payment.
    :vartype creditor_party: :class:`tmvault.models.subsidiary.Party`
    :ivar payment_type: The type of this payment, e.g.
                        PAYMENT_TYPE_IMMEDIATE_PAYMENT.
    :vartype payment_type: str
    :ivar metadata: Additional information related to the payment.
    :vartype metadata: Dict[str, str]
    :ivar value_timestamp: The timestamp indicating when the payment was
                           created.
    :vartype value_timestamp: str
    :ivar update_timestamp: The timestamp indicating when the last change to
                            the payment current_status occurred.
    :vartype update_timestamp: str
    """

    def __init__(
        self,
        id_: str,
        amount: str,
        currency: str,
        reference: str,
        current_status: PaymentStatus,
        status_reason: str,
        target_status: PaymentStatus,
        debtor_party: Party,
        creditor_party: Party,
        payment_type: str,
        metadata: Dict[str, str],
        value_timestamp: datetime,
        update_timestamp: datetime,
    ):
        self.id_ = id_
        self.amount = amount
        self.currency = currency
        self.reference = reference
        self.current_status = current_status
        self.status_reason = status_reason
        self.target_status = target_status
        self.debtor_party = debtor_party
        self.creditor_party = creditor_party
        self.payment_type = payment_type
        self.metadata = metadata
        self.value_timestamp = value_timestamp
        self.update_timestamp = update_timestamp

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Payment)
            and self.id_ == other.id_
            and self.amount == other.amount
            and self.currency == other.currency
            and self.reference == other.reference
            and self.current_status == other.current_status
            and self.status_reason == other.status_reason
            and self.target_status == other.target_status
            and self.debtor_party == other.debtor_party
            and self.creditor_party == other.creditor_party
            and self.payment_type == other.payment_type
            and self.metadata == other.metadata
            and self.value_timestamp == other.value_timestamp
            and self.update_timestamp == other.update_timestamp
        )

    def __repr__(self) -> str:
        return (
            f'Payment['
            f'id_ = {self.id_}, '
            f'amount = {self.amount}, '
            f'currency = {self.currency}, '
            f'reference = {self.reference}, '
            f'current_status = {self.current_status}, '
            f'status_reason = {self.status_reason}, '
            f'target_status = {self.target_status}, '
            f'debtor_party = {self.debtor_party}, '
            f'creditor_party = {self.creditor_party}, '
            f'payment_type = {self.payment_type}, '
            f'metadata = {self.metadata}, '
            f'value_timestamp = {self.value_timestamp}, '
            f'update_timestamp = {self.update_timestamp}'
            f']'
        )

    @classmethod
    def from_json(cls, json_obj: Dict[str, Any]):
        return cls(
            id_=json_obj.get('id'),
            amount=json_obj.get('amount'),
            currency=json_obj.get('currency'),
            reference=json_obj.get('reference'),
            current_status=PaymentStatus(
                json_obj.get(
                    'current_status',
                    PaymentStatus.PAYMENT_STATUS_UNKNOWN.value
                )
            ),
            status_reason=json_obj.get('status_reason'),
            target_status=PaymentStatus(
                json_obj.get(
                    'target_status',
                    PaymentStatus.PAYMENT_STATUS_UNKNOWN.value
                )
            ),
            debtor_party=Party.from_json(json_obj.get('debitor_party', {})),
            creditor_party=Party.from_json(json_obj.get('creditor_party', {})),
            payment_type=json_obj.get('payment_type'),
            metadata=json_obj.get('metadata'),
            value_timestamp=datetime_from_timestamp_iso_string(
                json_obj.get('value_timestamp')
            ),
            update_timestamp=datetime_from_timestamp_iso_string(
                json_obj.get('update_timestamp')
            ),
        )
