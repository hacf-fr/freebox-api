class Notifications:

    def __init__(self, access):
        self._access = access

    os_type = [
        'android',
        'ios'
    ]

    subscription = [
        'security',
        'wan',
        'downloader',
        'phone'
    ]

    notification_target_data_schema = {
        'id': '',
        'name': '',
        'subscriptions': subscription,
        'token': '',
        'type': os_type[0]
    }

    async def create_notification_target(self, notification_target_data=notification_target_data_schema):
        '''
        Create notification target
        '''
        return await self._access.post('notif/targets/', notification_target_data)

    async def delete_notification_target(self, target_id):
        '''
        Delete notification target
        '''
        await self._access.delete(f'notif/targets/{target_id}')

    async def edit_notification_target(self, target_id, notification_target_data):
        '''
        Edit notification target
        '''
        return await self._access.put(f'notif/targets/{target_id}', notification_target_data)

    async def get_notification_target(self, target_id):
        '''
        Get notification target
        '''
        return await self._access.get(f'notif/targets/{target_id}')
