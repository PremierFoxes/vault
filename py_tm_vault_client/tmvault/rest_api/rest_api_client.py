from typing import Dict
from uuid import uuid4

import requests


# We use this because the HTTPError raised within `response.raise_for_status()`
# ignores the body of the response which has vault error information in
def raise_for_status(response: requests.Response):
    try:
        response.raise_for_status()
    except requests.HTTPError:
        try:
            json_response = response.json()
            vault_error_code = json_response.get('vault_error_code')
            tracing_id = json_response.get('tracing_id')
            message = json_response.get('message')
            raise requests.HTTPError(
                (
                    f'Request to url <{response.url}> '
                    f'failed with HTTP Code <{response.status_code}>, '
                    f'Vault Error Code: <{vault_error_code}>, '
                    f'Tracing ID <{tracing_id}>, '
                    f'Message: <{message}>'
                ),
                response=response
            ) from None
        except ValueError:
            # If the response does not contain JSON
            raise requests.HTTPError(
                'Request to url %s failed with http code %s, body: %s' % (
                    response.url, response.status_code, response.content),
                response=response
            ) from None


class RestAPIClient:
    def __init__(self, base_api_uri: str, access_token: str) -> None:
        self.headers = {
            'X-Auth-Token': access_token
        }
        self.api_uri = base_api_uri

    def get(self, endpoint_path: str, params: Dict[str, any] = {}) -> dict:
        """Performs an HTTP GET request to the Vault REST API and returns the
        json-encoded response.

        Example:
        .. code-block:: python
            rest_api_client.get(
                '/v1/accounts/754386409',
                {'fields_to_include':['INCLUDE_FIELD_DERIVED_INSTANCE_PARAM_VALS']})

        :param endpoint_path: API endpoint path, starting with /
        :type endpoint_path: str
        :param params: Dictionary of query parameters
        :type params: Dict[str, any]
        ...
        :raises requests.HTTPError: [ErrorDescription]
        ...
        :return: If the HTTP request returned an error status code (4xx, 5xx)
        :rtype: dict
        """
        response = requests.get(
            f'{self.api_uri}{endpoint_path}',
            params=params,
            headers=self.headers
        )
        raise_for_status(response)
        return response.json()

    def post(self, endpoint_path: str, data: Dict[str, any]) -> dict:
        """Performs an HTTP POST request to the Vault REST API and returns the
        json-encoded response.

        Example:
        .. code-block:: python
            rest_api_client.post(
                '/v1/flag-definitions',
                {
                    'flag_definition': {
                        "id": "hello_this_is_maurice",
                        "name": "hello_this_is_maurice",
                        "description": "test test",
                        "required_flag_level": "FLAG_LEVEL_CUSTOMER",
                        "flag_visibility": "FLAG_VISIBILITY_CONTRACT",
                        "is_active": False
                    }
                })

        :param endpoint_path: API endpoint path
        :type endpoint_path: str
        :param data: JSON dictionary to post
        :type data: Dict[str, any]
        ...
        :raises requests.HTTPError: [ErrorDescription]
        ...
        :return: If the HTTP request returned an error status code (4xx, 5xx)
        :rtype: dict
        """
        post_json = {'request_id': str(uuid4()), **data}
        response = requests.post(
            f'{self.api_uri}{endpoint_path}',
            json=post_json,
            headers=self.headers
        )
        raise_for_status(response)
        return response.json()

    def put(self, endpoint_path: str, data: Dict[str, any]) -> dict:
        """Performs an HTTP PUT request to the Vault REST API and returns the
        json-encoded response.

        Example:
        .. code-block:: python
            rest_api_client.put(
                '/v1/accounts/6734-safd7ssdsad-432334',
                {
                    'account': {
                    'stakeholder_ids': ['346783465345786', '7322634786326']
                },
                'update_mask': {
                    'paths': ['stakeholder_ids']
                }
            })

        :param endpoint_path: API endpoint path
        :type endpoint_path: str
        :param data: JSON dictionary to put
        :type data: Dict[str, any]
        ...
        :raises requests.HTTPError: [ErrorDescription]
        ...
        :return: If the HTTP request returned an error status code (4xx, 5xx)
        :rtype: dict
        """
        put_json = {'request_id': str(uuid4()), **data}
        response = requests.put(
            f'{self.api_uri}{endpoint_path}',
            json=put_json,
            headers=self.headers
        )
        raise_for_status(response)
        return response.json()
