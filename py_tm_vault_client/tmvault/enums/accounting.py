from enum import Enum


class TSide(Enum):
    """Enumeration for the side of the balance sheet that this account's
    balance is counted on in double-entry bookkeeping.

    More information at
    https://en.wikipedia.org/wiki/Debits_and_credits#Accounts_pertaining_to_the_five_accounting_elements

    - :TSIDE_ASSET: accounts whose balances benefit the bank, and will
                    continue to do so; for example, a credit card, personal
                    loan or mortgage.
    - :TSIDE_LIABILITY: accounts whose balances records a debt or future
                        obligation owed by the bank; for example, a current
                        account or savings account.
    - :TSIDE_UNKNOWN:
    """

    TSIDE_ASSET = 'TSIDE_ASSET'
    TSIDE_LIABILITY = 'TSIDE_LIABILITY'
    TSIDE_UNKNOWN = 'TSIDE_UNKNOWN'
