"""Sensors for Elite Dangerous."""

from collections.abc import Callable
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import EliteDangerousCoordinator
from .const import DOMAIN

SensorValue = str | int | float | None


def _commander_credits(data: dict[str, Any]) -> SensorValue:
    commander = data["profile"].get("commander") or {}
    return commander.get("credits")


def _current_system(data: dict[str, Any]) -> SensorValue:
    profile = data["profile"]
    ship = profile.get("ship") or {}
    star_system = ship.get("starsystem") or {}
    last_system = profile.get("lastSystem") or {}
    return star_system.get("name") or last_system.get("name")


def _current_station(data: dict[str, Any]) -> SensorValue:
    profile = data["profile"]
    if not (profile.get("commander") or {}).get("docked"):
        return None
    ship = profile.get("ship") or {}
    station = ship.get("station") or {}
    last_starport = profile.get("lastStarport") or {}
    return station.get("name") or last_starport.get("name")


def _current_ship(data: dict[str, Any]) -> SensorValue:
    ship = data["profile"].get("ship") or {}
    return ship.get("shipName") or ship.get("name")


def _fleet_carrier_balance(data: dict[str, Any]) -> SensorValue:
    carrier = data.get("fleet_carrier")
    if carrier is None:
        return None
    return (carrier.get("finance") or {}).get("bankBalance")


SENSOR_DESCRIPTIONS: tuple[
    tuple[SensorEntityDescription, Callable[[dict[str, Any]], SensorValue]], ...
] = (
    (
        SensorEntityDescription(
            key="commander_credits",
            translation_key="commander_credits",
            native_unit_of_measurement="credits",
            icon="mdi:wallet",
        ),
        _commander_credits,
    ),
    (
        SensorEntityDescription(
            key="current_system",
            translation_key="current_system",
            icon="mdi:star-four-points",
        ),
        _current_system,
    ),
    (
        SensorEntityDescription(
            key="current_station",
            translation_key="current_station",
            icon="mdi:space-station",
        ),
        _current_station,
    ),
    (
        SensorEntityDescription(
            key="current_ship",
            translation_key="current_ship",
            icon="mdi:rocket-launch",
        ),
        _current_ship,
    ),
    (
        SensorEntityDescription(
            key="fleet_carrier_balance",
            translation_key="fleet_carrier_balance",
            native_unit_of_measurement="credits",
            icon="mdi:wallet",
        ),
        _fleet_carrier_balance,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Elite Dangerous sensors."""
    coordinator: EliteDangerousCoordinator = entry.runtime_data
    async_add_entities(
        EliteDangerousSensor(coordinator, entry, description, value_fn)
        for description, value_fn in SENSOR_DESCRIPTIONS
    )


class EliteDangerousSensor(
    CoordinatorEntity[EliteDangerousCoordinator], SensorEntity
):
    """Represent an Elite Dangerous value as a sensor."""

    entity_description: SensorEntityDescription

    def __init__(
        self,
        coordinator: EliteDangerousCoordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
        value_fn: Callable[[dict[str, Any]], SensorValue],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._value_fn = value_fn
        self._attr_unique_id = f"{entry.unique_id}_{description.key}"
        self._attr_has_entity_name = True
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.unique_id)},
            name=entry.title,
            manufacturer="Frontier Developments",
            model="Companion API",
        )

    @property
    def native_value(self) -> SensorValue:
        """Return the latest value."""
        if self.coordinator.data is None:
            return None
        return self._value_fn(self.coordinator.data)
