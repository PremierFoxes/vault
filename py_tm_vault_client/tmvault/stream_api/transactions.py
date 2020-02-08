import json

from ..models import TransactionEvent

_STREAM_API_TOPIC = 'vault.xpl_api.v1.transactions.transaction.events'


class TransactionsStreamAPI:
    def __init__(self, bootstrap_servers: str, group_id: str) -> None:
        from .kafka import Consumer
        self.consumer = Consumer(
            bootstrap_servers, _STREAM_API_TOPIC, group_id)

    def __del__(self) -> None:
        self.consumer.close()

    def consume(self) -> TransactionEvent:
        """Consumes from the transaction event topic and converts the JSON
        message into a TransactionEvent object.
        Blocks until a message is consumed.

        :return: The consumed transaction event
        :rtype: :class:`tmvault.models.TransactionEvent`
        """
        msg = self.consumer.consume()
        if msg:
            return TransactionEvent.from_json(json.loads(msg))
        return None

    def commit(self) -> None:
        """Commits the latest consumed message offset to Kafka.
        Call this after processing messages to avoid re-consuming the same
        messages after a application restart, assuming a group_id has been set.
        """
        self.consumer.commit()
