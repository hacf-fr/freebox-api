from typing import Any, List


class Upload:
    """
    Upload
    """

    def __init__(self, access) -> None:
        self._access = access

    async def cancel_upload(self, upload_id: int) -> None:
        """
        Cancel upload

        upload_id : `int`
        """
        await self._access.delete(f"upload/{upload_id}/cancel")

    async def clean_uploads(self) -> None:
        """
        Clean uploads
        """
        await self._access.delete(f"upload/clean")

    async def delete_upload(self, upload_id: int) -> None:
        """
        Delete upload

        upload_id : `int`
        """
        await self._access.delete(f"upload/{upload_id}")

    async def get_uploads(self) -> List[Any]:
        """
        Get uploads
        """
        return await self._access.get("upload/")

    async def get_upload(self, upload_id: int):
        """
        Get upload

        upload_id : `int`
        """
        return await self._access.get(f"upload/{upload_id}")


'''     async def upload_file(self, upload_file_start):
        """
        Upload file need websocket api
        """
        return await None '''
