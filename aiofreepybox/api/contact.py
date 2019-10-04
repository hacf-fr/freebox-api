class Contact:

    def __init__(self, access):
        self._access = access

    contact_object_type = [
        'numbers',
        'emails',
        'urls',
        'addresses'
    ]

    add_to_group_schema = {
        'group_id': 1,
        'contact_id': 1
    }

    import_contacts_schema = {
        'emptyBeforeAdding': False,
        'contacts': ['']
    }

    photo_url_schema = {
        'photo_url': ''
    }

    async def add_contact(self, contact_data):
        '''
        Add contact
        '''
        return await self._access.post('contact/', contact_data)

    async def add_to_group(self, add_to_group):
        '''
        Add to group
        '''
        return await self._access.post('contact/addtogroup', add_to_group)

    async def create_contact_object(self, contact_id, contact_data, contact_object_type=None):
        '''
        Create contact object
        '''
        if contact_object_type is None:
            contact_object_type = self.contact_object_type[0]
        return await self._access.post(f'contact/{contact_id}/{contact_object_type}', contact_data)

    async def delete_contact_object(self, contact_id, contact_object_type=None):
        '''
        Delete contact object
        '''
        if contact_object_type is None:
            contact_object_type = self.contact_object_type[0]
        await self._access.delete(f'contact/{contact_id}/{contact_object_type}')

    async def edit_contact_object(self, contact_id, contact_data, contact_object_type=None):
        '''
        Edit contact object
        '''
        if contact_object_type is None:
            contact_object_type = self.contact_object_type[0]
        return await self._access.put(f'contact/{contact_id}/{contact_object_type}', contact_data)

    async def export_contacts(self):
        '''
        Export contacts to vcf format
        '''
        return await self._access.post('contact/export/')

    async def get_contact(self, contact_id):
        '''
        Get contact
        '''
        return await self._access.get(f'contact/{contact_id}')

    async def get_contact_data(self, contact_id, contact_object_type=None):
        '''
        Get contact data
        '''
        if contact_object_type is None:
            contact_object_type = self.contact_object_type[0]
        return await self._access.get(f'contact/{contact_id}/{contact_object_type}')

    async def get_contacts(self):
        '''
        Get contacts
        '''
        return await self._access.get('contact/')

    async def get_contacts_count(self):
        '''
        Get contacts count
        '''
        return await self._access.get('contact/count')

    async def get_groups(self):
        '''
        Get contacts groups
        '''
        return await self._access.get('contact/groups')

    async def import_contacts_step1(self, import_contacts_vcard):
        '''
        Import contacts step 1
        '''
        return await self._access.post('contact/import/step1/', import_contacts_vcard)

    async def import_contacts_step2(self, import_contacts):
        '''
        Import contacts step 2
        '''
        return await self._access.post('contact/import/step2/', import_contacts)

    async def remove_from_group(self, remove_from_group=add_to_group_schema):
        '''
        Remove from group
        '''
        return await self._access.post('contact/removefromgroup', remove_from_group)

    async def update_contact(self, contact_id, contact_data):
        '''
        Update contact
        '''
        return await self._access.put(f'contact/{contact_id}', contact_data)

    async def update_contact_photo(self, contact_id, photo_url):
        '''
        Update contact photo
        '''
        return await self._access.put(f'contact/{contact_id}/update_photo/', photo_url)
