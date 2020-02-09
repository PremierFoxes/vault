from __future__ import print_function
from django.http import HttpResponse
import swagger_client
from swagger_client.rest import ApiException
from py_tm_vault_client.tmvault import TMVaultClient

client = TMVaultClient('./data/vault-config.json')
api_instance = swagger_client.IcHackControllerApi()

def index(request):
    return HttpResponse("Hello World")

def get_account_balance(request):
    print("HELLO")
    wallet_id = request.GET.get('wallet_id', 'id')
    wallet_key = request.GET.get('wallet_key', 'key')
    prover_did = request.GET.get('prover_did', 'did')
    mid = request.GET.get('prover_mid', 'mid')
    api_response = ''
    try:
        api_response = api_instance.get_account_id_using_get(did=prover_did, mid=mid,
                                                             id=wallet_id,
                                                             key=wallet_key)
        print(api_response)
    except ApiException as e:
        return HttpResponse('unsuccessful')

    account = client.accounts.get_account(api_response)
    balance = get_balance(account)
    response = HttpResponse(balance)
    response['Access-Control-Allow-Origin'] = '*'
    print(balance)
    return response

def create_account(request):
    wallet_id = request.GET.get('wallet_id', 'id')
    wallet_key = request.GET.get('wallet_key', 'key')
    #profile_pic = request.GET.get('image', 'pic')
    name = request.GET.get('name', 'name')
    dob = request.GET.get('dob', 'dob')

    customer = client.customers.create_customer(
        first_name=wallet_id,
        last_name=wallet_key
    )
    print(customer.id_)
    account = client.accounts.create_account(product_id='current_account', stakeholder_customer_ids=[customer.id_])
    account_id = account.id_

    try:
        print("HELLO")
        api_response = api_instance.create_new_user_wallet_without_image_using_post(_date=dob, name=name,
                                                                                    prover_wallet_id=wallet_id,
                                                                                    prover_wallet_key=wallet_key,
                                                                                    account_id=account_id)
        response = HttpResponse(api_response)
        response['Access-Control-Allow-Origin'] = '*'
        print(api_response)
        return response
    except ApiException as e:
        return HttpResponse('error creating account')

# Create your views here.

def buy_ticket(request):
    wallet_id = request.GET.get('wallet_id', 'd')
    wallet_key = request.GET.get('wallet_key', 'd')
    prover_did = request.GET.get('prover_did', 'YZuaiEJB3MJDrhsqBEXMUQ')
    mid = request.GET.get('prover_mid', '5b42781e-978e-4e9a-aa5f-10054b20bece')
    event = request.GET.get('event', 'event')
    seat = request.GET.get('seat', 'seat')
    price = request.GET.get('price', '10')
    api_response = ''
    try:
        api_response = api_instance.get_account_id_using_get(did=prover_did, mid=mid,
                                                             id=wallet_id,
                                                             key=wallet_key)
        print(api_response)
    except ApiException as e:
        print("Exception when calling IcHackControllerApi->get_account_id_using_get: %s\n" % e)
        return HttpResponse('bad request')

    account = client.accounts.get_account(account_id=api_response)
    balance = get_balance(account)

    creditor = client.accounts.get_account(account_id='7652eb1b-04da-ca56-b2a2-ad0c2cc05754')

    if balance > price:
        print(account)
        client.payments.create_payment(
            amount=str(10),
            debtor_account_id=account.id_,
            debtor_sort_code=account.uk_sort_code,
            debtor_account_number=account.uk_account_number,
            creditor_account_id=creditor.id_,
            creditor_sort_code=creditor.uk_sort_code,
            creditor_account_number=creditor.uk_account_number,
            reference='ticket purchase'
        )
    else:
        return HttpResponse(status_code=500, content='insufficient funds')

    try:
        issued_ticket = api_instance.issue_airline_ticket_using_post(prover_did=prover_did, master_secret_id=mid,
                                                             prover_wallet_id=wallet_id,
                                                             prover_wallet_key=wallet_key,
                                                             area=event, seat=seat)
        print(issued_ticket)
        response = HttpResponse(issued_ticket, content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except ApiException as e:
        print("Exception when calling IcHackControllerApi->issue_ticket_using_post: %s\n" % e)
        return HttpResponse('Couldn\'t issue ticket')

def get_balance(account):
    for i in range(len(account.account_balance.live_balances)):
        if str(account.account_balance.live_balances[i].phase) == 'PostingPhase.POSTING_PHASE_COMMITTED':
            live_balance = account.account_balance.live_balances[i].amount
            print('Balance:', live_balance)
            return live_balance

def deposit_funds(request):
    wallet_id = request.GET.get('wallet_id', 'd')
    wallet_key = request.GET.get('wallet_key', 'd')
    prover_did = request.GET.get('prover_did', 'did')
    mid = request.GET.get('prover_mid', 'mid')
    amount = request.GET.get('amount', '0')
    account = ''
    try:
        account_id = api_instance.get_account_id_using_get(did=prover_did, mid=mid,
                                                             id=wallet_id,
                                                             key=wallet_key)
        print(account_id)
    except ApiException as e:
        return HttpResponse('error getting account details')

    try:
        account = client.accounts.get_account(account_id=account_id)

        client.payments.create_payment(
            amount=amount,
            debtor_account_id='aae9a2b9-f5c2-75c5-81ad-b605b9542baa',
            debtor_sort_code='989999',
            debtor_account_number='69732649',
            creditor_account_id=account.id_,
            creditor_sort_code=account.uk_sort_code,
            creditor_account_number=account.uk_account_number,
            reference='deposit'
        )

        response = HttpResponse(get_balance(account))
        response['Access-Control-Allow-Origin'] = '*'
        return response

    except ApiException as e:
        return HttpResponse('error depositing funds')

