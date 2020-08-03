"""Provides device automations for Crownstone presence sensors."""
from typing import List

import voluptuous as vol

from homeassistant.components.automation import AutomationActionType, state
from homeassistant.components.device_automation import TRIGGER_BASE_SCHEMA
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENTITY_ID,
    CONF_PLATFORM,
    CONF_TYPE,
    STATE_OFF,
    STATE_ON,
)
from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.helpers import config_validation as cv, entity_registry
from homeassistant.helpers.typing import ConfigType

from .const import CONF_USER, DOMAIN, SENSOR_PLATFORM

CROWNSTONE_USERS = set()

TRIGGER_TYPES = {
    "user_entered",
    "user_left",
    "multiple_entered",
    "multiple_left",
    "all_entered",
    "all_left",
}

TRIGGER_SCHEMA = TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_ENTITY_ID): cv.entity_id,
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES),
        vol.Required(CONF_USER): vol.In(CROWNSTONE_USERS),
    }
)


def _get_crownstone_users(hass: HomeAssistant, config_entry_id: str) -> None:
    """Fetch the users for the Crownstone config entry."""
    crownstone_hub = hass.data[DOMAIN][config_entry_id]
    for user in crownstone_hub.sphere.users:
        CROWNSTONE_USERS.add(f"{user.first_name} {user.last_name}")


async def async_get_triggers(hass: HomeAssistant, device_id: str) -> List[dict]:
    """List device triggers for Crownstone devices."""
    registry = await entity_registry.async_get_registry(hass)
    triggers = []

    # Get all the integrations entities for all sensor devices from Crownstone and add triggers
    for entry in entity_registry.async_entries_for_device(registry, device_id):
        if entry.domain == SENSOR_PLATFORM:
            # Get all the Crownstone users from the Crownstone integration
            # Point to the correct config entry for this entity using the config entry id
            _get_crownstone_users(hass, entry.config_entry_id)

            for trigger in TRIGGER_TYPES:
                triggers.append(
                    {
                        CONF_PLATFORM: "device",
                        CONF_DEVICE_ID: device_id,
                        CONF_DOMAIN: DOMAIN,
                        CONF_ENTITY_ID: entry.entity_id,
                        CONF_TYPE: trigger,
                    }
                )

    return triggers


async def async_get_trigger_capabilities(hass: HomeAssistant, config: dict) -> dict:
    """List trigger capabilities."""
    return {
        "extra_fields": vol.Schema({vol.Required(CONF_USER): vol.In(CROWNSTONE_USERS)})
    }


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: AutomationActionType,
    automation_info: dict,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    config = TRIGGER_SCHEMA(config)

    # Implement your own logic to attach triggers.
    # Generally we suggest to re-use the existing state or event
    # triggers from the automation integration.

    if config[CONF_TYPE] == "turned_on":
        from_state = STATE_OFF
        to_state = STATE_ON
    else:
        from_state = STATE_ON
        to_state = STATE_OFF

    state_config = {
        state.CONF_PLATFORM: "state",
        CONF_ENTITY_ID: config[CONF_ENTITY_ID],
        state.CONF_FROM: from_state,
        state.CONF_TO: to_state,
    }
    state_config = state.TRIGGER_SCHEMA(state_config)
    return await state.async_attach_trigger(
        hass, state_config, action, automation_info, platform_type="device"
    )
