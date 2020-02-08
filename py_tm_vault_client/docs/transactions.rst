Transactions
============

Transactions API
----------------

Manage transactions within a bank.

.. py:currentmodule:: tmvault.rest_api

Methods available on ``client.transactions``:

.. rst-class:: hide-signature
.. autoclass:: TransactionsAPI

  .. automethod:: batch_get_transactions()
  .. automethod:: create_transaction()
  .. automethod:: list_transactions()
  .. automethod:: list_transactions_when_exists()


The TransactionsList object
---------------------------

.. autoclass:: TransactionsList()

  .. automethod:: is_next_page()
  .. automethod:: get_next_page()


The Transaction object
----------------------

.. py:currentmodule:: tmvault.models

.. autoclass:: Transaction()


.. _transactions_stream:

Transactions Stream API
-----------------------

Consume transaction create or update events.

.. py:currentmodule:: tmvault.stream_api

Methods available on ``client.transactions_stream``:

.. rst-class:: hide-signature
.. autoclass:: TransactionsStreamAPI

  .. automethod:: consume()
  .. automethod:: commit()


The TransactionEvent object
---------------------------

.. py:currentmodule:: tmvault.models

.. autoclass:: TransactionEvent()
