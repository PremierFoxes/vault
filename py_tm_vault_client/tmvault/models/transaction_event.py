from datetime import datetime
from typing import List

from ..utils import datetime_from_timestamp_iso_string, datetime_to_str
from ..enums import TransactionEventType
from .transaction import Transaction


class TransactionEvent:
    """A Stream API transaction event caused by either a create or update
    event.

    :ivar event_id: Unique identifier for this event.
    :vartype event_id: str
    :ivar timestamp: UTC timestamp of when event was emitted.
    :vartype timestamp: datetime
    :ivar change_id: An incremental counter representing the number of times
                     this transaction has been updated.
                     This will always be 0 for a CREATED event.
    :vartype change_id: int
    :ivar event_type: The type of event. Either a CREATED or UPDATED event.
    :vartype event_type: :class:`tmvault.enums.TransactionEventType`
    :ivar update_mask: List of transaction fields that were updated.
                       Will be an empty List for a CREATED event.
    :vartype update_mask: List[str]
    :ivar transaction: The transaction that was created/updated.
    :vartype transaction: :class:`tmvault.models.Transaction`
    """
    def __init__(
        self,
        event_id: str,
        timestamp: datetime,
        change_id: int,
        event_type: TransactionEventType,
        update_mask: List[str],
        transaction: Transaction
    ) -> None:
        self.event_id = event_id
        self.timestamp = timestamp
        self.change_id = change_id
        self.event_type = event_type
        self.update_mask = update_mask
        self.transaction = transaction

    def __eq__(self, o: object) -> bool:
        return (
            isinstance(o, TransactionEvent)
            and self.event_id == o.event_id
            and self.timestamp == o.timestamp
            and self.change_id == o.change_id
            and self.event_type == o.event_type
            and self.update_mask == o.update_mask
            and self.transaction == o.transaction
        )

    def __repr__(self) -> str:
        return (
            f'TransactionEvent['
            f'event_id: {self.event_id}, '
            f'timestamp: {datetime_to_str(self.timestamp)}, '
            f'change_id: {self.change_id}, '
            f'event_type: {self.event_type}, '
            f'update_mask: {self.update_mask}, '
            f'transaction: {self.transaction}'
            f']'
        )

    @classmethod
    def from_json(cls, json_obj) -> 'TransactionEvent':
        event_type = TransactionEventType.TRANSACTION_EVENT_UNKNOWN
        update_mask = []
        transaction = None

        if json_obj.get('transaction_created') is not None:
            event_type = TransactionEventType.TRANSACTION_EVENT_CREATED
            transaction = Transaction.from_json(
                json_obj.get('transaction_created').get('transaction'))
        elif json_obj.get('transaction_updated') is not None:
            event_type = TransactionEventType.TRANSACTION_EVENT_UPDATED
            update_event = json_obj.get('transaction_updated')
            update_mask = update_event.get('update_mask').get('paths')
            transaction = Transaction.from_json(
                update_event.get('transaction'))

        return cls(
            event_id=json_obj.get('event_id'),
            timestamp=datetime_from_timestamp_iso_string(
                json_obj.get('timestamp')),
            change_id=json_obj.get('change_id'),
            event_type=event_type,
            update_mask=update_mask,
            transaction=transaction
        )
