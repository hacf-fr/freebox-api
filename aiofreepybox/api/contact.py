from typing import Any, Dict, List, Optional

from aiohttp.client_reqrep import ClientResponse

from aiofreepybox.access import Access


class Contact:
    """
    Contact
    """

    def __init__(self, access: Access) -> None:
        self._access = access

    add_to_group_schema = {"group_id": 1, "contact_id": 1}
    contact_object_type = ["numbers", "emails", "urls", "addresses"]
    group_schema = {"id": 0, "name": "", "nb_contact": 0}
    import_contacts_schema = {"empty_before_adding": False, "contacts": [""]}
    import_contacts_vcard_formats = ["vcard", "ldif", "csv"]
    import_contacts_vcard_schema = {
        "file": "",
        "format": import_contacts_vcard_formats[0],
        "removeall": 0,
    }
    photo_url_schema = {"photo_url": ""}

    async def add_contact(
        self, contact_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Add contact

        contact_data : `dict`
        """
        return await self._access.post("contact/", contact_data)

    async def add_to_group(self, add_to_group: Dict[str, Any]) -> None:
        """
        Add to group

        add_to_group : `dict`
        """
        return await self._access.post("contact/addtogroup", add_to_group)

    async def create_contact_object(
        self, contact_id: int, contact_data, contact_object_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Create contact object

        contact_id : `int`
        contact_data : `dict`
        contact_object_type : `str`
        """
        return await self._access.post(
            f"contact/{contact_id}/{contact_object_type}", contact_data
        )

    async def create_group(
        self, group_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create group

        group_data : `dict`
        """
        return await self._access.post("group/", group_data)

    async def delete_contact_object(
        self, contact_id: int, contact_object_type: str
    ) -> None:
        """
        Delete contact object

        contact_id : `int`
        contact_object_type : `str`
        """
        await self._access.delete(f"contact/{contact_id}/{contact_object_type}")

    async def delete_group(self, group_id: int) -> None:
        """
        Delete group

        group_id : `int`
        """
        await self._access.delete(f"group/{group_id}")

    async def edit_contact_object(
        self, contact_id: int, contact_data: Dict[str, Any], contact_object_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Edit contact object

        contact_id : `int`
        contact_data : `dict`
        contact_object_type : `str`
        """
        return await self._access.put(
            f"contact/{contact_id}/{contact_object_type}", contact_data
        )

    async def export_contacts(self) -> Optional[ClientResponse]:
        """
        Export contacts to vcf format
        """
        return await self._access.get("contact/export/")

    async def get_contact(self, contact_id: int) -> Optional[Dict[str, Any]]:
        """
        Get contact

        contact_id : `int`
        """
        return await self._access.get(f"contact/{contact_id}")

    async def get_contact_data(
        self, contact_id: int, contact_object_type: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get contact data

        contact_id : `int`
        contact_object_type : `str`
        """
        return await self._access.get(f"contact/{contact_id}/{contact_object_type}")

    async def get_contacts(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get contacts
        """
        return await self._access.get("contact/")

    async def get_contacts_count(self) -> Optional[int]:
        """
        Get contacts count
        """
        return await self._access.get("contact/count")

    async def get_contact_groups(self) -> Optional[Dict[Any, Any]]:
        """
        Get contacts groups
        """
        return await self._access.get("contact/groups")

    async def get_group(self, group_id: int) -> Optional[Dict[str, Any]]:
        """
        Get group

        group_id : `int`
        """
        return await self._access.get(f"group/{group_id}")

    async def get_groups(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get groups
        """
        return await self._access.get("group/?page=1&start=0&limit=200")

    async def import_contacts_step1(
        self, import_contacts_vcard: Dict[Any, Any]
    ) -> Optional[Dict[Any, Any]]:
        """
        Import contacts step 1

        import_contacts_vcard : `str`
        """
        return await self._access.post("contact/import/step1/", import_contacts_vcard)

    async def import_contacts_step2(
        self, import_contacts: Dict[Any, Any]
    ) -> Optional[Dict[Any, Any]]:
        """
        Import contacts step 2

        import_contacts : `dict`
        """
        return await self._access.post("contact/import/step2/", import_contacts)

    async def remove_from_group(
        self, remove_from_group: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Remove from group

        remove_from_group : `dict`
        """
        return await self._access.post("contact/removefromgroup", remove_from_group)

    async def update_contact(
        self, contact_id: int, contact_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update contact

        contact_id : `int`
        contact_data : `dict`
        """
        return await self._access.put(f"contact/{contact_id}", contact_data)

    async def update_contact_photo(
        self, contact_id: int, photo_url: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update contact photo

        contact_id : `int`
        photo_url : `dict`
        """
        return await self._access.put(f"contact/{contact_id}/update_photo/", photo_url)
