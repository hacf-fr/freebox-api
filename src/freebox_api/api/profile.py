class Profile:
    """
    (The new) API to manage network profiles
    """
    def __init__(self, access):
        self._access = access

    profile_write_parms = { 'name': 'text', 'icon': 'text' }
    profile_data_schema = { 'name': '', 'icon': '/resources/images/profile/profile_01.png' }
    netcontrol_modes = [ 'allowed', 'denied', 'webonly' ]
    cday_values = [ ':fr_bank_holidays', ':fr_school_holidays_a', ':fr_school_holidays_b', ':fr_school_holidays_c', ':fr_school_holidays_corse' ]
    netcontrol_write_parms = { 'override_mode': 'text', 'macs': 'list', 'cdayranges': 'list' }
    netcontrol_data_schema = { 'override_mode': netcontrol_modes[2], 'macs': [], 'cdayranges': [] }
    rule_write_parms = { 'name': 'text', 'mode': 'text', 'start_time': 'int', 'end_time': 'int', 'enabled': 'bool', 'weekdays': 'list' }
    rule_data_schema = { 'name': '', 'mode': netcontrol_modes[1], 'start_time': 0, 'end_time': 0, 'enabled': True, 'weekdays': [] }
    
    async def get_profiles(self):
        """
        Gets all profiles
        """
        return await self._access.get('profile/')

    async def get_profile(self, profile_id):
        """
        Gets all profiles
        """
        return await self._access.get(f"profile/{profile_id}")

    async def add_profile(self, new_profile):
        """
        Adds a profile
        """
        return await self._access.post('profile/', new_profile)

    async def del_profile(self, profile_id):
        """
        Deletes a profile
        """
        return await self._access.delete(f"profile/{profile_id}")

    async def set_profile(self, profile_id, data):
        """
        Configures a profile
        """
        return await self._access.put(f"profile/{profile_id}", payload=data)

    async def get_netcontrols(self):
        """
        Gets network control for all profiles
        """
        return await self._access.get('network_control/')

    async def get_netcontrol(self, profile_id):
        """
        Gets network control for a profile
        """
        return await self._access.get(f"network_control/{profile_id}")

    async def set_netcontrol(self, profile_id, data):
        """
        Sets network control for a profile
        """
        return await self._access.put(f"network_control/{profile_id}", payload=data)
    
    async def override(self, profile_id, duration=0):
        """
        Switch to override mode for the specified duration
        """
        oldconf = self.get_netcontrol(profile_id)
        return await self._access.put(f"network_control/{profile_id}", { 'override': True, 'override_until': duration, 'macs': oldconf['macs'] })

    async def back(self, profile_id):
        """
        Switch to standard mode
        """
        oldconf = self.get_netcontrol(profile_id)
        return await self._access.put(f"network_control/{profile_id}", { 'override': False, 'macs': oldconf['macs'] })

    async def get_migration_status(self):
        """
        Gets migration status
        """
        return await self._access.get('network_control/migrate')

    async def migrate(self):
        """
        Migrates to new version
        """
        return await self._access.post('network_control/migrate', payload=None)

    async def get_netcontrol_rules(self, profile_id):
        """
        Gets all rules for a network control profile
        """
        return await self._access.get(f"network_control/{profile_id}/rules/")

    async def get_netcontrol_rule(self, profile_id, rule_id):
        """
        Gets a rule for a network control profile
        """
        return await self._access.get(f"network_control/{profile_id}/rules/{rule_id}")

    async def add_netcontrol_rule(self, profile_id, new_profile):
        """
        Adds a rule for a network control profile
        """
        if 'weekdays' in new_profile:
            newlist = []
            for day in new_profile['weekdays']: newlist.append(day == 'True')
            new_profile['weekdays'] = newlist
        return await self._access.post(f"network_control/{profile_id}/rules/", new_profile)

    async def set_netcontrol_rule(self, profile_id, rule_id, data):
        """
        Sets a rule for a network control profile
        """
        if 'weekdays' in data:
            newlist = []
            for day in data['weekdays']: newlist.append(day == 'True')
            data['weekdays'] = newlist
        return await self._access.put(f"network_control/{profile_id}/rules/{rule_id}", data)

    async def del_netcontrol_rule(self, profile_id, rule_id):
        """
        Deletes a profile
        """
        return await self._access.delete(f"network_control/{profile_id}/rules/{rule_id}")
