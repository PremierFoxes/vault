from typing import Dict, List

from ...enums import PostingPhase, TSide


class StonksBalance:
    """A simplified balance.

    :ivar amount: The amount of this balance.
    :vartype amount: float
    :ivar denomination: The unit that of this balance - typically a currency
                        code.
    :vartype denomination: str
    """

    def __init__(self, amount: float, denomination: str):
        self.amount = amount
        self.denomination = denomination

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, StonksBalance)
            and self.amount == other.amount
            and self.denomination == other.denomination
        )

    def __repr__(self) -> str:
        return (
            f'StonksBalance['
            f'amount: {self.amount}, '
            f'denomination: {self.denomination}'
            f']'
        )


class LiveBalanceAccounting:
    """Accounting information for a :class:`LiveBalance`.

    :ivar tside: The t-side for this balance.
    :vartype tside: :class:`tmvault.enums.TSide`
    """

    def __init__(self, tside: TSide):
        self.tside = tside

    def __repr__(self) -> str:
        return (
            f'LiveBalanceAccounting['
            f'tside: {self.tside}'
            f']'
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LiveBalanceAccounting) \
            and self.tside == other.tside

    @staticmethod
    def from_json(json_obj: Dict[str, any]):
        if 'tside' in json_obj:
            return LiveBalanceAccounting(
                tside=TSide(json_obj['tside'])
            )


class LiveBalance:
    """An account's current balance.

    :ivar amount: The net value of the balance.
    :vartype amount: str
    :ivar account_address: The address of this balance.
    :vartype account_address: str
    :ivar phase: The posting phase the balance applies to.
    :vartype phase: :class:`tmvault.enums.PostingPhase`
    :ivar asset: The asset in which the balance is held.
    :vartype asset: str
    :ivar denomination: The denomination in which the balance is held for the
                        given asset.
    :vartype denomination: str
    :ivar accounting: Accounting information for this live balance.
    :vartype accounting: :class:`LiveBalanceAccounting`
    """

    def __init__(self,
                 amount: str,
                 account_address: str,
                 phase: PostingPhase,
                 asset: str,
                 denomination: str,
                 accounting: LiveBalanceAccounting):
        self.amount = amount
        self.account_address = account_address
        self.phase = phase
        self.asset = asset
        self.denomination = denomination
        self.accounting = accounting

    def __repr__(self) -> str:
        return (
            f'LiveBalance['
            f'amount: {self.amount}, '
            f'account_address: {self.account_address}, '
            f'phase: {self.phase}, '
            f'asset: {self.asset}, '
            f'denomination: {self.denomination}, '
            f'accounting: {self.accounting}'
            f']'
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, LiveBalance)
            and self.amount == other.amount
            and self.account_address == other.account_address
            and self.phase == other.phase
            and self.asset == other.asset
            and self.denomination == other.denomination
            and self.accounting == other.accounting
        )

    @staticmethod
    def from_json(json_obj: Dict[str, any]) -> 'LiveBalance':
        return LiveBalance(
            amount=json_obj.get('amount'),
            account_address=json_obj.get('account_address'),
            phase=PostingPhase(json_obj.get(
                'phase', PostingPhase.POSTING_PHASE_UNKNOWN.value)),
            asset=json_obj.get('asset'),
            denomination=json_obj.get('denomination'),
            accounting=LiveBalanceAccounting.from_json(
                json_obj.get('accounting', {}))
        )


class AccountBalance:
    """The calculated balances associated with the account.

    :ivar as_of_pib_id: As of which Posting Instruction Batch ID to calculate
                        balances.
    :vartype as_of_pib_id: str
    :ivar live_balances: The current account balances.
    :vartype live_balances: List[:class:`LiveBalance`]
    """

    def __init__(self,
                 as_of_pib_id: str,
                 live_balances: List[LiveBalance]):
        self.as_of_pib_id = as_of_pib_id
        self.live_balances = live_balances

    def __repr__(self) -> str:
        return (
            f'AccountBalance['
            f'as_of_pib_id: {self.as_of_pib_id}, '
            f'live_balances: {self.live_balances}'
            f']'
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, AccountBalance)
            and self.as_of_pib_id == other.as_of_pib_id
            and self.live_balances == other.live_balances
        )

    @staticmethod
    def from_json(json_obj: Dict[str, any]) -> 'AccountBalance':
        return AccountBalance(
            as_of_pib_id=json_obj.get(
                'as_of_posting_instruction_batch_id'),
            live_balances=list(
                map(LiveBalance.from_json, json_obj.get('live_balances')))
        )
