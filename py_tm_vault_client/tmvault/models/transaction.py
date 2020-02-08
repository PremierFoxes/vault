from datetime import datetime
from typing import List

from ..enums import TransactionStatus, TransactionRejectionCode
from .subsidiary import ChargeAmount
from ..utils import datetime_from_timestamp_iso_string, datetime_to_str


class Transaction:
    r"""A transaction within a customer account.

    :ivar id\_: Unique identifier for this transaction.
    :vartype id\_: str
    :ivar account_id: The Vault account ID this transaction applies to.
    :vartype account_id: str
    :ivar charge_amount: The amount of the transaction.
    :vartype charge_amount: :class:`tmvault.models.subsidiary.ChargeAmount`
    :ivar is_credit: Whether the transaction is a credit or debit from the
                     point of view of the account referenced by `account_id`.
    :vartype is_credit: bool
    :ivar reference: The reference for this transaction.
    :vartype reference: str
    :ivar status: The transaction status.
    :vartype status: :class:`tmvault.enums.TransactionStatus`
    :ivar rejection_code: If a transaction has status rejected, this code
                          represents the reason for being rejected.
    :vartype rejection_code: :class:`tmvault.enums.TransactionRejectionCode`
    :ivar value_timestamp: A UTC timestamp that records when the assets become
                           available to the account owner for a credit or
                           cease to be available to the account owner for a
                           debit. If this field is populated and the
                           transaction is in a pending state, it refers to an
                           expected/requested value date.
    :vartype value_timestamp: :class:`datetime.datetime`
    :ivar booking_timestamp: A UTC timestamp that records when a transaction
                             becomes final. If this field is populated and the
                             transaction is in a pending state, it refers to
                             an expected booking date.
    :vartype booking_timestamp: :class:`datetime.datetime`
    :ivar last_update_timestamp: UTC timestamp recording when the transaction
                                 was last updated. If the transaction has
                                 never been updated, this field will represent
                                 the time the transaction resource was created.
    :vartype last_update_timestamp: :class:`datetime.datetime`
    :ivar payee_id: If applicable, ID of a payee associated with this
                    transaction.
    :vartype payee_id: str
    :ivar payment_order_id: If applicable, ID of the payment that generated
                            this transaction as returned by the Payments API.
    :vartype payment_order_id: str
    :ivar posting_instruction_batch_ids: Ordered list of posting instruction
                                         batch IDs. Ordered by posting batch
                                         value_timestamp, ascending. Once a
                                         batch ID has been linked to a
                                         transaction, it cannot be unlinked.
                                         Updates may only add new IDs to this
                                         collection. Can be empty (e.g.
                                         cancelled transaction, pre-auth
                                         creation).
    :vartype posting_instruction_batch_ids: List[str]
    """

    def __init__(
        self,
        id_: str,
        account_id: str,
        charge_amount: ChargeAmount,
        is_credit: bool,
        reference: str,
        status: TransactionStatus,
        rejection_code: TransactionRejectionCode,
        value_timestamp: datetime,
        booking_timestamp: datetime,
        last_update_timestamp: datetime,
        payee_id: str,
        payment_order_id: str,
        posting_instruction_batch_ids: List[str],
    ) -> None:
        self.id_ = id_
        self.account_id = account_id
        self.charge_amount = charge_amount
        self.is_credit = is_credit
        self.reference = reference
        self.status = status
        self.rejection_code = rejection_code
        self.value_timestamp = value_timestamp
        self.booking_timestamp = booking_timestamp
        self.last_update_timestamp = last_update_timestamp
        self.payee_id = payee_id
        self.payment_order_id = payment_order_id
        self.posting_instruction_batch_ids = posting_instruction_batch_ids

    def __eq__(self, o: object) -> bool:
        return (
            isinstance(o, Transaction)
            and self.id_ == o.id_
            and self.account_id == o.account_id
            and self.charge_amount == o.charge_amount
            and self.is_credit == o.is_credit
            and self.reference == o.reference
            and self.status == o.status
            and self.rejection_code == o.rejection_code
            and self.value_timestamp == o.value_timestamp
            and self.booking_timestamp == o.booking_timestamp
            and self.last_update_timestamp == o.last_update_timestamp
            and self.payee_id == o.payee_id
            and self.payment_order_id == o.payment_order_id
            and (self.posting_instruction_batch_ids ==
                 o.posting_instruction_batch_ids)
        )

    def __repr__(self) -> str:
        return (
            f'Transaction['
            f'id: {self.id_}, '
            f'account_id: {self.account_id}, '
            f'charge_amount: {self.charge_amount}, '
            f'is_credit: {self.is_credit}, '
            f'reference: {self.reference}, '
            f'status: {self.status}, '
            f'rejection_code: {self.rejection_code}, '
            f'value_timestamp: {datetime_to_str(self.value_timestamp)}, '
            f'booking_timestamp: {datetime_to_str(self.booking_timestamp)}, '
            f'last_update_timestamp: '
            f'{datetime_to_str(self.last_update_timestamp)}, '
            f'payee_id: {self.payee_id}, '
            f'payment_order_id: {self.payment_order_id}, '
            f'posting_instruction_batch_ids: '
            f'{self.posting_instruction_batch_ids}'
            f']'
        )

    @classmethod
    def from_json(cls, json_obj) -> 'Transaction':
        return cls(
            id_=json_obj.get('id', ''),
            account_id=json_obj.get('account_id', ''),
            charge_amount=ChargeAmount.from_json(
                json_obj.get('charge_amount', {})),
            is_credit=json_obj.get('is_credit'),
            reference=json_obj.get('reference', ''),
            status=TransactionStatus(json_obj.get(
                'status',
                TransactionStatus.TRANSACTION_STATUS_UNKNOWN.value
            )),
            rejection_code=TransactionRejectionCode(
                json_obj.get('rejection_code')),
            value_timestamp=datetime_from_timestamp_iso_string(
                json_obj.get('value_timestamp')),
            booking_timestamp=datetime_from_timestamp_iso_string(
                json_obj.get('booking_timestamp')),
            last_update_timestamp=datetime_from_timestamp_iso_string(
                json_obj.get('last_update_timestamp')),
            payee_id=json_obj.get('payee_id', ''),
            payment_order_id=json_obj.get('payment_order_id', ''),
            posting_instruction_batch_ids=json_obj.get(
                'posting_instruction_batch_ids', []),
        )
