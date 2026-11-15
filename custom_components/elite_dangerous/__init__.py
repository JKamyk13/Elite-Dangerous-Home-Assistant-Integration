"""Elite Dangerous Home Assistant integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow

from .api import FrontierApiClient
from .const import DOMAIN
from .coordinator import EliteDangerousCoordinator
from .oauth import FrontierOAuth2Implementation

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Elite Dangerous from a config entry."""
    implementation = FrontierOAuth2Implementation(hass, entry.data["client_id"])
    config_entry_oauth2_flow.async_register_implementation(
        hass, DOMAIN, implementation
    )
    oauth_session = config_entry_oauth2_flow.OAuth2Session(
        hass,
        entry,
        implementation,
    )
    coordinator = EliteDangerousCoordinator(hass, FrontierApiClient(oauth_session))
    entry.runtime_data = coordinator

    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Elite Dangerous config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
