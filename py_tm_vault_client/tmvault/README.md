# Thought Machine Vault Client for Python

## Example

```python3
from tmvault import TMVaultClient

client = TMVaultClient('/path/to/your/vault-config.json')

accounts_for_person_a = client.accounts.list_accounts_for_customer('5320319443367695238')
print(accounts_for_person_a[0].name)
```

## Documentation

Documentation is auto-generated from code comments using [Sphinx](http://www.sphinx-doc.org).

### Pre-requisites

- Python 3.6+
- Some Python dependencies
  - [`requests`](https://requests.readthedocs.io/): `pip3 install requests`
  - [`python-dateutil`](https://dateutil.readthedocs.io/en/stable/): `pip3 install python-dateutil`
  - [`confluent-kafka`](https://docs.confluent.io/current/clients/confluent-kafka-python/): `pip3 install confluent-kafka`

For using `vault-stonks`:
- [`names`](https://github.com/treyhunner/names): `pip3 install names`
- [`sshuttle`](https://sshuttle.readthedocs.io/en/stable/): `pip3 install sshuttle`
