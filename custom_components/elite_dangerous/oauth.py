"""Frontier OAuth implementation."""

import base64
import hashlib
import secrets

from homeassistant.core import HomeAssistant
from homeassistant.helpers.config_entry_oauth2_flow import (
    LocalOAuth2ImplementationWithPkce,
)

from .const import AUTHORIZATION_URL, DOMAIN, TOKEN_URL


class FrontierOAuth2Implementation(LocalOAuth2ImplementationWithPkce):
    """OAuth 2 implementation using Frontier's PKCE flow."""

    def __init__(self, hass: HomeAssistant, client_id: str) -> None:
        """Initialize the Frontier OAuth implementation."""
        implementation_id = hashlib.sha256(client_id.encode()).hexdigest()[:12]
        super().__init__(
            hass,
            f"{DOMAIN}_{implementation_id}",
            client_id,
            AUTHORIZATION_URL,
            TOKEN_URL,
        )
        self.code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode(
            "ascii"
        )

    @property
    def name(self) -> str:
        """Return the implementation name."""
        return "Frontier Developments"

    @property
    def service_domain(self) -> str:
        """Return the service domain used for OAuth errors."""
        return DOMAIN

    @property
    def extra_authorize_data(self) -> dict[str, str]:
        """Return Frontier-specific authorization parameters."""
        return {
            **super().extra_authorize_data,
            "audience": "frontier",
            "scope": "auth capi",
        }
