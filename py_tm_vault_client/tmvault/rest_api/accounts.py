from typing import Dict, List

from .rest_api_client import RestAPIClient
from ..const import LIST_PAGE_SIZE, SORT_CODE_BASE
from ..models import Account
from ..utils import timestamp_now
from ..enums import AccountStatus

CREATE_STATUS = AccountStatus.ACCOUNT_STATUS_OPEN.value
VIEW = 'ACCOUNT_VIEW_INCLUDE_BALANCES'


class AccountsAPI:
    def __init__(
        self,
        core_rest_api: RestAPIClient,
        payments_hub_rest_api: RestAPIClient
    ):
        self._core_rest_api = core_rest_api
        self._payments_hub_rest_api = payments_hub_rest_api

    def list_accounts_for_customer(
            self,
            customer_id: str,
            include_uk_sort_code_and_account_number: bool = True
    ) -> List[Account]:
        """Lists the accounts for a customer.

        :param customer_id: The ID of the customer.
        :type customer_id: str
        :return: A list of accounts for the customer.
        :param include_uk_sort_code_and_account_number: If this is set to True,
                                                        the uk_sort_code
                                                        and uk_account_number
                                                        fields on the returned
                                                        account will be
                                                        populated.
                                                        Defaults to True.
                                                        Optional.
        :type include_uk_sort_code_and_account_number: bool
        :rtype: List[Account]
        """
        json_response = self._core_rest_api.get('/v1/accounts', {
            'page_size': LIST_PAGE_SIZE,
            'stakeholder_id': customer_id,
            'view': VIEW
        })
        account_list = list(map(Account.from_json, json_response['accounts']))
        if include_uk_sort_code_and_account_number:
            self._add_sort_code_account_number_to_account_list(account_list)
        return account_list

    def get_account(
            self,
            account_id: str,
            include_uk_sort_code_and_account_number: bool = True
    ) -> Account:
        """Gets an existing Account object by its ID.

        :param account_id: The ID of the account.
        :type account_id: str
        :param include_uk_sort_code_and_account_number: If this is set to True,
                                                        the uk_sort_code
                                                        and uk_account_number
                                                        fields on the returned
                                                        account will be
                                                        populated.
                                                        Defaults to True.
                                                        Optional.
        :type include_uk_sort_code_and_account_number: bool
        :return: The Account object.
        :rtype: Account
        """
        json_response = self._core_rest_api.get(
            '/v1/accounts/%s' % account_id, {
                'instance_param_vals_effective_timestamp': timestamp_now(),
                'view': VIEW
            }
        )
        account = Account.from_json(json_response)
        if include_uk_sort_code_and_account_number:
            self._add_sort_code_account_number_to_account(account)
        return account

    def create_account(
        self,
        account_id: str = None,
        product_id: str = None,
        stakeholder_customer_ids: List[str] = None,
        instance_param_vals: Dict[str, str] = None,
        details: Dict[str, str] = None,
        with_uk_account_number_and_sort_code: bool = True,
    ) -> Account:
        """Create an account for one or more customers.

        :param account_id: The ID of the new account.
                           It must be unique.
                           Optional.
        :type account_id: str
        :param product_id: The ID of the product that this new account is
                           associated with. You can find a list of these in
                           the Operations Dashboard under Products > Product
                           Management.
                           Required.
        :type product_id: str
        :param stakeholder_customer_ids: A list of the customers' IDs who are
                                         stakeholders for this account. This
                                         will be one ID for an individual
                                         account, or two or more for a joint
                                         account.
                                         Required.
        :type stakeholder_customer_ids: List[str]
        :param instance_param_vals: The instance-level parameters for the
                                    associated product; a map of the parameter
                                    name to value, defaults to {}.
        :type instance_param_vals: Dict[str, str], optional
        :param details: A string-to-string map of custom additional account
                        details, defaults to {}.
        :type details: Dict[str, str], optional
        :param with_uk_account_number_and_sort_code: If this is set to True,
                                                     the created account will
                                                     be allocated a UK style
                                                     Account Number
                                                     and Sort Code.
                                                     This is required to make
                                                     or receive payments.
                                                     Defaults to True.
                                                     Optional.
        :type with_uk_account_number_and_sort_code: bool
        :return: The created account.
        :rtype: :class:`tmvault.models.Account`
        """

        account_to_create = {
            'status': CREATE_STATUS
        }
        if account_id is not None:
            account_to_create['id'] = account_id
        if product_id is not None:
            account_to_create['product_id'] = product_id
        if stakeholder_customer_ids is not None:
            account_to_create['stakeholder_ids'] = stakeholder_customer_ids
        if instance_param_vals is not None:
            account_to_create['instance_param_vals'] = instance_param_vals
        if details is not None:
            account_to_create['details'] = details

        account_dict = self._core_rest_api.post('/v1/accounts', {
            'account': account_to_create,
        })
        account = self.get_account(
            account_dict['id'], include_uk_sort_code_and_account_number=False
        )

        if with_uk_account_number_and_sort_code:
            uk_bank_account_number_dict = self._payments_hub_rest_api.post(
                '/v1/uk-bank-account-numbers', {
                    "uk_bank_account_number": {
                        "sort_code": SORT_CODE_BASE
                    }
                }
            )
            self._payments_hub_rest_api.post('/v1/payment-device-links', {
                'payment_device_link': {
                    'uk_bank_account_number_id':
                        uk_bank_account_number_dict['id'],
                    'vault_account_id': account.id_
                }
            })
            account.uk_sort_code = (
                uk_bank_account_number_dict['sort_code']
            )
            account.uk_account_number = (
                uk_bank_account_number_dict['account_number']
            )
        return account

    def update_account_stakeholders(
        self,
        account_id: str,
        new_stakeholder_customer_ids: List[str]
    ) -> Account:
        """Change the stakeholder customers for an account.

        :param account_id: The ID of the account.
        :type account_id: str
        :param new_stakeholder_customer_ids: A list of customer IDs who will be
                                             the new stakeholders of the
                                             account.
        :type new_stakeholder_customer_ids: List[str]
        :return: The updated account.
        :rtype: :class:`tmvault.models.Account`
        """
        put_response = self._core_rest_api.put(
            '/v1/accounts/%s' % account_id, {
                'account': {
                    'stakeholder_ids': new_stakeholder_customer_ids
                },
                'update_mask': {
                    'paths': ['stakeholder_ids']
                }
            }
        )
        return self.get_account(put_response['id'])

    def _add_sort_code_account_number_to_account(
        self, account: Account
    ) -> None:
        # Get payment device link
        payment_device_links = self._core_rest_api.get(
            '/v1/payment-device-links', {
                'account_ids': [account.id_]
            }
        )

        # Get the first one
        payment_device_link = payment_device_links['payment_device_links'][0]
        payment_device_id = payment_device_link['payment_device_id']

        # Get the device
        payment_devices_batch = self._core_rest_api.get(
            '/v1/payment-devices:batchGet', {
                'ids': [payment_device_id]
            }
        )
        payment_device = (
            payment_devices_batch['payment_devices'][payment_device_id]
        )
        routing_info = payment_device['routing_info']
        sort_code = routing_info['sort_code']
        account_number = routing_info['account_number']

        account.uk_sort_code = sort_code
        account.uk_account_number = account_number

    def _add_sort_code_account_number_to_account_list(
        self, account_list: List[Account]
    ) -> None:
        # Get payment device link
        payment_device_links_response = self._core_rest_api.get(
            '/v1/payment-device-links', {
                'account_ids': [a.id_ for a in account_list]
            }
        )
        payment_device_links_list = (
            payment_device_links_response['payment_device_links']
        )
        payment_device_id_by_account_id = {
                link['account_id']: link['payment_device_id']
                for link in payment_device_links_list
        }
        payment_device_ids = [
            link['payment_device_id']
            for link in payment_device_links_list
        ]

        # Get the device
        payment_devices_batch = self._core_rest_api.get(
            '/v1/payment-devices:batchGet', {
                'ids': payment_device_ids
            }
        )
        payment_devices = payment_devices_batch['payment_devices']

        for a in account_list:
            payment_device_id = payment_device_id_by_account_id[a.id_]
            payment_device = payment_devices[payment_device_id]
            routing_info = payment_device['routing_info']
            sort_code = routing_info['sort_code']
            account_number = routing_info['account_number']
            a.uk_sort_code = sort_code
            a.uk_account_number = account_number
