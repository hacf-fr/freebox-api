class Domain:

    def __init__(self, access):
        self._access = access

    request_cert_schema = {
        'key_type': 'rsa'
    }

    domain_data_schema = {
        'id': ''
    }

    reserve_data_schema = {
        'prefix': '',
        'domain': ''
    }

    async def add_domain(self, domain_data):
        """
        Add domain
        """
        return await self._access.post(f'domain/owned/', domain_data)

    async def delete_domain(self, domain_id):
        """
        Delete domain
        """
        await self._access.delete(f'domain/owned/{domain_id}')

    async def get_domains_configuration(self):
        """
        Get domains configuration
        """
        return await self._access.get('domain/config/')

    async def get_domain(self, domain_id):
        """
        Get domain
        """
        return await self._access.get(f'domain/owned/{domain_id}')

    async def get_domains(self):
        """
        Get domains
        """
        return await self._access.get('domain/owned/')

    async def get_domain_availability(self, domain_name):
        """
        Get domain availability
        """
        return await self._access.get(f'domain/availability/{domain_name}')

    async def import_certificate(self, domain_id, cert_data):
        """
        Import certificate
        """
        return await self._access.post(f'domain/owned/{domain_id}/import_cert', cert_data)

    async def request_certificate(self, domain_id, request_cert_data):
        """
        Request certificate
        """
        return await self._access.post(f'domain/owned/{domain_id}/request_cert', request_cert_data)

    async def reserve_domain(self, reserve_data):
        """
        Reserve domain
        """
        return await self._access.post('domain/reserve/', reserve_data)
