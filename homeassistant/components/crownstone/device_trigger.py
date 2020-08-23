"""Provides device automations for Crownstone presence sensors."""
from typing import List

import voluptuous as vol

from homeassistant.components.automation import AutomationActionType, template
from homeassistant.components.crownstone.const import (
    ALL_USERS_ENTERED,
    ALL_USERS_LEFT,
    CONF_USER,
    CONF_USERS,
    DOMAIN,
    MULTIPLE_USERS_ENTERED,
    MULTIPLE_USERS_LEFT,
    SENSOR_PLATFORM,
    USER_ENTERED,
    USER_LEFT,
)
from homeassistant.components.crownstone.helpers import set_to_dict
from homeassistant.components.device_automation import TRIGGER_BASE_SCHEMA
from homeassistant.const import (
    CONF_DEVICE,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENTITY_ID,
    CONF_PLATFORM,
    CONF_TYPE,
    CONF_VALUE_TEMPLATE,
)
from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.helpers import config_validation as cv, entity_registry
from homeassistant.helpers.typing import ConfigType

CROWNSTONE_USERS = set()

TRIGGER_TYPES = {
    USER_ENTERED,
    USER_LEFT,
    MULTIPLE_USERS_ENTERED,
    MULTIPLE_USERS_LEFT,
    ALL_USERS_ENTERED,
    ALL_USERS_LEFT,
}

TRIGGER_SCHEMA = TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_ENTITY_ID): cv.entity_id,
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES),
    }
)

TRIGGER_SCHEMA = vol.All(
    cv.key_value_schemas(
        CONF_TYPE,
        {
            USER_ENTERED: TRIGGER_SCHEMA.extend(
                {vol.Required(CONF_USER): vol.In(CROWNSTONE_USERS)}
            ),
            USER_LEFT: TRIGGER_SCHEMA.extend(
                {vol.Required(CONF_USER): vol.In(CROWNSTONE_USERS)}
            ),
            MULTIPLE_USERS_ENTERED: TRIGGER_SCHEMA.extend(
                {
                    vol.Required(CONF_USERS): cv.multi_select(
                        set_to_dict(CROWNSTONE_USERS)
                    )
                }
            ),
            MULTIPLE_USERS_LEFT: TRIGGER_SCHEMA.extend(
                {
                    vol.Required(CONF_USERS): cv.multi_select(
                        set_to_dict(CROWNSTONE_USERS)
                    )
                }
            ),
            ALL_USERS_ENTERED: TRIGGER_SCHEMA,
            ALL_USERS_LEFT: TRIGGER_SCHEMA,
        },
    )
)


def get_crownstone_users(hass: HomeAssistant, config_entry_id: str) -> None:
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
            get_crownstone_users(hass, entry.config_entry_id)

            for trigger in TRIGGER_TYPES:
                triggers.append(
                    {
                        CONF_PLATFORM: CONF_DEVICE,
                        CONF_DEVICE_ID: device_id,
                        CONF_DOMAIN: DOMAIN,
                        CONF_ENTITY_ID: entry.entity_id,
                        CONF_TYPE: trigger,
                    }
                )

    return triggers


async def async_get_trigger_capabilities(hass: HomeAssistant, config: dict) -> dict:
    """List trigger capabilities based on trigger type."""
    if config[CONF_TYPE] in (USER_ENTERED, USER_LEFT):
        return {
            "extra_fields": vol.Schema(
                {vol.Required(CONF_USER): vol.In(CROWNSTONE_USERS)}
            )
        }
    if config[CONF_TYPE] in (MULTIPLE_USERS_ENTERED, MULTIPLE_USERS_LEFT):
        return {
            "extra_fields": vol.Schema(
                {
                    vol.Required(CONF_USERS): cv.multi_select(
                        set_to_dict(CROWNSTONE_USERS)
                    )
                }
            )
        }
    return {}


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: AutomationActionType,
    automation_info: dict,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    config = TRIGGER_SCHEMA(config)

    presence_template = None

    template_config = {
        template.CONF_PLATFORM: "template",
        CONF_VALUE_TEMPLATE: presence_template,
    }
    template_config = template.TRIGGER_SCHEMA(template_config)
    return await template.async_attach_trigger(
        hass, template_config, action, automation_info, platform_type=CONF_DEVICE
    )
