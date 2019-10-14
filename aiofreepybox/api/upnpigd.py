class Upnpigd:

    def __init__(self, access):
        self._access = access

    async def delete_redir(self, redir_id):
        """
        Deletes the given upnpigd redirection

        redir_id : `int`
        """
        return await self._access.delete(f'upnpigd/redir/{redir_id}')

    async def get_configuration(self):
        """
        Get the upnpigd configuration
        """
        return await self._access.get('upnpigd/config/')

    async def get_redirs(self):
        """
        Get the list of upnpigd redirections
        """
        return await self._access.get('upnpigd/redir/')

    async def update_configuration(self, upnpigd_config):
        """
        Update the upnpigd configuration

        upnpigd_config : `dict`
        """
        return await self._access.put('upnpigd/config/', upnpigd_config)
