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
        self.session_permissions = None

    async def _get_challenge(self, base_url, timeout=10):
        '''
        Return challenge from freebox API
        '''
        url = urljoin(base_url, 'login')
        r = await self.session.get(url, timeout=timeout)
        resp = await r.json()

        # raise exception if resp.success != True
        if not resp.get('success'):
            raise AuthorizationError('Getting challenge failed (APIResponse: {})'
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
            raise AuthorizationError('Starting session failed (APIResponse: {})'
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
        self.session_permissions = session_permissions

    def _get_headers(self):
        return {'X-Fbx-App-Auth': self.session_token}

    async def _perform_request(self, verb, end_url, **kwargs):
        '''
        Perform the given request, refreshing the session token if needed
        '''
        if not self.session_token:
            await self._refresh_session_token()

        url = urljoin(self.base_url, end_url)
        request_params = {
            **kwargs,
            "headers": self._get_headers(),
            "timeout": self.timeout
        }
        r = await verb(url, **request_params)

        # Return response if content is not json
        if r.content_type != 'application/json':
            return r
        else:
            resp = await r.json()

            if resp.get('error_code') in ['auth_required', "invalid_session"]:
                logger.debug('Invalid session')
                await self._refresh_session_token()
                request_params["headers"] = self._get_headers()
                r = await verb(url, **request_params)
                resp = await r.json()

            if not resp['success']:
                errMsg = 'Request failed (APIResponse: {})'.format(json.dumps(resp))
                if resp.get('error_code') == 'insufficient_rights':
                    raise InsufficientPermissionsError(errMsg)
                else:
                    raise HttpRequestError(errMsg)

            return resp['result'] if 'result' in resp else None

    async def get(self, end_url):
        '''
        Send get request and return results
        '''
        return await self._perform_request(self.session.get, end_url)

    async def post(self, end_url, payload=None):
        '''
        Send post request and return results
        '''
        data = json.dumps(payload) if payload is not None else None
        return await self._perform_request(self.session.post, end_url, data=data)

    async def put(self, end_url, payload=None):
        '''
        Send post request and return results
        '''
        data = json.dumps(payload) if payload is not None else None
        return await self._perform_request(self.session.put, end_url, data=data)

    async def delete(self, end_url, payload=None):
        '''
        Send delete request and return results
        '''
        data = json.dumps(payload) if payload is not None else None
        return await self._perform_request(self.session.delete, end_url, data=data)

    async def get_permissions(self):
        '''
        Returns the permissions for this session/app.
        '''
        if not self.session_permissions:
            await self._refresh_session_token()
        return self.session_permissions
