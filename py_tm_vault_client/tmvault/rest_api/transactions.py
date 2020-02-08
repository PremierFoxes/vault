from datetime import datetime
import time
from typing import List, Dict

from .rest_api_client import RestAPIClient
from ..const import (
    DEFAULT_RETRY_SECONDS, DEFAULT_RETRY_INTERVAL, LIST_PAGE_SIZE
)
from ..enums import (
    TransactionStatus, TransactionRejectionCode,
    TransactionDirection, TransactionOrderBy
)
from ..models import Transaction
from ..models.subsidiary import ChargeAmount
from ..utils import datetime_to_str, get_logger
from ..errors import TransactionsNotFoundError

log = get_logger(__name__)


class TransactionsList(list):
    """
    A list of transactions, which is returned by the `list_transactions`
    methods.

    This class inherits from python's builtin :class:`list` class.

    This acts like a normal :class:`list` object in the way you'd expect.
    If you never need more than the first (up to) 100 transactions,
    you can treat this class as a normal python :class:`list` object.

    This class's purpose is to provide a `.get_next_page()` method which
    allows you to get the next page of transactions, if there is any.
    List transactions will return the first (up to) 100 transactions matching
    the filter provided.
    If your use case requires more than this, you will need to call
    `.get_next_page()` to get the next (up to) 100 transactions.
    """
    def __init__(
        self,
        list_: List[Transaction],
        transactions_api: 'TransactionsAPI',
        page_token: str,
        account_ids: List[str] = None,
        payment_order_ids: List[str] = None,
        payee_ids: List[str] = None,
        direction: TransactionDirection = None,
        statuses: List[TransactionStatus] = None,
        value_timestamp_range: Dict[str, datetime] = None,
        booking_timestamp_range: Dict[str, datetime] = None,
        last_update_timestamp_range: Dict[str, datetime] = None,
        charge_amount_value_range: Dict[str, str] = None,
        order_by: List[TransactionOrderBy] = None
    ):
        super().__init__(list_)
        self.transactions_api = transactions_api
        self.page_token = page_token
        self.account_ids = account_ids
        self.payment_order_ids = payment_order_ids
        self.payee_ids = payee_ids
        self.direction = direction
        self.statuses = statuses
        self.value_timestamp_range = value_timestamp_range
        self.booking_timestamp_range = booking_timestamp_range
        self.last_update_timestamp_range = last_update_timestamp_range
        self.charge_amount_value_range = charge_amount_value_range
        self.order_by = order_by

    def is_next_page(self) -> bool:
        """
        :return: True if there is a next page of transactions,
                 False otherwise.
        :rtype: bool
        """
        return bool(self.page_token)

    def get_next_page(self) -> 'TransactionsList':
        """
        :return: The next page of (up to) 100 transactions.
        :rtype: :class:`tmvault.rest_api.TransactionsList`
        """
        if not self.page_token:
            return TransactionsList([], self.transactions_api, "")
        return self.transactions_api._list_transactions(
            self.account_ids,
            self.payment_order_ids,
            self.payee_ids,
            self.direction,
            self.statuses,
            self.value_timestamp_range,
            self.booking_timestamp_range,
            self.last_update_timestamp_range,
            self.charge_amount_value_range,
            self.order_by,
            self.page_token
        )


