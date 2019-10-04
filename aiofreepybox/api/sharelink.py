class Sharelink:

    def __init__(self, access):
        self._access = access

    share_link_data_schema = {
        'path': '',
        'expire': 0
    }

    async def create_share_link(self, share_link_data=share_link_data_schema):
        """
        Create share link
        """
        return await self._access.post('share_link/', share_link_data)

    async def delete_share_link(self, token):
        """
        Delete share link
        """
        await self._access.delete(f'share_link/{token}')

    async def get_share_links(self):
        """
        Get share links
        """
        return await self._access.get('share_link/')
