from datetime import datetime
from typing import Dict, List, Any

from .subsidiary import AccountBalance, StonksBalance
from ..enums import AccountStatus, PostingPhase, TSide
from ..utils import datetime_from_timestamp_iso_string, datetime_to_str


class Account:
    r"""A customer account.

    :ivar id\_: Globally unique ID for the account.
    :vartype id\_: str
    :ivar name: Display name.
    :vartype name: str
    :ivar product_id: The name of the product backing the account.
    :vartype product_id: str
    :ivar product_version_id: The ID of the product version matching the
                              product ID.
    :vartype product_version_id: str
    :ivar stonks_balances: The balances of this account. This is a map of
                           account address to a
                           :class:`tmvault.models.subsidiary.StonksBalance`
                           object. Usually, there will be one account address -
                           "DEFAULT" - unless the smart contract for this
                           account's product specifies otherwise.
    :vartype stonks_balances: Dict[str,
                              :class:`tmvault.models.subsidiary.StonksBalance`]
    :ivar status: The status of the account.
    :vartype status: :class:`tmvault.enums.AccountStatus`
    :ivar opening_timestamp: The time when the account was opened.
    :vartype opening_timestamp: :class:`datetime.datetime`
    :ivar stakeholder_ids: The customer IDs that can access the account.
    :vartype stakeholder_ids: List[str]
    :ivar instance_param_vals: The instance-level parameters for the
                               associated product; a map of the parameter name
                               to value.
    :vartype instance_param_vals: Dict[str, str]
    :ivar derived_instance_param_vals: The instance-level parameters for the
                                       associated product, derived from the
                                       account's Smart Contract code; a map of
                                       the parameter name to value.
    :vartype derived_instance_param_vals: Dict[str, str]
    :ivar details: A string-to-string map of custom additional account details.
    :vartype details: Dict[str, str]
    :ivar account_balance: The calculated balances associated with the account.
                           **Advanced and not recommended.** You'll probably
                           want to use the *stonks_balances* variable instead
    :vartype account_balance: :class:`tmvault.models.subsidiary.AccountBalance`
    :ivar tside: The side of the balance sheet where the account balance is
                 counted.
    :ivar uk_sort_code: The UK Sort Code of the account. May be unset.
    :vartype uk_sort_code: str
    :ivar uk_account_number: The Account Number of the account. May be unset.
    :vartype uk_account_number: str
    :vartype tside: :class:`tmvault.enums.TSide`
    """

    def __init__(self,
                 id_: str,
                 name: str,
                 product_id: str,
                 product_version_id: str,
                 status: AccountStatus,
                 opening_timestamp: datetime,
                 stakeholder_ids: List[str],
                 instance_param_vals: Dict[str, str],
                 derived_instance_param_vals: Dict[str, str],
                 details: Dict[str, str],
                 account_balance: AccountBalance,
                 tside: TSide,
                 uk_sort_code: str,
                 uk_account_number: str):
        self.id_ = id_
        self.name = name
        self.product_id = product_id
        self.product_version_id = product_version_id
        self.status = status
        self.opening_timestamp = opening_timestamp
        self.stakeholder_ids = stakeholder_ids
        self.instance_param_vals = instance_param_vals
        self.derived_instance_param_vals = derived_instance_param_vals
        self.details = details
        self.account_balance = account_balance
        self.tside = tside
        self.uk_sort_code = uk_sort_code
        self.uk_account_number = uk_account_number
        self._create_stonks_balances()

    def _create_stonks_balances(self) -> None:
        committed_live_balances = filter(
            lambda live_balance:
                live_balance.phase == PostingPhase.POSTING_PHASE_COMMITTED,
            self.account_balance.live_balances
        )
        self.stonks_balances: Dict[str, StonksBalance] = {
            live_balance.account_address: StonksBalance(
                float(live_balance.amount), live_balance.denomination
            ) for live_balance in committed_live_balances
        }

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Account)
            and self.id_ == other.id_
            and self.name == other.name
            and self.product_id == other.product_id
            and self.product_version_id == other.product_version_id
            and self.status == other.status
            and self.opening_timestamp == other.opening_timestamp
            and self.stakeholder_ids == other.stakeholder_ids
            and self.instance_param_vals == other.instance_param_vals
            and (self.derived_instance_param_vals ==
                 other.derived_instance_param_vals)
            and self.details == other.details
            and self.account_balance == other.account_balance
            and self.tside == other.tside
            and self.uk_sort_code == other.uk_sort_code
            and self.uk_account_number == other.uk_account_number
            and self.stonks_balances == other.stonks_balances
        )

    def __repr__(self) -> str:
        return (
            f'Account['
            f'id: {self.id_}, '
            f'name: {self.name}, '
            f'product_id: {self.product_id}, '
            f'product_version_id: {self.product_version_id}, '
            f'status: {self.status.name}, '
            f'opening_timestamp: {datetime_to_str(self.opening_timestamp)}, '
            f'stakeholder_ids: {self.stakeholder_ids}, '
            f'instance_param_vals: {self.instance_param_vals}, '
            f'derived_instance_param_vals: '
            f'{self.derived_instance_param_vals}, '
            f'details: {self.details}, '
            f'account_balance: {self.account_balance}, '
            f'tside: {self.tside.name}, '
            f'uk_sort_code: {self.uk_sort_code}, '
            f'uk_account_number: {self.uk_account_number}, '
            f'stonks_balances: {self.stonks_balances}'
            f']'
        )

    @classmethod
    def from_json(cls, json_obj: Dict[str, Any]):
        return cls(
            id_=json_obj.get('id'),
            name=json_obj.get('name'),
            product_id=json_obj.get('product_id'),
            product_version_id=json_obj.get('product_version_id'),
            status=AccountStatus(json_obj.get(
                'status', AccountStatus.ACCOUNT_STATUS_UNKNOWN.value)),
            opening_timestamp=datetime_from_timestamp_iso_string(
                json_obj.get('opening_timestamp')),
            stakeholder_ids=json_obj.get('stakeholder_ids'),
            instance_param_vals=json_obj.get('instance_param_vals'),
            derived_instance_param_vals=json_obj.get(
                'derived_instance_param_vals'),
            details=json_obj.get('details'),
            account_balance=AccountBalance.from_json(
                json_obj.get('account_balance', {})),
            tside=TSide[json_obj.get('accounting', {}).get(
                'tside', TSide.TSIDE_UNKNOWN.value)],
            # Sort code and account number *may* be set after creation
            uk_sort_code="",
            uk_account_number="",
        )
