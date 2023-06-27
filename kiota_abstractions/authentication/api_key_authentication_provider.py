from enum import Enum
from typing import List
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from kiota_abstractions.authentication import AllowedHostsValidator, AuthenticationProvider
from kiota_abstractions.request_information import RequestInformation


class KeyLocation(Enum):
    """
    Defines the locations a key can be used.
    """

    QueryParameter = "query_parameter"
    Header = "header"


class ApiKeyAuthenticationProvider(AuthenticationProvider):
    """
    Adds an API Key to the request.
    """

    def __init__(
        self,
        key_location: KeyLocation,
        api_key: str,
        parameter_name: str,
        allowed_hosts: List[str] = [],
    ) -> None:
        if not isinstance(key_location, KeyLocation):
            raise ValueError(f"key_location can only be 'query_parameter' or 'header'")

        if not all([isinstance(api_key, str), api_key]):
            raise ValueError(
                f"api_key can only be a string but you supplied {api_key!r}"
            )

        if not all([isinstance(parameter_name, str), parameter_name]):
            raise ValueError(
                f"parameter_name can only be a string but you supplied {parameter_name!r}"
            )

        self.key_location = key_location
        self.api_key = api_key
        self.parameter_name = parameter_name
        self.allowed_hosts_validator = AllowedHostsValidator(allowed_hosts)

    async def authenticate_request(self, request: RequestInformation) -> None:
        """
        Ensures that the API key is placed in the correct location for a request.
        """
        if request is None:
            raise ValueError(f"request can not be empty")

        if not self.allowed_hosts_validator.is_url_host_valid(request.url):
            raise ValueError(f"{request.url!r} is not a valid URL")

        if self.key_location == KeyLocation.QueryParameter:
            url_parts = list(urlparse(request.url))
            query = dict(parse_qsl(url_parts[4]))
            query.update({self.parameter_name: self.api_key})
            url_parts[4] = urlencode(query)
            request.url = urlunparse(url_parts)
        elif self.key_location == KeyLocation.Header:
            request.add_request_headers({self.parameter_name: self.api_key})
        return
