from pydantic import BaseModel
from typing_extensions import List

from api._base import BaseEndpoint, check_response, create_list_of_items
from api.access._models import Ips
from api.profiles.constants import Endpoints


class AccessFormData(BaseModel):
    """
    Form data for learning new IPs.

    Args:
        ips: List[str] IPv4 or IPv6 addresses
        device_id: str Primary key of the device.

    """

    ips: List[str]
    device_id: str


class AccessEndpoint(BaseEndpoint):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._url = Endpoints.ACCESS

    def list_known_ips(self, device_id: str) -> List[Ips]:
        """List up to latest 50 IPs that were used to query against a Device (resolver).
        https://docs.controld.com/reference/get_access
        """
        response = self._session.get(self._url, params={"device_id": device_id})
        check_response(response)

        data = response.json()

        return create_list_of_items(Ips, data["body"]["ips"])

    def learn_new_ip(self, form_data: AccessFormData) -> bool:
        """Supply an array of IPs to authorize on the device.
        These IPs will be able to use the Legacy DNS IPv4 resolver and have access to proxies.
        If this is a restricted device, then only these IPs will be able to communicate with it.

        https://docs.controld.com/reference/post_access
        """

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self._session.post(self._url, data=form_data.model_dump_json(), headers=headers)
        check_response(response)
        return True

    def delete_learned_ip(self, form_data: AccessFormData) -> bool:
        """Delete a learned IP from the device.

        https://docs.controld.com/reference/delete_access
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self._session.delete(
            self._url, data=form_data.model_dump_json(), headers=headers
        )
        check_response(response)
        return True
