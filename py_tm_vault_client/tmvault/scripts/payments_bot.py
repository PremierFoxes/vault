from datetime import datetime
import json
import logging
import os
import random
from random import randint
import time
from typing import Dict

from .. import TMVaultClient
from ..models import Payment
from ..enums import PaymentStatus

log = logging.getLogger(__name__)


def create_payment(
    client: TMVaultClient,
    amount: str,
    debtor: Dict[str, str],
    creditor: Dict[str, str],
    payment_count: int,
) -> Payment:
    debtor_account_id = debtor.get('account_id')
    debtor_account_number = debtor.get('account_number')
    debtor_sort_code = debtor.get('sort_code')
    creditor_account_id = creditor.get('account_id')
    creditor_account_number = creditor.get('account_number')
    creditor_sort_code = creditor.get('sort_code')
    current_time = datetime.now().strftime("%H:%M:%S")
    reference = f'P{str(payment_count)}-{current_time}'

    return client.payments.create_payment(
        amount,
        debtor_account_id,
        debtor_sort_code,
        debtor_account_number,
        creditor_account_id,
        creditor_sort_code,
        creditor_account_number,
        reference
    )


def payments_bot(
    tm_vault_client: TMVaultClient,
    customers_file_path: str
):
    if not os.path.exists(customers_file_path):
        raise Exception(
            f'Cannot find customers file at {customers_file_path}')

    with open(customers_file_path) as customers_file:
        customers_json = json.load(customers_file)
    if len(customers_json) < 2:
        raise Exception(
            f'The customers.json does not contain enough customers '
            f'to make payments.'
        )

    try:
        payment_count = 0
        while True:
            time.sleep(randint(5, 20))
            customers = random.sample(customers_json, k=2)
            debtor = customers[0]
            creditor = customers[1]
            amount = str(round(random.uniform(0.50, 15.00), 2))
            payment_count += 1
            created_payment = create_payment(
                tm_vault_client,
                amount,
                debtor,
                creditor,
                payment_count
            )

            if (created_payment.current_status !=
                    PaymentStatus.PAYMENT_STATUS_SETTLED):
                log.warn(
                    f'Failed to create payment from '
                    f'{created_payment.debtor_party.account_id} to '
                    f'{created_payment.creditor_party.account_id} with status '
                    f'{created_payment.current_status}, reason '
                    f'{created_payment.status_reason} and target_status '
                    f'{created_payment.target_status}'
                )
                continue
            log.info(
                f'Payment of {amount} from '
                f'{created_payment.debtor_party.account_id} to '
                f'{created_payment.creditor_party.account_id}'
            )
    except KeyboardInterrupt:
        return
