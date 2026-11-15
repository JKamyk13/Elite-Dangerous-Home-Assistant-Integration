"""Config flow for Elite Dangerous."""

import asyncio
import logging
from typing import Any

from aiohttp import ClientError
import voluptuous as vol

from homeassistant.config_entries import ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.config_entry_oauth2_flow import (
    AbstractOAuth2FlowHandler,
)

from .const import BUILTIN_CLIENT_ID, CAPI_URL, DOMAIN
from .oauth import FrontierOAuth2Implementation

_LOGGER = logging.getLogger(__name__)


class EliteDangerousConfigFlow(AbstractOAuth2FlowHandler, domain=DOMAIN):
    """Handle the OAuth config flow for Elite Dangerous."""

    DOMAIN = DOMAIN

    def __init__(self) -> None:
        """Initialize the config flow."""
        super().__init__()
        self.client_id = ""

    @property
    def logger(self) -> logging.Logger:
        """Return the config flow logger."""
        return _LOGGER

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Ask which public Frontier application client ID to use."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            "client_id_source", default="integration"
                        ): vol.In(
                            {
                                "integration": "Use the integration Client ID",
                                "custom": "Use your own Client ID",
                            }
                        )
                    }
                ),
            )

        if user_input["client_id_source"] == "integration":
            return await self._async_start_auth(BUILTIN_CLIENT_ID)
        return await self.async_step_client_id()

    async def async_step_client_id(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Ask for the user's own public Frontier application Client ID."""
        if user_input is None:
            return self.async_show_form(
                step_id="client_id",
                data_schema=vol.Schema({vol.Required("client_id"): str}),
            )

        client_id = user_input["client_id"].strip()
        if not client_id:
            return self.async_show_form(
                step_id="client_id",
                data_schema=vol.Schema({vol.Required("client_id"): str}),
                errors={"base": "invalid_client_id"},
            )

        return await self._async_start_auth(client_id)

    async def _async_start_auth(self, client_id: str) -> ConfigFlowResult:
        """Start Frontier authorization with the selected Client ID."""
        self.client_id = client_id
        self.flow_impl = FrontierOAuth2Implementation(self.hass, client_id)
        return await self.async_step_auth()

    async def async_oauth_create_entry(self, data: dict[str, Any]) -> ConfigFlowResult:
        """Validate the token with CAPI and create the config entry."""
        token = data["token"]
        session = async_get_clientsession(self.hass)

        try:
            async with asyncio.timeout(30):
                async with session.get(
                    f"{CAPI_URL}/profile",
                    headers={
                        "Authorization": (
                            f"{token.get('token_type', 'Bearer')} "
                            f"{token['access_token']}"
                        )
                    },
                ) as response:
                    if response.status != 200:
                        return self.async_abort(reason="cannot_connect")
                    profile = await response.json()
        except (ClientError, TimeoutError, ValueError) as err:
            _LOGGER.error("Unable to validate the Frontier CAPI profile: %s", err)
            return self.async_abort(reason="cannot_connect")

        commander = profile.get("commander") if isinstance(profile, dict) else None
        if not isinstance(commander, dict):
            return self.async_abort(reason="invalid_profile")

        commander_id = commander.get("id")
        commander_name = commander.get("name")
        if commander_id is None and not commander_name:
            return self.async_abort(reason="invalid_profile")

        await self.async_set_unique_id(str(commander_id or commander_name).casefold())
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"Elite Dangerous ({commander_name or commander_id})",
            data={
                **data,
                "client_id": self.client_id,
            },
        )
