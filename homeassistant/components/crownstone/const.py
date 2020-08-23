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
# config
CONF_USER = "user"
CONF_USERS = "users"
# triggers
USER_ENTERED = "user_entered"
USER_LEFT = "user_left"
MULTIPLE_USERS_ENTERED = "multiple_entered"
MULTIPLE_USERS_LEFT = "multiple_left"
ALL_USERS_ENTERED = "all_entered"
ALL_USERS_LEFT = "all_left"
