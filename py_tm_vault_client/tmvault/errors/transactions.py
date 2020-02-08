class TransactionsNotFoundError(IOError):
    """
    Error exclusively used within the
    `list_transactions_when_exists` function
    within :class:`tmvault.rest_api.TransactionsAPI`.

    Error indicates that the method cannot find any transactions
    after retrying for the specified time period.

    Error inherits from :class:`IOError`.
    """
    pass
