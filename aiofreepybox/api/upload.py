class Upload:

    def __init__(self, access):
        self._access = access

    async def cancel_upload(self, upload_id):
        '''
        Cancel upload
        '''
        await self._access.delete(f'upload/{upload_id}/cancel')

    async def clean_uploads(self):
        '''
        Clean upload
        '''
        await self._access.delete(f'upload/clean')

    async def delete_upload(self, upload_id):
        '''
        Delete upload
        '''
        await self._access.delete(f'upload/{upload_id}')

    async def get_uploads(self):
        '''
        Get uploads
        '''
        return await self._access.get('upload/')

    async def get_upload(self, upload_id):
        '''
        Get upload
        '''
        return await self._access.get(f'upload/{upload_id}')


"""     async def upload_file(self, upload_file_start):
        '''
        Upload file need websocket api
        '''
        return await None """
