import json
import os

REQUIRED_CONFIG_KEYS = {
    'user',
    'service_account_token',
    'core_api_url',
    'xpl_api_url',
    'payments_hub_api_url',
    'kafka_url',
    'vault_cidr',
}


class VaultConfig:
    def __init__(self, config_dict) -> None:
        self.config_dict = config_dict

    @property
    def user(self):
        return self.config_dict['user']

    @property
    def service_account_token(self):
        return self.config_dict['service_account_token']

    @property
    def core_api_url(self):
        return self.config_dict['core_api_url']

    @property
    def xpl_api_url(self):
        return self.config_dict['xpl_api_url']

    @property
    def payments_hub_api_url(self):
        return self.config_dict['payments_hub_api_url']

    @property
    def kafka_url(self):
        return self.config_dict['kafka_url']

    @property
    def vault_cidr(self):
        return self.config_dict['vault_cidr']

    def __repr__(self) -> str:
        return repr(self.config_dict)

    @classmethod
    def from_json_file_path(cls, config_path: str):
        if not os.path.exists(config_path):
            raise Exception(
                f'Cannot find config file at {config_path}')
        with open(config_path) as config_file:
            json_dict = json.load(config_file)
            for required_config_key in REQUIRED_CONFIG_KEYS:
                if required_config_key not in json_dict:
                    raise Exception(
                        f'The key, {required_config_key}, is not in your '
                        f'config file'
                    )
            return cls(json_dict)
