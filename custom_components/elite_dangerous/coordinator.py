"""Data update coordinator for Elite Dangerous."""

import asyncio
import logging
import time
from typing import Any

from aiohttp import ClientError

from homeassistant.exceptions import (
    ConfigEntryAuthFailed,
    OAuth2TokenRequestError,
    OAuth2TokenRequestReauthError,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import FrontierApiClient, FrontierApiError
from .const import DOMAIN, FLEET_CARRIER_UPDATE_INTERVAL, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class EliteDangerousCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinate rate-limited Frontier CAPI requests."""

    def __init__(self, hass: HomeAssistant, api: FrontierApiClient) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self._api = api
        self._profile: dict[str, Any] | None = None
        self._fleet_carrier: dict[str, Any] | None = None
        self._last_fleet_carrier_request: float | None = None

    async def _async_update_data(self) -> dict[str, Any]:
        """Update one CAPI endpoint per interval to respect Frontier's limits."""
        try:
            await asyncio.wait_for(self._async_fetch_next_endpoint(), timeout=30)
        except OAuth2TokenRequestReauthError as err:
            raise ConfigEntryAuthFailed from err
        except TimeoutError as err:
            raise UpdateFailed("Timed out communicating with Frontier CAPI") from err
        except (ClientError, FrontierApiError, OAuth2TokenRequestError) as err:
            raise UpdateFailed(f"Error communicating with Frontier CAPI: {err}") from err

        return {
            "profile": self._profile,
            "fleet_carrier": self._fleet_carrier,
        }

    async def _async_fetch_next_endpoint(self) -> None:
        """Fetch the profile and carrier on separate polling intervals."""
        now = time.monotonic()
        carrier_due = (
            self._profile is not None
            and (
                self._last_fleet_carrier_request is None
                or now - self._last_fleet_carrier_request
                >= FLEET_CARRIER_UPDATE_INTERVAL.total_seconds()
            )
        )

        if carrier_due:
            self._fleet_carrier = await self._api.async_get_fleet_carrier()
            self._last_fleet_carrier_request = now
        else:
            self._profile = await self._api.async_get_profile()
