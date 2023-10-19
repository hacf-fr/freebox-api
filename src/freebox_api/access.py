import hmac
import json
import logging
from typing import Any
from typing import Dict
from typing import Optional
from urllib.parse import urljoin

from aiohttp import ClientSession

from freebox_api.exceptions import AuthorizationError
from freebox_api.exceptions import HttpRequestError
from freebox_api.exceptions import InsufficientPermissionsError

logger = logging.getLogger(__name__)


class Access:
    def __init__(
        self,
        session: ClientSession,
        base_url: str,
        app_token: str,
        app_id: str,
        http_timeout: int,
    ):
        self.session = session
        self.base_url = base_url
        self.app_token = app_token
        self.app_id = app_id
        self.timeout = http_timeout
        self.session_token: Optional[str] = None
        self.session_permissions: Optional[Dict[str, bool]] = None

    async def _get_challenge(self, base_url, timeout=10):
        """
        Return challenge from freebox API
        """
        url = urljoin(base_url, "login")
        resp = await self.session.get(url, timeout=timeout)
        resp_data = await resp.json()

        # raise exception if resp.success != True
        if not resp_data.get("success"):
            raise AuthorizationError(
                "Getting challenge failed (APIResponse: {})".format(
                    json.dumps(resp_data)
                )
            )

        return resp_data["result"]["challenge"]

    async def _get_session_token(self, base_url, app_token, app_id, timeout=10):
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
        resp = await self.session.post(url, data=data, timeout=timeout)
        resp_data = await resp.json()

        # raise exception if resp.success != True
        if not resp_data.get("success"):
            raise AuthorizationError(
                "Starting session failed (APIResponse: {})".format(
                    json.dumps(resp_data)
                )
            )

        session_token = resp_data["result"].get("session_token")
        session_permissions = resp_data["result"].get("permissions")

        return (session_token, session_permissions)

    async def _refresh_session_token(self):
        # Get token for the current session
        session_token, session_permissions = await self._get_session_token(
            self.base_url, self.app_token, self.app_id, self.timeout
        )

        logger.info("Session opened")
        logger.info("Permissions: " + str(session_permissions))
        self.session_token = session_token
        self.session_permissions = session_permissions

    def _get_headers(self) -> Dict[str, Optional[str]]:
        return {"X-Fbx-App-Auth": self.session_token}

    async def _perform_request(self, verb, end_url, **kwargs):
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
        resp = await verb(url, **request_params)

        # Return response if content is not json
        if resp.content_type != "application/json":
            return resp

        resp_data = await resp.json()
        if resp_data.get("error_code") in ["auth_required", "invalid_session"]:
            logger.debug("Invalid session")
            await self._refresh_session_token()
            request_params["headers"] = self._get_headers()
            resp = await verb(url, **request_params)
            resp_data = await resp.json()

        if not resp_data["success"]:
            err_msg = "Request failed (APIResponse: {})".format(json.dumps(resp_data))
            if resp_data.get("error_code") == "insufficient_rights":
                raise InsufficientPermissionsError(err_msg)
            raise HttpRequestError(err_msg)

        return resp_data.get("result")

    async def get(
        self, end_url: str
    ) -> Any:  # Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Send get request and return results
        """
        return await self._perform_request(self.session.get, end_url)

    async def post(
        self, end_url: str, payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send post request and return results
        """
        data = json.dumps(payload) if payload else None
        return await self._perform_request(self.session.post, end_url, data=data)  # type: ignore

    async def put(
        self, end_url: str, payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send post request and return results
        """
        data = json.dumps(payload) if payload else None
        return await self._perform_request(self.session.put, end_url, data=data)  # type: ignore

    async def delete(
        self, end_url: str, payload: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, bool]]:
        """
        Send delete request and return results
        """
        data = json.dumps(payload) if payload else None
        return await self._perform_request(self.session.delete, end_url, data=data)  # type: ignore

    async def get_permissions(self) -> Optional[Dict[str, bool]]:
        """
        Returns the permissions for this session/app.
        """
        if not self.session_permissions:
            await self._refresh_session_token()
        return self.session_permissions
