import base64


class Sharelink:
    """
    Sharelink
    """

    def __init__(self, access):
        self._access = access

    share_link_data_schema = {"path": "", "expire": 0, "fullurl": ""}

    async def create_share_link(self, path, expire):
        """
        Create share link

        path : `str`
        expire : `int`
        """

        share_link_data = self.share_link_data_schema
        share_link_data["path"] = base64.b64encode(path.encode("utf-8")).decode("utf-8")
        share_link_data["expire"] = expire
        return await self._access.post("share_link/", share_link_data)

    async def delete_share_link(self, token):
        """
        Delete share link

        token : `str`
        """
        await self._access.delete(f"share_link/{token}")

    async def get_share_link(self, token):
        """
        Get a share link
        """
        return await self._access.get(f"share_link/{token}")

    async def get_share_links(self):
        """
        Get share links
        """
        return await self._access.get("share_link/")
