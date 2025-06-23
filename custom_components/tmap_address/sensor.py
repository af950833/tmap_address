from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.restore_state import RestoreEntity
import aiohttp
import async_timeout
import logging
from datetime import timedelta
import asyncio

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensor through config entry."""
    coordinator = TmapDataCoordinator(hass, config_entry)
    await asyncio.sleep(10)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([TmapAddressSensor(coordinator, config_entry)])

class TmapDataCoordinator(DataUpdateCoordinator):
    """Data update coordinator for TMAP API."""

    def __init__(self, hass, config_entry):
        super().__init__(
            hass,
            _LOGGER,
            name="TMAP Address",
            update_interval=timedelta(
                seconds=config_entry.data.get("scan_interval", 900)
            ),
        )
        self.config_entry = config_entry

    async def _async_update_data(self):
        """Fetch data from TMAP API."""
        try:
            target_entity = self.config_entry.data["target_entity"]
            
            # Get coordinates from entities
            target_state = self.hass.states.get(target_entity)
            
            if not target_state:
                raise UpdateFailed("Entity not found")
                
            target_lon = target_state.attributes.get("longitude")
            target_lat = target_state.attributes.get("latitude")

            if None in (target_lon, target_lat):
                raise UpdateFailed("Invalid coordinates")

            # API request configuration
            headers = {
                "appKey": self.config_entry.data["api_key"],
                "Accept": "application/json"
            }
            
            payload = {
                "lon": target_lon,
                "lat": target_lat
            }

            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    response = await session.get(
                        "https://apis.openapi.sk.com/tmap/geo/reversegeocoding?version=1&addressType=A04",
                        headers=headers,
                        params=payload
                    )
                    result = await response.json()

            if response.status != 200:
                raise UpdateFailed(f"API Error: {result.get('errorMessage', 'Unknown error')}")

            address = result["addressInfo"]["fullAddress"]
            return address

        except Exception as e:
            raise UpdateFailed(f"Error updating address: {str(e)}")

class TmapAddressSensor(SensorEntity, RestoreEntity):
    """Representation of a TMAP Address sensor."""

    def __init__(self, coordinator, config_entry):
        self.coordinator = coordinator
        self._config_entry = config_entry
        self._attr_unique_id = f"tmap_address_{config_entry.entry_id}"
        self._attr_name = config_entry.data["name"]
        self._attr_icon = "mdi:map-marker"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator.data if self.coordinator.data else None

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(
                self.async_write_ha_state
            )
        )
      
