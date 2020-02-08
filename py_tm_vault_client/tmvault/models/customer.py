from datetime import date
import re
from typing import Dict


from ..enums import (
    CustomerAccessibility, CustomerContactMethod, CustomerGender, CustomerTitle
)


class Customer:
    r"""A customer object.

    :ivar id\_: Globally unique ID for the customer.
    :vartype id\_: str
    :ivar title: The customer's title.
    :vartype title: :class:`tmvault.enums.CustomerTitle`
    :ivar first_name: The customer's first name.
    :vartype first_name: str
    :ivar middle_name: The customer's middle name.
    :vartype middle_name: str
    :ivar last_name: The customer's last name.
    :vartype last_name: str
    :ivar dob: The customer's date of birth.
    :vartype dob: :class:`datetime.date`
    :ivar gender: The customer's gender.
    :vartype gender: :class:`tmvault.enums.CustomerGender`
    :ivar nationality: The customer's nationality.
    :vartype nationality: str
    :ivar email_address: The customer's email address.
    :vartype email_address: str
    :ivar mobile_phone_number: The customer's mobile phone number.
    :vartype mobile_phone_number: str
    :ivar home_phone_number: The customer's home phone number.
    :vartype home_phone_number: str
    :ivar business_phone_number: The customer's business phone number.
    :vartype business_phone_number: str
    :ivar contact_method: The customer's preferred method of contact.
    :vartype contact_method: :class:`tmvault.enums.CustomerContactMethod`
    :ivar country_of_residence: The customer's country of residence.
    :vartype country_of_residence: str
    :ivar country_of_taxation: The customer's country of taxation.
    :vartype country_of_taxation: str
    :ivar accessibility: The customer's accessibility requirements.
    :vartype accessibility: :class:`tmvault.enums.CustomerAccessibility`
    :ivar additional_details: A string-to-string dictionary of custom
                              additional customer details.
    :vartype additional_details: Dict[str, str]
    """

    def __init__(self,
                 id_: str,
                 title: CustomerTitle,
                 first_name: str,
                 middle_name: str,
                 last_name: str,
                 dob: date,
                 gender: CustomerGender,
                 nationality: str,
                 email_address: str,
                 mobile_phone_number: str,
                 home_phone_number: str,
                 business_phone_number: str,
                 contact_method: CustomerContactMethod,
                 country_of_residence: str,
                 country_of_taxation: str,
                 accessibility: CustomerAccessibility,
                 additional_details: Dict[str, str]
                 ):
        self.id_ = id_
        self.title = title
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.nationality = nationality
        self.email_address = email_address
        self.mobile_phone_number = mobile_phone_number
        self.home_phone_number = home_phone_number
        self.business_phone_number = business_phone_number
        self.contact_method = contact_method
        self.country_of_residence = country_of_residence
        self.country_of_taxation = country_of_taxation
        self.accessibility = accessibility
        self.additional_details = additional_details

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Customer)
            and self.id_ == other.id_
            and self.title == other.title
            and self.first_name == other.first_name
            and self.middle_name == other.middle_name
            and self.last_name == other.last_name
            and self.dob == other.dob
            and self.gender == other.gender
            and self.nationality == other.nationality
            and self.email_address == other.email_address
            and self.mobile_phone_number == other.mobile_phone_number
            and self.home_phone_number == other.home_phone_number
            and self.business_phone_number == other.business_phone_number
            and self.contact_method == other.contact_method
            and self.country_of_residence == other.country_of_residence
            and self.country_of_taxation == other.country_of_taxation
            and self.accessibility == other.accessibility
            and self.additional_details == other.additional_details
        )

    def __repr__(self) -> str:
        return (
            f'Customer['
            f'id: {self.id_}, '
            f'title: {self.title.name}, '
            f'first_name: {self.first_name}, '
            f'middle_name: {self.middle_name}, '
            f'last_name: {self.last_name}, '
            f'dob: {str(self.dob)}, '
            f'gender: {self.gender.name}, '
            f'nationality: {self.nationality}, '
            f'email_address: {self.email_address}, '
            f'mobile_phone_number: {self.mobile_phone_number}, '
            f'home_phone_number: {self.home_phone_number}, '
            f'business_phone_number: {self.business_phone_number}, '
            f'contact_method: {self.contact_method.name}, '
            f'country_of_residence: {self.country_of_residence}, '
            f'country_of_taxation: {self.country_of_taxation}, '
            f'accessibility: {self.accessibility.name}, '
            f'additional_details: {self.additional_details}'
            f']'
        )

    @classmethod
    def from_json(cls, json_obj: Dict[str, any]):
        customer_details_json_obj = json_obj.get('customer_details', {})
        dob_match = re.match(r'(\d+)-(\d+)-(\d+)',
                             customer_details_json_obj.get('dob', ''))
        dob = (date(int(dob_match[1]), int(dob_match[2]), int(
            dob_match[3])) if dob_match else None)
        return cls(
            id_=json_obj.get('id'),
            title=CustomerTitle(customer_details_json_obj.get(
                'title', CustomerTitle.CUSTOMER_TITLE_UNKNOWN.value)),
            first_name=customer_details_json_obj.get('first_name'),
            middle_name=customer_details_json_obj.get('middle_name'),
            last_name=customer_details_json_obj.get('last_name'),
            dob=dob,
            gender=CustomerGender(customer_details_json_obj.get(
                'gender', CustomerGender.CUSTOMER_GENDER_UNKNOWN.value)),
            nationality=customer_details_json_obj.get('nationality'),
            email_address=customer_details_json_obj.get('email_address'),
            mobile_phone_number=customer_details_json_obj.get(
                'mobile_phone_number'),
            home_phone_number=customer_details_json_obj.get(
                'home_phone_number'),
            business_phone_number=customer_details_json_obj.get(
                'business_phone_number'),
            contact_method=CustomerContactMethod(customer_details_json_obj.get(
                'contact_method',
                CustomerContactMethod.CUSTOMER_CONTACT_METHOD_NONE.value
            )),
            country_of_residence=customer_details_json_obj.get(
                'country_of_residence'),
            country_of_taxation=customer_details_json_obj.get(
                'country_of_taxation'),
            accessibility=CustomerAccessibility(customer_details_json_obj.get(
                'accessibility',
                CustomerAccessibility.CUSTOMER_ACCESSIBILITY_UNKNOWN.value
            )),
            additional_details=json_obj.get('additional_details', {})
        )
