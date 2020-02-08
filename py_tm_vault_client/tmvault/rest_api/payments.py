import time
from typing import Dict

from .rest_api_client import RestAPIClient
from ..models import Payment
from ..enums import PaymentStatus


class PaymentsAPI:
    def __init__(self, rest_api_client: RestAPIClient) -> None:
        self._rest_api_client = rest_api_client

    def create_payment(
            self,
            amount: str,
            debtor_account_id: str,
            debtor_sort_code: str,
            debtor_account_number: str,
            creditor_account_id: str,
            creditor_sort_code: str,
            creditor_account_number: str,
            reference: str,
            currency: str = "GBP",
            metadata: Dict[str, str] = {},
    ) -> Payment:
        """Creates a new payment.

        :param amount: The payment amount value in string format, as an
                       unsigned number with optional floating point and
                       arbitrary precision.
                       Valid examples: <10>, <0.1>, <0.234>.
        :type amount: str
        :param debtor_account_id: The debtor's Vault account ID.
        :type debtor_account_id: str
        :param debtor_sort_code: The UK sort code identifying the bank branch
                                 the debtor's account is held in.
        :type debtor_sort_code: str
        :param debtor_account_number: The debtor's account number associated
                                      with the sort code.
        :type debtor_account_number: str
        :param creditor_account_id: The creditor's Vault account ID.
        :type creditor_account_id: str
        :param creditor_sort_code: The UK sort code identifying the bank branch
                                   the creditor's account is held in.
        :type creditor_sort_code: str
        :param creditor_account_number: The creditor's account number
                                        associated with the sort code.
        :type creditor_account_number: str
        :param reference: The reference of this payment.
        :type reference: str
        :param currency: The denomination of the amount, e.g. GBP, EUR.
                         Defaults to GBP.
        :type currency: str
        :param metadata: Additional information related to the payment,
                         optional.
        :type metadata: Dict[str, str]
        :return: The created payment.
        :rtype: :class:`tmvault.models.Payment`
        """

        debtor_party = {
            'account_id': debtor_account_id,
            'name': 'debtor_name',
            'bban': {
                'bank_id_code': 'GBDSC',
                'bank_id': debtor_sort_code,
                'account_number': debtor_account_number,
            }
        }
        creditor_party = {
            'account_id': creditor_account_id,
            'name': 'creditor_name',
            'bban': {
                'bank_id_code': 'GBDSC',
                'bank_id': creditor_sort_code,
                'account_number': creditor_account_number,
            }
        }

        post_response = self._rest_api_client.post('/v1/payments', {
            'payment': {
                'scheme': "OnUs",
                'amount': amount,
                'currency': currency,
                'reference': reference,
                'debitor_party': debtor_party,
                'creditor_party': creditor_party,
                'direction': "PAYMENT_DIRECTION_OUTBOUND",
                'payment_type': "PAYMENT_TYPE_IMMEDIATE_PAYMENT",
                'metadata':  metadata,
            }
        })

        created_payment = Payment.from_json(post_response)
        # We check that the payment passed validation, otherwise we return the
        # created payment. Inspect status_reason for more details.
        if created_payment.current_status !=\
                PaymentStatus.PAYMENT_STATUS_RECEIVED:
            return created_payment

        payment_id = created_payment.id_
        put_data = {
            'payment': {
                'target_status': PaymentStatus.PAYMENT_STATUS_SETTLED.value,
            },
            'update_mask': {
                'paths': ['target_status'],
            }
        }

        put_response = self._rest_api_client.put(
            '/v1/payments/%s' % payment_id, put_data)
        fetched_payment = Payment.from_json(put_response)

        while fetched_payment.current_status ==\
                PaymentStatus.PAYMENT_STATUS_RECEIVED or \
                fetched_payment.current_status ==\
                PaymentStatus.PAYMENT_STATUS_AWAITING_SETTLEMENT:
            fetched_payment = self.get_payment(payment_id)
            time.sleep(0.5)

        return fetched_payment

    def get_payment(self, payment_id: str) -> Payment:
        """Gets an existing Payment object by its ID.

        :param payment_id: The ID of the payment.
        :type payment_id: str
        :return: The Payment object.
        :rtype: :class:`tmvault.models.Payment`
        """

        json_response = self._rest_api_client.get(
            '/v1/payments:batchGet', {'ids': [payment_id]}
        )
        payments_json_response = json_response.get('payments', {})
        fetched_payment = payments_json_response[payment_id]
        return Payment.from_json(fetched_payment)
