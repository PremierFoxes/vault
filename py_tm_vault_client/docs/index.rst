Thought Machine Vault Client for Python
===================================================================

A Python library for a subset of Thought Machine's Vault Core Banking Engine. This is designed for use at hackathons and other engineering events.

You can also use the underlying API directly. For more information about this, go to Vault's `Documentation Hub <http://documentation.ichack.tmachine.io>`_.

Installation
------------

Pre-requisites
^^^^^^^^^^^^^^^

You need to have the following installed on your machine:

- `Python 3.6+ <https://www.python.org/downloads/>`_
- `requests <https://requests.readthedocs.io/>`_ Python library
- `dateutil <https://dateutil.readthedocs.io/en/stable/>`_ Python library
- `confluent-kafka <https://docs.confluent.io/current/clients/confluent-kafka-python/>`_ Python library

Obtaining the Vault Client library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Obtain the library zipfile from one of the Thought Machine team.
#. Extract the zipfile contents into your working directory.
#. Install the pre-requisites. This can be done easily with :code:`pip3 install --user --requirement py_tm_vault_client/requirements.txt`
#. Get a set of configuration and credentials from one of the Thought Machine team. This will be provided as a JSON file. **Make sure to add this file to your** ``.gitignore``
#. Set up the provided SSH keys, following the instructions provided. Then connect to Vault.

Getting started
---------------

To communicate with your Vault instance, you first need to instantiate a client:
::

    from py_tm_vault_client.tmvault import TMVaultClient
    client = TMVaultClient('/path/to/your/vault-config.json')


You can then create customers...
::

    from py_tm_vault_client.tmvault.enums import CustomerGender, CustomerTitle
    from datetime import date

    alice = client.customers.create_customer(
        customer_id='23503096792526979',
        title=CustomerTitle.CUSTOMER_TITLE_MISS,
        first_name='Alice',
        middle_name='Abigail',
        last_name='Anderson',
        dob=date(1997,1,1),
        gender=CustomerGender.CUSTOMER_GENDER_FEMALE,
        nationality='Australian',
        email_address='alice@example.com',
        mobile_phone_number='07979799799'
    )

    bob = client.customers.create_customer(
        customer_id='15101811503545856',
        title=CustomerTitle.CUSTOMER_TITLE_MR,
        first_name='Bob',
        middle_name='Brian',
        last_name='Brown',
        dob=date(1998,12,31),
        gender=CustomerGender.CUSTOMER_GENDER_MALE,
        nationality='Bahamian',
        email_address='bob@example.com',
        mobile_phone_number='07878788788'
    )

You can create accounts...
::

    alice_personal_account = client.accounts.create_account(
        account_id='alice_account_001',
        product_id='current_account_001',
        stakeholder_customer_ids=[alice.id_]
    )

    joint_account = client.accounts.create_account(
        account_id='alice_bob_joint_account_001',
        product_id='current_account_001',
        stakeholder_customer_ids=[alice.id_, bob.id_]
    )

You can make a payment...
::

    created_payment = client.payments.create_payment(
        amount='10.01',
        currency='GBP',
        debtor_account_id=alice_personal_account.id_,
        debtor_sort_code=alice_personal_account.uk_sort_code,
        debtor_account_number=alice_personal_account.uk_account_number,
        creditor_account_id=joint_account.id_,
        creditor_sort_code=joint_account.uk_sort_code,
        creditor_account_number=joint_account.uk_account_number,
        reference='my first payment',
        metadata={'key': 'value'}
    )

    # created_payment and fetched_payment are equal.
    fetched_payment = client.payments.get_payment(created_payment.id_)

.. toctree::
   :hidden:
   :maxdepth: 2

   vault_client
   accounts
   customers
   payments
   transactions
   enumerations
   subsidiary_types
   errors
