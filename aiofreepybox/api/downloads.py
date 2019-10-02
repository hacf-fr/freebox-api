class Downloads:

    def __init__(self, access):
        self._access = access

    download_advanced_schema = {
        'download_url_list': [''],
        'username': '',
        'password': '',
        'recursive': False,
        'download_dir': ''
    }

    download_url_schema = {
        'download_url': ''
    }

    download_blacklist_data_schema = {
        'host': '',
        'expire': 0
    }

    rss_feed_data_schema = {
        'url': ''
    }

    new_download_tracker_data_schema = {
        'announce': ''
    }

    download_file_priority = [
        'no_dl',
        'low',
        'normal',
        'high'
    ]

    download_file_status = [
        'queued',
        'error',
        'done',
        'downloading'
    ]

    download_ratio_schema = {
        'ratio': 0
    }

    download_state = [
        'stopped',
        'queued',
        'starting',
        'downloading',
        'stopping',
        'error',
        'done',
        'checking',
        'repairing',
        'extracting',
        'seeding',
        'retry'
    ]

    download_state_schema = {
        'status': download_state[0]
    }

    mark_item_as_read_schema = {
        'isRead': True
    }

    async def add_download_advanced(self, download_advanced):
        '''
        Add download advanced
        '''
        await self._access.post('downloads/add/', download_advanced)

    async def add_download_from_file(self, download_file):
        '''
        Add download from file
        '''
        await self._access.post('downloads/add/', download_file)

    async def add_download_from_url(self, download_url):
        '''
        Add download from url
        '''
        await self._access.post('downloads/add/', download_url)

    async def create_download_blacklist_entry(self, download_blacklist_data):
        '''
        Create download blacklist entry
        '''
        await self._access.post('downloads/blacklist/', download_blacklist_data)

    async def create_download_feed(self, rss_feed_data=rss_feed_data_schema):
        '''
        Create download feed
        '''
        return await self._access.post('downloads/feeds/', rss_feed_data)

    async def create_download_tracker(self, download_id, new_download_tracker_data):
        '''
        Create download tracker
        '''
        await self._access.post(f'downloads/{download_id}/trackers/', new_download_tracker_data)

    async def delete_download(self, download_id):
        '''
        Delete download
        '''
        await self._access.delete(f'downloads/{download_id}')

    async def delete_download_blacklist_entry(self, host):
        '''
        Delete download blacklist entry
        '''
        await self._access.delete(f'downloads/blacklist/{host}')

    async def delete_download_erase_files(self, download_id):
        '''
        Delete download erase files
        '''
        await self._access.delete(f'downloads/{download_id}/erase/')

    async def delete_download_feed(self, feed_id):
        '''
        Delete download feed
        '''
        await self._access.delete(f'downloads/feeds/{feed_id}/')

    async def download_feed_item(self, feed_id, item_id):
        '''
        Download feed item
        '''
        await self._access.post(f'downloads/feeds/{feed_id}/items/{item_id}/download/')

    async def download_file(self, file_path):
        '''
        Download file
        '''
        return await self._access.get(f'dl/{file_path}')

    async def edit_download_file(self, download_id, file_id, download_file_data):
        '''
        Edit download file
        '''
        return await self._access.put(f'downloads/{download_id}/files/{file_id}', download_file_data)

    async def edit_download_ratio(self, download_id, download_ratio):
        '''
        Edit download ratio
        '''
        return await self._access.put(f'downloads/{download_id}', download_ratio)

    async def edit_download_state(self, download_id, download_state_data):
        '''
        Edit download state
        '''
        return await self._access.put(f'downloads/{download_id}', download_state_data)

    async def edit_download_tracker(self, download_id, tracker_url, download_tracker_data):
        '''
        Edit download tracker
        '''
        await self._access.put(f'downloads/{download_id}/trackers/{tracker_url}', download_tracker_data)

    async def empty_download_blacklist(self, download_id):
        '''
        Empty download blacklist
        '''
        await self._access.delete(f'downloads/{download_id}/blacklist/empty/')

    async def fetch_download_feed(self, feed_id):
        '''
        Fetch download feed
        '''
        await self._access.post(f'downloads/feeds/{feed_id}/fetch/')

    async def get_download(self, download_id):
        '''
        Get download
        '''
        return await self._access.get(f'downloads/{download_id}')

    async def get_download_blacklist(self, download_id):
        '''
        Get download blacklist
        '''
        return await self._access.get(f'downloads/{download_id}/blacklist/')

    async def get_download_feed_items(self, feed_id):
        '''
        Get download feed items
        '''
        return await self._access.get(f'downloads/feeds/{feed_id}/items/')

    async def get_download_feeds(self, feed_id):
        '''
        Get download feeds
        '''
        return await self._access.get('downloads/feeds/')

    async def get_download_files(self, download_id):
        '''
        Get download files
        '''
        return await self._access.get(f'downloads/{download_id}/files/')

    async def get_download_log(self, download_id):
        '''
        Get download log
        '''
        return await self._access.get(f'downloads/{download_id}/log/')

    async def get_download_peers(self, download_id):
        '''
        Get download peers
        '''
        return await self._access.get(f'downloads/{download_id}/peers/')

    async def get_download_trackers(self, download_id):
        '''
        Get download trackers
        '''
        return await self._access.get(f'downloads/{download_id}/trackers/')

    async def get_downloads(self, download_id):
        '''
        Get downloads
        '''
        return await self._access.get('downloads/')

    async def get_downloads_configuration(self, download_id):
        '''
        Get downloads configuration
        '''
        return await self._access.get('downloads/config/')

    async def mark_download_feed_as_read(self, feed_id):
        '''
        Mark download feed as read
        '''
        await self._access.post(f'downloads/feeds/{feed_id}/mark_all_as_read/')

    async def mark_download_item_as_read(self, feed_id, item_id, mark_item_as_read=mark_item_as_read_schema):
        '''
        Mark download feed item as read
        '''
        await self._access.post(f'downloads/feeds/{feed_id}/items/{item_id}', mark_item_as_read)

    async def remove_download_tracker(self, download_id, tracker_url, download_tracker):
        '''
        Remove download tracker
        '''
        await self._access.delete(f'downloads/{download_id}/trackers/{tracker_url}', download_tracker)

    async def set_downloads_configuration(self, downloads_configuration):
        '''
        Set downloads configuration
        '''
        return await self._access.put('downloads/config/', downloads_configuration)
