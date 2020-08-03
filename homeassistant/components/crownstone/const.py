"""Constants for the crownstone integration."""

# Integrations
DOMAIN = "crownstone"
SENSOR_PLATFORM = "sensor"
LIGHT_PLATFORM = "light"

# Config flow
CONF_SPHERE = "sphere"

# Crownstone entity
CROWNSTONE_TYPES = {
    "PLUG": "Crownstone plug",
    "CROWNSTONE_USB": "Crownstone USB",
    "BUILTIN": "Crownstone built-in",
    "BUILTIN_ONE": "Crownstone built-in one",
    "GUIDESTONE": "Crownstone guidestone",
}
CROWNSTONE_EXCLUDE = ["CROWNSTONE_USB", "GUIDESTONE"]

# Presence entity
PRESENCE_SPHERE = {"icon": "mdi:earth", "description": "Sphere presence"}
PRESENCE_LOCATION = {
    "icon": "mdi:map-marker-radius",
    "description": "Location presence",
}

# Device automation
CONF_USER = "user"
