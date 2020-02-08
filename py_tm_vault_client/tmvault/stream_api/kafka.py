import socket

from confluent_kafka import (
    Consumer as ConfluentConsumer, Producer as ConfluentProducer
)
from confluent_kafka import KafkaError, KafkaException

from ..utils import get_logger

MEBIBYTE = 1024 * 1024

log = get_logger(__name__)


class Consumer:
    def __init__(
        self, bootstrap_servers: str, topic: str, group_id: str
    ) -> None:
        config = {
            'bootstrap.servers': bootstrap_servers,
            # Where to consume from after a reset
            # "latest" is the end of the topic, "earliest" is the beginning
            'default.topic.config': {
                'auto.offset.reset': 'latest'
            },
            'metadata.request.timeout.ms': 20000,
            'enable.auto.commit': False,
            'group.id': group_id,
            'api.version.request': True,
            'fetch.wait.max.ms': 100,
            'log.connection.close': False,
            # This logger will log messages originating from non-Python code
            'logger': get_logger('librdkafka'),
            # Max number of bytes per partition returned by the server
            'max.partition.fetch.bytes': MEBIBYTE * 5,
            'statistics.interval.ms': 15000,
            'queued.max.messages.kbytes': 1024 * 64,
        }
        self._consumer = ConfluentConsumer(config)
        self._consumer.subscribe([topic])

    def consume(self) -> str:
        while True:
            msg = self._consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error() is None:
                log.debug(f'Received message: {msg.value().decode("utf-8")}')
                return msg.value().decode('utf-8')
            elif msg.error().code() != KafkaError._PARTITION_EOF:
                log.error(
                    f'Failed to consume from topic, continuing... '
                    f'Reason: {KafkaException(msg.error())}',
                )
            else:
                log.debug('Reached end of topic, waiting for new messages...')

    def commit(self) -> None:
        self._consumer.commmit()

    def close(self) -> None:
        self._consumer.unsubscribe()
        self._consumer.close()


class Producer:
    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self._topic = topic
        config = {
            'bootstrap.servers': bootstrap_servers,
            'default.topic.config': {
                'acks': 'all'
            },
            'queue.buffering.max.ms': 50,
            'metadata.request.timeout.ms': 20000,
            'client.id': socket.gethostname(),
            'compression.codec': 'snappy',
            'api.version.request': True,
            'log.connection.close': False,
            # The maximum size of a request in bytes
            'message.max.bytes': MEBIBYTE * 4
        }
        self._producer = ConfluentProducer(config)

    def produce(self, msg: str):

        def on_callback(error, message):
            """Raises KafkaException if message delivery failed.
            """
            if error is not None:
                raise KafkaException(error)

        self._producer.produce(
            self._topic, msg.encode('utf-8'), callback=on_callback
        )
        self._producer.flush()
