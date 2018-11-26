import hmac
import json
import logging
from urllib.parse import urljoin
from aiofreepybox.exceptions import *

logger = logging.getLogger(__name__)

class Access:
    def __init__(self, session, base_url, app_token, app_id, http_timeout):
        self.session = session
        self.base_url = base_url
        self.app_token = app_token
        self.app_id = app_id
        self.timeout = http_timeout
        self.session_token = None

    async def _get_challenge(self, base_url, timeout=10):
        '''
        Return challenge from freebox API
        '''
        url = urljoin(base_url, 'login')
        r = await self.session.get(url, timeout=timeout)
        resp = await r.json()

        # raise exception if resp.success != True
        if not resp.get('success'):
            raise AuthorizationError('Getting challenge failed (APIResponse: {0})'
                                     .format(json.dumps(resp)))

        return resp['result']['challenge']

    async def _get_session_token(self, base_url, app_token, app_id, timeout=10):
        """
        Get session token from freebox.
        Returns (session_token, session_permissions)
        """
        # Get challenge from API
        challenge = await self._get_challenge(base_url, timeout)

        # Hash app_token with chalenge key to get the password
        h = hmac.new(app_token.encode(), challenge.encode(), 'sha1')
        password = h.hexdigest()

        url = urljoin(base_url, 'login/session/')
        data = json.dumps({'app_id': app_id, 'password': password})
        r = await self.session.post(url, data=data, timeout=timeout)
        resp = await r.json()

        # raise exception if resp.success != True
        if not resp.get('success'):
            raise AuthorizationError('Starting session failed (APIResponse: {0})'
                                     .format(json.dumps(resp)))

        session_token = resp.get('result').get('session_token')
        session_permissions = resp.get('result').get('permissions')

        return(session_token, session_permissions)

    async def _refresh_session_token(self):
        # Get token for the current session
        session_token, session_permissions = await self._get_session_token(
            self.base_url,
            self.app_token,
            self.app_id,
            self.timeout)

        logger.info('Session opened')
        logger.info('Permissions: ' + str(session_permissions))
        self.session_token = session_token

    async def get(self, end_url):
        '''
        Send get request and return results
        '''
        if not self.session_token:
            await self._refresh_session_token()
        url = urljoin(self.base_url, end_url)
        r = await self.session.get(url, headers={'X-Fbx-App-Auth': self.session_token}, timeout=self.timeout)
        resp = await r.json()

        if resp.get('error_code') == 'auth_required':
            await self._refresh_session_token()
            r = await self.session.get(url, headers={'X-Fbx-App-Auth': self.session_token}, timeout=self.timeout)
            resp = await r.json()

        if not resp['success']:
            raise HttpRequestError('GET request failed (APIResponse: {0})'
                                   .format(json.dumps(resp)))

        return resp['result'] if 'result' in resp else None

    async def post(self, end_url, payload=None):
        '''
        Send post request and return results
        '''
        if not self.session_token:
            await self._refresh_session_token()
        url = urljoin(self.base_url, end_url)
        data = json.dumps(payload) if payload is not None else None
        r = await self.session.post(url, headers={'X-Fbx-App-Auth': self.session_token}, data=data, timeout=self.timeout)
        resp = await r.json()

        if resp.get('error_code') == 'auth_required':
            await self._refresh_session_token()
            r = await self.session.post(url, headers={'X-Fbx-App-Auth': self.session_token}, data=data, timeout=self.timeout)
            resp = await r.json()
        if not resp['success']:
            raise HttpRequestError('POST request failed (APIResponse: {0})'
                                   .format(json.dumps(resp)))

        return resp['result'] if 'result' in resp else None

    async def put(self, end_url, payload=None):
        '''
        Send post request and return results
        '''
        if not self.session_token:
            await self._refresh_session_token()
        url = urljoin(self.base_url, end_url)
        data = json.dumps(payload) if payload is not None else None
        r = await self.session.put(url, headers=self.header, data=data, timeout=self.timeout)
        resp = await r.json()

        if resp.get('error_code') == 'auth_required':
            await self._refresh_session_token()
            r = await self.session.put(url, headers={'X-Fbx-App-Auth': self.session_token}, data=data, timeout=self.timeout)
            resp = await r.json()
        if not resp['success']:
            raise HttpRequestError('PUT request failed (APIResponse: {0})'
                                   .format(json.dumps(resp)))

        return resp['result'] if 'result' in resp else None
