from ...enums import ChargeAmountAsset


class ChargeAmount:
    """The amount of a transaction.

    The amount of a transaction is represented as an object with three fields.

    :ivar asset: The asset type of the Charge Amount.
    :vartype asset: :class:`tmvault.enums.ChargeAmountAsset`
    :ivar value: The value of the amount in string format, as an unsigned
                 number with optional floating point and arbitrary precision.
                 Valid examples: <100>, <0.1>, <5.99>, <0.23422>.
    :vartype value: str
    :ivar denomination: The denomination of the amount, e.g. GBP, EUR.
    :vartype denomination: str
    """

    def __init__(
        self,
        asset: ChargeAmountAsset,
        value: str,
        denomination: str
    ):
        self.asset = asset
        self.value = value
        self.denomination = denomination

    def __eq__(self, other):
        return (
            isinstance(other, ChargeAmount)
            and self.asset == other.asset
            and self.value == other.value
            and self.denomination == other.denomination
        )

    def __repr__(self):
        return (
            f'ChargeAmount['
            f'asset: {self.asset}, '
            f'value: {self.value},'
            f'denomination: {self.denomination}'
            f']'
        )

    def get_dict(self) -> dict:
        return {
            'asset': self.asset.value,
            'value': self.value,
            'denomination': self.denomination,
        }

    @classmethod
    def from_json(cls, json_obj) -> 'ChargeAmount':
        return cls(
            asset=ChargeAmountAsset(
                json_obj.get('asset', ChargeAmountAsset.UNKNOWN.value)),
            value=json_obj.get('value', ''),
            denomination=json_obj.get('denomination', '')
        )
