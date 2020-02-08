from datetime import date
from typing import Dict, List

from .rest_api_client import RestAPIClient
from ..enums import (
    CustomerAccessibility, CustomerContactMethod, CustomerGender, CustomerTitle
)
from ..models import Customer


class CustomersAPI:
    def __init__(self, rest_api: RestAPIClient):
        self._rest_api = rest_api

    def get_customer(self, customer_id: str) -> Customer:
        """Gets an existing Customer object by its ID.

        :param customer_id: The ID of the customer.
        :type customer_id: str
        :return: The Customer object.
        :rtype: :class:`tmvault.models.Customer`
        """
        json_response = self._rest_api.get('/v1/customers/%s' % customer_id)
        return Customer.from_json(json_response)

    def get_customers(self, customer_ids: List[str]) -> Dict[str, Customer]:
        """Gets multiple existing customers by their IDs.

        :param customer_ids: A list of the IDs of the customers.
        :type customer_ids: List[str]
        :return: A customer ID-to-Customer object map of the requested
                 customers.
        :rtype: Dict[str, :class:`tmvault.models.Customer`]
        """
        json_response = self._rest_api.get(
            '/v1/customers:batchGet', {'ids': customer_ids})
        customers_json_response = json_response.get('customers', {})
        return {
            customer_id: Customer.from_json(customer_json)
            for customer_id, customer_json in customers_json_response.items()
        }

    def create_customer(
        self,
        customer_id: str = None,
        title: CustomerTitle = None,
        first_name: str = None,
        middle_name: str = None,
        last_name: str = None,
        dob: date = None,
        gender: CustomerGender = None,
        nationality: str = None,
        email_address: str = None,
        mobile_phone_number: str = None,
        home_phone_number: str = None,
        business_phone_number: str = None,
        contact_method: CustomerContactMethod =
        CustomerContactMethod.CUSTOMER_CONTACT_METHOD_NONE,
        country_of_residence: str = None,
        country_of_taxation: str = None,
        accessibility: CustomerAccessibility = None,
        additional_details: Dict[str, str] = None
    ) -> Customer:
        """Creates a new customer

        :param customer_id: Unique ID of the new customer. This must be a
                            string representation of a 64-bit unsigned integer.
                            Generated randomly if not provided. Optional.
        :type customer_id: str
        :param title: The customer's title. Defaults to CUSTOMER_TITLE_UNKNOWN.
                      Optional.
        :type title: :class:`tmvault.enums.CustomerTitle`
        :param first_name: The customer's first name. Optional.
        :type first_name: str
        :param middle_name: The customer's middle name. Optional.
        :type middle_name: str
        :param last_name: The customer's last name. Optional.
        :type last_name: str
        :param dob: The customer's date of birth. Optional.
        :type dob: :class:`datetime.date`
        :param gender: The customer's gender. Optional.
        :type gender: :class:`tmvault.enums.CustomerGender`
        :param nationality: The customer's nationality. Optional.
        :type nationality: str
        :param email_address: The customer's email address. It must be a valid
                              email address. If provided, this will be set as
                              an identifier for the customer. Optional.
        :type email_address: str
        :param mobile_phone_number: The customer's mobile phone number. It
                                    must be a valid telephone number.
                                    Optional.
        :type mobile_phone_number: str
        :param home_phone_number: The customer's home phone number. It must be
                                  a valid telephone number, defaults to None.
        :type home_phone_number: str, optional
        :param business_phone_number: The customer's business phone number. It
                                      must be a valid telephone number,
                                      defaults to None.
        :type business_phone_number: str, optional
        :param contact_method: The customer's preferred method of contact,
                               defaults to CUSTOMER_CONTACT_METHOD_NONE.
        :type contact_method: :class:`tmvault.enums.CustomerContactMethod`,
                              optional
        :param country_of_residence: The customer's country of residence,
                                     defaults to None.
        :type country_of_residence: str, optional
        :param country_of_taxation: The customer's country of taxation,
                                    defaults to None.
        :type country_of_taxation: str, optional
        :param accessibility: The customer's accessibility requirements,
                              defaults to CUSTOMER_ACCESSIBILITY_UNKNOWN.
        :type accessibility: :class:`tmvault.enums.CustomerAccessibility`,
                             optional
        :param additional_details: A string-to-string map of custom additional
                                   customer details, defaults to {}.
        :type additional_details: Dict[str, str], optional
        :return: The created customer.
        :rtype: :class:`tmvault.models.Customer`
        """
        customer_details = {}
        if title is not None:
            customer_details['title'] = title.value
        if first_name is not None:
            customer_details['first_name'] = first_name
        if middle_name is not None:
            customer_details['middle_name'] = middle_name
        if last_name is not None:
            customer_details['last_name'] = last_name
        if dob is not None:
            customer_details['dob'] = str(last_name)
        if gender is not None:
            customer_details['gender'] = gender.value
        if nationality is not None:
            customer_details['nationality'] = nationality
        if email_address is not None:
            customer_details['email_address'] = email_address
        if mobile_phone_number is not None:
            customer_details['mobile_phone_number'] = mobile_phone_number
        if home_phone_number is not None:
            customer_details['home_phone_number'] = home_phone_number
        if business_phone_number is not None:
            customer_details['business_phone_number'] = business_phone_number
        if contact_method is not None:
            customer_details['contact_method'] = contact_method.value
        if country_of_residence is not None:
            customer_details['country_of_residence'] = country_of_residence
        if country_of_taxation is not None:
            customer_details['country_of_taxation'] = country_of_taxation
        if accessibility is not None:
            customer_details['accessibility'] = accessibility.value

        customer = {
            'customer_details': customer_details,
            'identifiers': []
        }
        if customer_id is not None:
            customer['id'] = customer_id
        if email_address is not None:
            customer['identifiers'].append(
                {
                    'identifier_type': 'IDENTIFIER_TYPE_EMAIL',
                    'identifier': email_address
                }
            )
        if additional_details is not None:
            customer['additional_details'] = additional_details

        post_response = self._rest_api.post('/v1/customers', {
            'customer': customer
        })
        return Customer.from_json(post_response)

    def update_customer(
        self,
        customer_id: str,
        title: CustomerTitle = None,
        first_name: str = None,
        middle_name: str = None,
        last_name: str = None,
        dob: date = None,
        gender: CustomerGender = None,
        nationality: str = None,
        email_address: str = None,
        mobile_phone_number: str = None,
        home_phone_number: str = None,
        business_phone_number: str = None,
        contact_method: CustomerContactMethod = None,
        country_of_residence: str = None,
        country_of_taxation: str = None,
        accessibility: CustomerAccessibility = None,
        additional_details_to_upsert: Dict[str, str] = None,
        additional_details_to_remove: List[str] = None
    ) -> Customer:
        """Updates details of an existing customer. The named parameters you
        pass in will be changed on the Customer object.

        :param customer_id: The ID of the customer to update. This is required.
        :type customer_id: str
        :param title: The customer's title, defaults to None.
        :type title: CustomerTitle, optional
        :param first_name: The customer's first name, defaults to None.
        :type first_name: str, optional
        :param middle_name: The customer's middle name, defaults to None.
        :type middle_name: str, optional
        :param last_name: The customer's last name, defaults to None.
        :type last_name: str, optional
        :param dob: The customer's date of birth, defaults to None.
        :type dob: :class:`datetime.date`, optional
        :param gender: The customer's gender, defaults to None.
        :type gender: :class:`tmvault.enums.CustomerGender`, optional
        :param nationality: The customer's nationality, defaults to None.
        :type nationality: str, optional
        :param email_address: The customer's email address. It must be a valid
                              email address, defaults to None.
        :type email_address: str, optional
        :param mobile_phone_number: The customer's mobile phone number. It
                                    must be a valid telephone number, defaults
                                    to None.
        :type mobile_phone_number: str, optional
        :param home_phone_number: The customer's home phone number. It must be
                                  a valid telephone number, defaults to None.
        :type home_phone_number: str, optional
        :param business_phone_number: The customer's business phone number. It
                                      must be a valid telephone number,
                                      defaults to None.
        :type business_phone_number: str, optional
        :param contact_method: The customer's preferred method of contact,
                               defaults to None.
        :type contact_method: :class:`tmvault.enums.CustomerContactMethod`,
                              optional
        :param country_of_residence: The customer's country of residence,
                                     defaults to None.
        :type country_of_residence: str, optional
        :param country_of_taxation: The customer's country of taxation,
                                    defaults to None.
        :type country_of_taxation: str, optional
        :param accessibility: The customer's accessibility requirements,
                              defaults to None.
        :type accessibility: :class:`tmvault.enums.CustomerAccessibility`,
                             optional
        :param additional_details_to_upsert: A string-to-string map of custom
                                             additional customer details to
                                             add or update, defaults to None.
        :type additional_details_to_upsert: Dict[str, str], optional
        :param additional_details_to_remove: A list of keys of existing custom
                                             additional customer details to
                                             remove, defaults to None.
        :type additional_details_to_remove: List[str], optional
        :return: The updated customer.
        :rtype: :class:`tmvault.models.Customer`
        """
        updated_customer_json = None
        if additional_details_to_upsert or additional_details_to_remove:
            put_data = {
                'id': customer_id
            }
            if additional_details_to_upsert:
                put_data['items_to_add'] = additional_details_to_upsert
            if additional_details_to_remove:
                put_data['items_to_remove'] = additional_details_to_remove
            updated_customer_json = self._rest_api.put(
                f'/v1/customers/{customer_id}:updateAdditionalDetails',
                put_data
            )
        update_mask_paths = []
        customer_obj = {}
        customer_details_obj = {}
        if email_address:
            customer_obj['identifiers'] = [
                {
                    "identifier_type": "IDENTIFIER_TYPE_EMAIL",
                    "identifier": email_address
                }
            ]
            update_mask_paths.append('identifiers')
            customer_details_obj['email_address'] = email_address
            update_mask_paths.append('customer_details.email_address')
        if title:
            customer_details_obj['title'] = title.value
            update_mask_paths.append('customer_details.title')
        if first_name:
            customer_details_obj['first_name'] = first_name
            update_mask_paths.append('customer_details.first_name')
        if middle_name:
            customer_details_obj['middle_name'] = middle_name
            update_mask_paths.append('customer_details.middle_name')
        if last_name:
            customer_details_obj['last_name'] = last_name
            update_mask_paths.append('customer_details.last_name')
        if dob:
            customer_details_obj['dob'] = str(dob)
            update_mask_paths.append('customer_details.dob')
        if gender:
            customer_details_obj['gender'] = gender.value
            update_mask_paths.append('customer_details.gender')
        if nationality:
            customer_details_obj['nationality'] = nationality
            update_mask_paths.append('customer_details.nationality')
        if mobile_phone_number:
            customer_details_obj['mobile_phone_number'] = mobile_phone_number
            update_mask_paths.append('customer_details.mobile_phone_number')
        if home_phone_number:
            customer_details_obj['home_phone_number'] = home_phone_number
            update_mask_paths.append('customer_details.home_phone_number')
        if business_phone_number:
            customer_details_obj[
                'business_phone_number'] = business_phone_number
            update_mask_paths.append('customer_details.business_phone_number')
        if contact_method:
            customer_details_obj['contact_method'] = contact_method.value
            update_mask_paths.append('customer_details.contact_method')
        if country_of_residence:
            customer_details_obj['country_of_residence'] = country_of_residence
            update_mask_paths.append('customer_details.country_of_residence')
        if country_of_taxation:
            customer_details_obj['country_of_taxation'] = country_of_taxation
            update_mask_paths.append('customer_details.country_of_taxation')
        if accessibility:
            customer_details_obj['accessibility'] = accessibility.value
            update_mask_paths.append('customer_details.accessibility')

        if len(customer_details_obj) > 0:
            customer_obj['customer_details'] = customer_details_obj

        if len(update_mask_paths) > 0 and len(customer_obj) > 0:
            put_data = {
                'customer': customer_obj,
                'update_mask': {
                    'paths': update_mask_paths
                }
            }
            updated_customer_json = self._rest_api.put(
                '/v1/customers/%s' % customer_id, put_data)

        return (
            Customer.from_json(updated_customer_json)
            if updated_customer_json else self.get_customer(customer_id)
        )
