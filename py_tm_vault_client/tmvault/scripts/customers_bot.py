import json

import names

from .. import TMVaultClient
from ..models import Customer
from ..rest_api import CustomersAPI


def create_customer(client: CustomersAPI) -> Customer:
    first_name, last_name = names.get_first_name(), names.get_last_name()
    customer = client.create_customer(
        first_name=first_name,
        last_name=last_name,
        email_address=f'{first_name.lower()}_{last_name.lower()}@tm.net',
    )

    return customer


def customers_bot(
        tm_vault_client: TMVaultClient,
        num_customers: int,
        product_id: str,
        add_payment_device: bool,
        output_file_name: str,
):
    records = []
    customers_api_client = tm_vault_client.customers
    accounts_api_client = tm_vault_client.accounts
    for _ in range(num_customers):
        customer = create_customer(customers_api_client)
        account = accounts_api_client.create_account(
            product_id=product_id,
            stakeholder_customer_ids=[customer.id_],
            with_uk_account_number_and_sort_code=add_payment_device,
        )

        record = {
            'customer_id': customer.id_,
            'account_id': account.id_,
            'sort_code': account.uk_sort_code,
            'account_number': account.uk_account_number,
        }
        records.append(record)

    with open(output_file_name, 'w') as output_file:
        json.dump(records, output_file)

    return records
