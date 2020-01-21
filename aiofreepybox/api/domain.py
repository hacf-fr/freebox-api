from typing import Any, Dict, List, Optional


class Domain:
    """
    Domain
    """

    def __init__(self, access) -> None:
        self._access = access

    request_cert_schema = {"key_type": "rsa"}
    domain_data_schema = {"id": ""}
    reserve_data_schema = {"prefix": "", "domain": ""}

    async def add_domain(self, domain_data: Dict[str, str]):
        """
        Add domain

        domain_data : `dict`
        """
        return await self._access.post(f"domain/owned/", domain_data)

    async def delete_domain(self, domain_id: int) -> None:
        """
        Delete domain

        domain_id : `int`
        """
        await self._access.delete(f"domain/owned/{domain_id}")

    async def get_domains_configuration(self) -> Dict[str, Any]:
        """
        Get domains configuration
        """
        return await self._access.get("domain/config/")

    async def get_domain(self, domain_id: str) -> Dict[str, Any]:
        """
        Get domain

        domain_id : `str`
        """
        return await self._access.get(f"domain/owned/{domain_id}")

    async def get_domains(self) -> List[Dict[str, Any]]:
        """
        Get domains
        """
        return await self._access.get("domain/owned/")

    async def get_domain_availability(self, domain_name: str):
        """
        Get domain availability

        domain_name : `str`
        """
        return await self._access.get(f"domain/availability/{domain_name}")

    async def import_certificate(self, domain_id: int, cert_data: str):
        """
        Import certificate

        domain_id : `int`
        cert_data : `str`
        """
        return await self._access.post(
            f"domain/owned/{domain_id}/import_cert", cert_data
        )

    async def request_certificate(
        self, domain_id: int, request_cert_data: Optional[Dict[str, str]] = None
    ):
        """
        Request certificate

        domain_id : `int`
        request_cert_data : `dict`
        """
        if request_cert_data is None:
            request_cert_data = self.request_cert_schema
        return await self._access.post(
            f"domain/owned/{domain_id}/request_cert", request_cert_data
        )

    async def reserve_domain(self, reserve_data: Dict[str, str]):
        """
        Reserve domain

        reserve_data : `dict`
        """
        return await self._access.post("domain/reserve/", reserve_data)
