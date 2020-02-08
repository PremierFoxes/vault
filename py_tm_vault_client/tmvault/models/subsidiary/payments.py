from typing import Dict


class Party:
    """The debtor or creditor in a :class:`tmvault.models.Payment`.

    :ivar account_id: The internal Vault account ID.
    :vartype account_id: str
    :ivar name: The name associated with the account.
    :vartype name: str
    :ivar sort_code: The UK sort code identifying the bank branch the account
                     is held in.
    :vartype account_id: str
    :ivar account_id: The account number associated with the sort code.
    :vartype account_id: str
    """

    def __init__(
        self,
        account_id: str,
        name: str,
        sort_code: str,
        account_number: str,
    ):
        self.account_id = account_id
        self.name = name
        self.sort_code = sort_code
        self.account_number = account_number

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Party)
            and self.account_id == other.account_id
            and self.name == other.name
            and self.sort_code == other.sort_code
            and self.account_number == other.account_number
        )

    def __repr__(self) -> str:
        return (
            f'Party['
            f'account_id: {self.account_id}, '
            f'name: {self.name}, '
            f'sort_code: {self.sort_code}, '
            f'account_number: {self.account_number}'
            f']'
        )

    @staticmethod
    def from_json(json_obj: Dict[str, any]) -> 'Party':
        return Party(
            account_id=json_obj.get('account_id'),
            name=json_obj.get('name'),
            sort_code=json_obj.get('bban').get('bank_id'),
            account_number=json_obj.get('bban').get('account_number')
        )
