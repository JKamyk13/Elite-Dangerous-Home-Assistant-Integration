"""Client for the Frontier Companion API."""

from http import HTTPStatus
from typing import Any

from aiohttp import ClientError

from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session

from .const import CAPI_URL


class FrontierApiError(Exception):
    """Raised when Frontier CAPI returns an invalid response."""


class FrontierApiClient:
    """Fetch commander data from Frontier CAPI."""

    def __init__(self, oauth_session: OAuth2Session) -> None:
        """Initialize the API client."""
        self._oauth_session = oauth_session

    async def async_get_profile(self) -> dict[str, Any]:
        """Fetch the authenticated commander's profile."""
        response_data = await self._async_get("profile")
        if not isinstance(response_data, dict) or not isinstance(
            response_data.get("commander"), dict
        ):
            raise FrontierApiError("Frontier returned an invalid commander profile")
        return response_data

    async def async_get_fleet_carrier(self) -> dict[str, Any] | None:
        """Fetch the commander's fleet carrier data, if available."""
        response_data = await self._async_get("fleetcarrier", optional=True)
        if response_data is not None and not isinstance(response_data, dict):
            raise FrontierApiError("Frontier returned invalid fleet carrier data")
        return response_data

    async def _async_get(
        self, endpoint: str, *, optional: bool = False
    ) -> Any | None:
        """Make an authenticated CAPI request."""
        response = await self._oauth_session.async_request(
            "GET", f"{CAPI_URL}/{endpoint}"
        )
        async with response:
            if optional and response.status in (
                HTTPStatus.NO_CONTENT,
                HTTPStatus.NOT_FOUND,
            ):
                return None
            if response.status != HTTPStatus.OK:
                raise FrontierApiError(
                    f"Frontier CAPI {endpoint} request failed "
                    f"with HTTP {response.status}"
                )
            try:
                return await response.json()
            except (ClientError, ValueError) as err:
                raise FrontierApiError(
                    f"Frontier CAPI {endpoint} returned invalid JSON"
                ) from err