class TransactionsAPI:
    def __init__(self, rest_api_client: RestAPIClient) -> None:
        self._rest_api_client = rest_api_client

    def batch_get_transactions(
        self,
        transaction_ids: List[str]
    ) -> Dict[str, Transaction]:
        """Gets multiple existing transactions by their IDs.

        :param transaction_ids: A list of the IDs of the transactions
                                requested.
        :type transaction_ids: List[str]
        :return: A transaction ID-to-Transaction object dictionary of the
                 requested transactions.
        :rtype: Dict[str, :class:`tmvault.models.Transaction`]
        """
        params = {'ids': transaction_ids}
        json_response = self._rest_api_client.get(
            '/v1/transactions:batchGet', params
        )
        return {
            id_: Transaction.from_json(json) for id_, json in
            json_response['transactions'].items()
        }

    def create_transaction(
        self,
        transaction_id: str = None,
        account_id: str = None,
        charge_amount: ChargeAmount = None,
        is_credit: bool = None,
        reference: str = None,
        status: TransactionStatus = None,
        value_timestamp: datetime = None,
        booking_timestamp: datetime = None,
        payee_id: str = None,
        payment_order_id: str = None,
        posting_instruction_batch_ids: List[str] = None,
        rejection_code: TransactionRejectionCode = None,
    ) -> Transaction:
        """Create a new transaction.

        :param transaction_id: Unique identifier for this transaction.
                    If not provided, a UUID will be automatically generated.
                    This field must contain a valid UUID in the canonical
                    8-4-4-4-12 form. Optional.
        :type transaction_id: str
        :param account_id: The Vault account ID this transaction applies to.
                            Required.
        :type account_id: str
        :param charge_amount: The amount of the transaction. Required.
        :type charge_amount: :class:`tmvault.models.subsidiary.ChargeAmount`
        :param is_credit: Whether the transaction is a credit or debit
                            from the point of view of the account referenced
                            by account_id. Defaults to false.
        :type is_credit: bool
        :param reference: The reference for this transaction. Optional.
        :type reference: str
        :param status: The transaction status. Required.
        :type status: :class:`tmvault.enums.TransactionStatus`
        :param value_timestamp: A UTC timestamp that records when the assets
                                become available to the account owner for
                                a credit or cease to be available to the
                                account owner for a debit.
                                If this field is populated and the transaction
                                is in a pending state,
                                it refers to an expected/requested value date.
                                Optional.
        :type value_timestamp: :class:`datetime.datetime`
        :param booking_timestamp: A UTC timestamp that records when a
                                    transaction becomes final.
                                    If this field is populated and the
                                    transaction is in a pending state,
                                    it refers to an expected booking date.
                                    Optional.
        :type booking_timestamp: :class:`datetime.datetime`
        :param payee_id: If applicable, ID of a payee associated with this
                            transaction. Optional.
        :type payee_id: str
        :param payment_order_id: If applicable, ID of the payment that
                                    generated this transaction as returned by
                                    the Payments API.
                                    This field must contain a valid UUID
                                    in the canonical 8-4-4-4-12 form. Optional.
        :type payment_order_id: str
        :param posting_instruction_batch_ids: Ordered list of posting
                                                instruction batch IDs.
                                                Ordered by posting batch
                                                value_timestamp, ascending.
                                                Can be supplied in any order,
                                                will be returned ordered.
                                                Once a batch ID has been linked
                                                to a transaction, it cannot
                                                be unlinked.
                                                Updates may only add new IDs
                                                to this collection.
                                                Can be empty (e.g. cancelled
                                                transaction, pre-auth
                                                creation).
                                                Optional.
        :type posting_instruction_batch_ids: List[str]
        :param rejection_code: If a transaction has status rejected,
                                this code represents the reason
                                for being rejected.
                                Optional.
        :type rejection_code: :class:`tmvault.enums.TransactionRejectionCode`
        :return: The created transaction
        :rtype: :class:`tmvault.models.Transaction`
        """

        transaction = {}

        if transaction_id is not None:
            transaction['id'] = transaction_id
        if account_id is not None:
            transaction['account_id'] = account_id
        if charge_amount is not None:
            transaction['charge_amount'] = charge_amount.get_dict()
        if is_credit is not None:
            transaction['is_credit'] = is_credit
        if reference is not None:
            transaction['reference'] = reference
        if status is not None:
            transaction['status'] = status.value
        if value_timestamp is not None:
            transaction['value_timestamp'] = datetime_to_str(value_timestamp)
        if booking_timestamp is not None:
            transaction['booking_timestamp'] = datetime_to_str(
                booking_timestamp
            )
        if payee_id is not None:
            transaction['payee_id'] = payee_id
        if payment_order_id is not None:
            transaction['payment_order_id'] = payment_order_id
        if posting_instruction_batch_ids is not None:
            transaction['posting_instruction_batch_ids'] = (
                posting_instruction_batch_ids
            )
        if rejection_code is not None:
            transaction['rejection_code'] = rejection_code.value

        post_response = self._rest_api_client.post("/v1/transactions", {
            "transaction": transaction
        })
        return Transaction.from_json(post_response)

    def list_transactions(
        self,
        account_ids: List[str] = None,
        payment_order_ids: List[str] = None,
        payee_ids: List[str] = None,
        direction: TransactionDirection = None,
        statuses: List[TransactionStatus] = None,
        value_timestamp_range: Dict[str, datetime] = None,
        booking_timestamp_range: Dict[str, datetime] = None,
        last_update_timestamp_range: Dict[str, datetime] = None,
        charge_amount_value_range: Dict[str, str] = None,
        order_by: List[TransactionOrderBy] = None
    ) -> TransactionsList:
        """
        Returns a filtered list of transactions.
        You must provide at least one of the available filter criteria to
        filter transactions.
        Filters are additive (similar to SQL AND),
        for example if you provide both account_ids
        and payment_order_ids then transactions will be returned that
        match both criteria.
        Within each filter field they are not additive however
        and works similar to the SQL OR operation.
        For example, providing multiple `account_ids` would return
        all of the transactions for both accounts.
        Transactions will be ordered by last_update_timestamp, descending.

        The first (up to) 100 transactions will be returned.
        To get the next (up to) 100 transactions, the
        :class:`tmvault.rest_api.TransactionsList` returned features a
        `get_next_page()` method.

        If no transactions match the filters specified,
        an empty list is returned.

        All range fields take a dictionary of the following format:

        .. highlight:: python
        .. code-block:: python

            {
                'from': <value_1>,
                'to': <value_2>
            }

        It is permitted to provide only a 'from' or only a 'to' field.
        For example, providing a 'from' field without a 'to' field
        would return all transactions that are greater than or equal to
        the specified value.
        From values are used in a 'greater than or equal to' comparison,
        and to values are used in a 'less than' comparison.

        :param account_ids: The Vault account IDs that are used to filter the
                            transaction list.
        :type account_ids: List[str]
        :param payment_order_ids: The payment order IDs that are used to filter
                                  the transaction list.
        :type payment_order_ids: List[str]
        :param payee_ids: The payee IDs that are used to filter the
                          transaction list.
        :type payee_ids: List[str]
        :param direction: Filter based on whether the transaction is a
                          creditor debit from the point of view of
                          the account referenced by account_id.
        :type direction: :class:`tmvault.enums.TransactionDirection`
        :param statuses: The transaction statuses that are used to filter
                         the transaction list.
        :type statuses: List[:class:`tmvault.enums.TransactionStatus`]
        :param value_timestamp_range: Filter based on a range of
                                      value timestamps.
        :type value_timestamp_range: Dict[str, :class:`datetime.datetime`]
        :param booking_timestamp_range: Filter based on a range of
                                        booking timestamps.
        :type booking_timestamp_range: Dict[str, :class:`datetime.datetime`]
        :param last_update_timestamp_range: Filter based on a range of
                                            last updated timestamps.
        :type last_update_timestamp_range: Dict[str,
                                                :class:`datetime.datetime`]
        :param charge_amount_value_range: Filter based on a range of
                                          charge amount values.
        :type charge_amount_value_range: Dict[str, str]
        :param order_by: The order by field sorts initially on the
                         specified column,
                         with the secondary sort performed on
                         the default column (last update timestamp desc).
        :type order_by: List[:class:`tmvault.enums.TransactionOrderBy`]
        :return: :class:`tmvault.rest_api.TransactionsList`
        """
        return self._list_transactions(
            account_ids,
            payment_order_ids,
            payee_ids,
            direction,
            statuses,
            value_timestamp_range,
            booking_timestamp_range,
            last_update_timestamp_range,
            charge_amount_value_range,
            order_by,
            None
        )

    def list_transactions_when_exists(
            self,
            account_ids: List[str] = None,
            payment_order_ids: List[str] = None,
            payee_ids: List[str] = None,
            direction: TransactionDirection = None,
            statuses: List[TransactionStatus] = None,
            value_timestamp_range: Dict[str, datetime] = None,
            booking_timestamp_range: Dict[str, datetime] = None,
            last_update_timestamp_range: Dict[str, datetime] = None,
            charge_amount_value_range: Dict[str, str] = None,
            order_by: List[TransactionOrderBy] = None,
            max_retry_seconds: int = DEFAULT_RETRY_SECONDS,
            retry_interval_seconds: int = DEFAULT_RETRY_INTERVAL
    ) -> TransactionsList:
        """
        This method performs the same function as `list_transactions`,
        but if `list_transactions` returns no results
        it retries for a pre-determined amount of time
        until a transaction exists.
        If after this time a transaction does not exist,
        a :class:`tmvault.errors.TransactionsNotFoundError` is raised.
        You may want to use this method if you have just created a
        payment using the API, as a transaction may not appear immediately
        whilst the payment processes. In almost all other cases
        it is expected that you would use `list_transactions`.

        Returns a filtered list of transactions.
        You must provide at least one of the available filter criteria to
        filter transactions.

        Filters are additive (similar to SQL AND),
        for example if you provide both account_ids
        and payment_order_ids then transactions will be returned that
        match both criteria.
        Within each filter field they are not additive however
        and works similar to the SQL OR operation.
        For example, providing multiple `account_ids` would return
        all of the transactions for both accounts.
        Transactions will be ordered by last_update_timestamp, descending.

        The first (up to) 100 transactions will be returned.
        To get the next (up to) 100 transactions,
        the :class:`tmvault.rest_api.TransactionsList` returned features a
        `get_next_page()` method.

        All range fields take a dictionary of the following format:

        .. highlight:: python
        .. code-block:: python

            {
                'from': <value_1>,
                'to': <value_2>
            }

        It is permitted to provide only a 'from' or only a 'to' field.
        For example, providing a 'from' field without a 'to' field
        would return all transactions that are greater than or equal to
        the specified value.
        From values are used in a 'greater than or equal to' comparison,
        and to values are used in a 'less than' comparison.

        :param account_ids: The Vault account IDs that are used to filter the
                            transaction list.
        :type account_ids: List[str]
        :param payment_order_ids: The payment order IDs that are used to filter
                                  the transaction list.
        :type payment_order_ids: List[str]
        :param payee_ids: The payee IDs that are used to filter the
                          transaction list.
        :type payee_ids: List[str]
        :param direction: Filter based on whether the transaction is a
                          creditor debit from the point of view of
                          the account referenced by account_id.
        :type direction: :class:`tmvault.enums.TransactionDirection`
        :param statuses: The transaction statuses that are used to filter
                         the transaction list.
        :type statuses: List[:class:`tmvault.enums.TransactionStatus`]
        :param value_timestamp_range: Filter based on a range of
                                      value timestamps.
        :type value_timestamp_range: Dict[str, :class:`datetime.datetime`]
        :param booking_timestamp_range: Filter based on a range of
                                        booking timestamps.
        :type booking_timestamp_range: Dict[str, :class:`datetime.datetime`]
        :param last_update_timestamp_range: Filter based on a range of
                                            last updated timestamps.
        :type last_update_timestamp_range: Dict[str,
                                                :class:`datetime.datetime`]
        :param charge_amount_value_range: Filter based on a range of
                                          charge amount values.
        :type charge_amount_value_range: Dict[str, str]
        :param order_by: The order by field sorts initially on the
                         specified column,
                         with the secondary sort performed on
                         the default column (last update timestamp desc).
        :type order_by: List[:class:`tmvault.enums.TransactionOrderBy`]
        :param max_retry_seconds: The maximum retry duration to wait for.
                                  Defaults to 5 seconds.
                                  Optional.
        :type max_retry_seconds: int
        :param retry_interval_seconds: The time period between each attempt
                                       to list transactions.
                                       Defaults to 0.5 seconds.
                                       Optional.
        :return: :class:`tmvault.rest_api.TransactionsList`
        """
        end_seconds = time.time() + max_retry_seconds
        while time.time() <= end_seconds:
            transactions = self.list_transactions(
                account_ids,
                payment_order_ids,
                payee_ids,
                direction,
                statuses,
                value_timestamp_range,
                booking_timestamp_range,
                last_update_timestamp_range,
                charge_amount_value_range,
                order_by,
            )
            if len(transactions) == 0:
                if time.time() + retry_interval_seconds <= end_seconds:
                    break
                log.debug("Cannot find any transactions, retrying...")
                time.sleep(retry_interval_seconds)
                continue
            return transactions
        log.debug("Failed to find any transactions after waiting")
        raise TransactionsNotFoundError(
            "Cannot find any transactions for the list criteria used"
        )

    def _list_transactions(
        self,
        account_ids: List[str] = None,
        payment_order_ids: List[str] = None,
        payee_ids: List[str] = None,
        direction: TransactionDirection = None,
        statuses: List[TransactionStatus] = None,
        value_timestamp_range: Dict[str, datetime] = None,
        booking_timestamp_range: Dict[str, datetime] = None,
        last_update_timestamp_range: Dict[str, datetime] = None,
        charge_amount_value_range: Dict[str, str] = None,
        order_by: List[TransactionOrderBy] = None,
        page_token: str = None,
    ) -> TransactionsList:
        params = {
            'page_size': LIST_PAGE_SIZE
        }

        if account_ids is not None:
            params['account_ids'] = account_ids
        if payment_order_ids is not None:
            params['payment_order_ids'] = payment_order_ids
        if payee_ids is not None:
            params['payee_ids'] = payee_ids
        if direction is not None:
            params['direction'] = direction.value
        if statuses is not None:
            params['statuses'] = [s.value for s in statuses]
        if value_timestamp_range is not None:
            if 'from' in value_timestamp_range:
                params['value_timestamp_range.from'] = datetime_to_str(
                    value_timestamp_range['from']
                )
            if 'to' in value_timestamp_range:
                params['value_timestamp_range.to'] = datetime_to_str(
                    value_timestamp_range['to']
                )
        if booking_timestamp_range is not None:
            if 'from' in booking_timestamp_range:
                params['booking_timestamp_range.from'] = datetime_to_str(
                    booking_timestamp_range['from']
                )
            if 'to' in booking_timestamp_range:
                params['booking_timestamp_range.to'] = datetime_to_str(
                    booking_timestamp_range['to']
                )
        if last_update_timestamp_range is not None:
            if 'from' in last_update_timestamp_range:
                params['last_update_timestamp_range.from'] = datetime_to_str(
                    last_update_timestamp_range['from']
                )
            if 'to' in last_update_timestamp_range:
                params['last_update_timestamp_range.to'] = datetime_to_str(
                    last_update_timestamp_range['to']
                )
        if charge_amount_value_range is not None:
            if 'from' in charge_amount_value_range:
                params['charge_amount_value_range.from'] = (
                    charge_amount_value_range['from']
                )
            if 'to' in charge_amount_value_range:
                params['charge_amount_value_range.to'] = (
                    charge_amount_value_range['to']
                )
        if order_by is not None:
            params['order_by'] = [o.value for o in order_by]

        if page_token is not None:
            params['page_token'] = page_token

        json_response = self._rest_api_client.get('/v1/transactions', params)
        list_resp = list(
            map(Transaction.from_json, json_response['transactions'])
        )
        return TransactionsList(
            list_resp,
            self,
            json_response.get('next_page_token'),
            account_ids,
            payment_order_ids,
            payee_ids,
            direction,
            statuses,
            value_timestamp_range,
            booking_timestamp_range,
            last_update_timestamp_range,
            charge_amount_value_range,
            order_by,
        )
