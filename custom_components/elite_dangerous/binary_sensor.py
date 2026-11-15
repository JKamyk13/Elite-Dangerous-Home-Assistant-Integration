"""Binary sensors for Elite Dangerous."""

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import EliteDangerousCoordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Elite Dangerous binary sensors."""
    coordinator: EliteDangerousCoordinator = entry.runtime_data
    async_add_entities([EliteDangerousDockedSensor(coordinator, entry)])


class EliteDangerousDockedSensor(
    CoordinatorEntity[EliteDangerousCoordinator], BinarySensorEntity
):
    """Represent whether the commander is docked."""

    entity_description = BinarySensorEntityDescription(
        key="docked",
        translation_key="docked",
        icon="mdi:space-station",
    )

    def __init__(
        self, coordinator: EliteDangerousCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.unique_id}_docked"
        self._attr_has_entity_name = True
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.unique_id)},
            name=entry.title,
            model="Companion API",
        )

    @property
    def is_on(self) -> bool | None:
        """Return whether the commander is docked."""
        if self.coordinator.data is None:
            return None
        commander = self.coordinator.data["profile"].get("commander") or {}
        return commander.get("docked")
