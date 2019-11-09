import hmac
import json
import logging
from asyncio import TimeoutError
from urllib.parse import urljoin
from aiofreepybox.exceptions import (
    AuthorizationError,
    HttpRequestError,
    InsufficientPermissionsError,
)

from aiohttp.client import ClientSession
from typing import Any, Callable, Dict, Optional, Tuple, Union

_DEFAULT_TIMEOUT = 10
_LOGGER = logging.getLogger(__name__)


class Access:
    """
    Access
    """

    def __init__(
        self,
        session: ClientSession,
        base_url: str,
        app_token: str,
        app_id: str,
        http_timeout: int,
    ) -> None:
        self.session = session
        self.base_url = base_url
        self.app_token = app_token
        self.app_id = app_id
        self.timeout = http_timeout
        self.session_token: Optional[str] = None
        self.session_permissions: Optional[str] = None

    async def _get_challenge(
        self, base_url: str, timeout: int = _DEFAULT_TIMEOUT
    ) -> str:
        """
        Return challenge from freebox API
        """

        url = urljoin(base_url, "login")
        async with self.session.get(url, timeout=timeout) as r:
            resp = await r.json()

        # raise exception if resp.success != True
        if not resp.get("success"):
            raise AuthorizationError(
                "Getting challenge failed (APIResponse: {})".format(json.dumps(resp))
            )

        return resp["result"]["challenge"]

    async def _get_session_token(
        self,
        base_url: str,
        app_token: str,
        app_id: str,
        timeout: int = _DEFAULT_TIMEOUT,
    ) -> Tuple[str, str]:
        """
        Get session token from freebox.
        Returns (session_token, session_permissions)
        """

        # Get challenge from API
        challenge = await self._get_challenge(base_url, timeout)

        # Hash app_token with chalenge key to get the password
        h = hmac.new(app_token.encode(), challenge.encode(), "sha1")
        password = h.hexdigest()

        url = urljoin(base_url, "login/session/")
        data = json.dumps({"app_id": app_id, "password": password})
        async with await self.session.post(url, data=data, timeout=timeout) as r:
            resp = await r.json()

        # raise exception if resp.success != True
        if not resp.get("success"):
            raise AuthorizationError(
                "Starting session failed (APIResponse: {})".format(json.dumps(resp))
            )

        session_token, session_permissions = (
            resp.get("result").get("session_token"),
            resp.get("result").get("permissions"),
        )
        return session_token, session_permissions

    async def _refresh_session_token(self) -> None:
        """Refresh session token"""

        # Get token for the current session
        self.session_token, self.session_permissions = await self._get_session_token(
            self.base_url, self.app_token, self.app_id, self.timeout
        )
        _LOGGER.info("Session opened")
        _LOGGER.debug("Permissions: " + str(self.session_permissions))

    def _get_headers(self) -> Dict[str, Optional[str]]:
        """Get headers"""
        return {"X-Fbx-App-Auth": self.session_token}

    async def _perform_request(self, verb: Callable, end_url: str, **kwargs) -> Any:
        """
        Perform the given request, refreshing the session token if needed
        """
        if not self.session_token:
            await self._refresh_session_token()

        url = urljoin(self.base_url, end_url)
        request_params = {
            **kwargs,
            "headers": self._get_headers(),
            "timeout": self.timeout,
        }
        try:
            r = await verb(url, **request_params)
        except TimeoutError as e:
            raise HttpRequestError(e)

        # Return response if content is not json
        if r.content_type != "application/json":
            return r
        resp = await r.json()

        if resp.get("error_code") in ["auth_required", "invalid_session"]:
            _LOGGER.debug("Invalid session")
            self.session_token = None
            return await self._perform_request(verb, end_url, **kwargs)

        # Check for 'result' response success
        if not resp["success"] if "success" in resp else True:
            # Check for 'data' response success
            if not resp["error"] if "error" in resp else False:
                # Return 'data' response
                return resp.get("data", None)

            error_message = "Request failed (APIResponse: {})".format(json.dumps(resp))
            if resp.get("error_code") in ["insufficient_rights", "access_denied"]:
                raise InsufficientPermissionsError(error_message)
            raise HttpRequestError(error_message)

        # Return 'result' response
        return resp.get("result", None)

    async def get(self, end_url: str, params_url: Optional[str] = None) -> Any:
        """
        Send get request and return results
        """
        params = params_url if params_url is not None else None
        return await self._perform_request(self.session.get, end_url, params=params)

    async def post(self, end_url: str, payload: Optional[str] = None) -> Any:
        """
        Send post request and return results
        """
        data = json.dumps(payload) if payload is not None else None
        return await self._perform_request(self.session.post, end_url, data=data)

    async def put(self, end_url: str, payload: Optional[str] = None) -> Any:
        """
        Send post request and return results
        """
        data = json.dumps(payload) if payload is not None else None
        return await self._perform_request(self.session.put, end_url, data=data)

    async def delete(self, end_url: str, payload: Optional[str] = None) -> Any:
        """
        Send delete request and return results
        """
        data = json.dumps(payload) if payload is not None else None
        return await self._perform_request(self.session.delete, end_url, data=data)

    async def get_permissions(self) -> Optional[str]:
        """
        Returns the permissions for this session/app.
        """
        if not self.session_permissions:
            await self._refresh_session_token()
        return self.session_permissions
