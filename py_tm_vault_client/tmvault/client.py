import os
from uuid import uuid4

from .config import VaultConfig
from .rest_api import (
    RestAPIClient, AccountsAPI, CustomersAPI, TransactionsAPI, PaymentsAPI
)
from .stream_api import TransactionsStreamAPI


class TMVaultClient:
    """A client for communicating with an instance of Vault.

    Example:

    .. highlight:: python
    .. code-block:: python

        from py_tm_vault_client.tmvault import TMVaultClient
        client = TMVaultClient('/path/to/your/vault-config.json')

    :param config_path: Path to the JSON configuration file.
                        Optional, defaults to data/vault-config.json.
    :type config_path: str
    :param group_id: A unique ID to be used as a Stream API consumer group ID.
                     This must be unique to avoid re-consuming messages or
                     consuming messages intended for a different consumer
                     group.
                     Optional, defaults to a random UUID4 string.
    :type group_id: str
    """

    def __init__(
        self,
        config_path: str = None,
        group_id: str = None
    ) -> None:
        config_path = config_path if config_path else os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            'data/vault-config.json'
        )
        config = VaultConfig.from_json_file_path(config_path)

        self._bootstrap_servers = config.kafka_url
        self._group_id = group_id if group_id else str(uuid4())

        # Set up REST base clients
        self._core_rest_api = RestAPIClient(
            config.core_api_url, config.service_account_token
        )
        self._xpl_rest_api = RestAPIClient(
            config.xpl_api_url, config.service_account_token
        )
        self._payments_hub_rest_api = RestAPIClient(
            config.payments_hub_api_url, config.service_account_token
        )

        # Declare REST API clients
        self._transactions_api = None
        self._accounts_api = None
        self._customers_api = None
        self._payments_hub_api = None

        # Declare Stream API clients
        self._transactions_stream_api = None

    @property
    def accounts(self) -> AccountsAPI:
        """An object for managing customer accounts.
        See the :doc:`Accounts documentation <accounts>` for details.
        """
        if self._accounts_api is None:
            self._accounts_api = AccountsAPI(
                self._core_rest_api, self._payments_hub_rest_api
            )
        return self._accounts_api

    @property
    def customers(self) -> CustomersAPI:
        """An object for managing customers.
        See the :doc:`Customers documentation <customers>` for details.
        """
        if self._customers_api is None:
            self._customers_api = CustomersAPI(self._core_rest_api)
        return self._customers_api

    @property
    def transactions(self) -> TransactionsAPI:
        """An object for managing transactions.
        See the :doc:`Transactions documentation <transactions>` for details.
        """
        if self._transactions_api is None:
            self._transactions_api = TransactionsAPI(self._xpl_rest_api)
        return self._transactions_api

    @property
    def transactions_stream(self) -> TransactionsStreamAPI:
        """An object for consuming transaction events.
        See the :ref:`Transactions documentation <transactions_stream>` for
        details.
        """
        if self._transactions_stream_api is None:
            self._transactions_stream_api = TransactionsStreamAPI(
                self._bootstrap_servers, self._group_id)
        return self._transactions_stream_api

    @property
    def payments(self) -> PaymentsAPI:
        """An object for creating and retrieving payments.
        See the :doc:`Payments documentation <payments>` for
        details.
        """
        if self._payments_hub_api is None:
            self._payments_hub_api = PaymentsAPI(self._payments_hub_rest_api)
        return self._payments_hub_api
