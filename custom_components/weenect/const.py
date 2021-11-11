"""Constants for weenect."""
from homeassistant.components.binary_sensor import DEVICE_CLASS_CONNECTIVITY
from homeassistant.const import (
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_TIMESTAMP,
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS,
)

# Base component constants
NAME = "Weenect"
DOMAIN = "weenect"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "2.0.2"
ATTRIBUTION = "Data provided by https://my.weenect.com/"
ISSUE_URL = "https://github.com/eifinger/hass-weenect/issues"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
PLATFORMS = ["binary_sensor", "device_tracker", "sensor"]

# Sensors
SENSOR_TYPES = [
    {
        "name": "Update Rate",
        "value_name": "freq_mode",
        "device_class": None,
        "enabled": True,
        "unit_of_measurement": None,
    },
    {
        "name": "Last Update Rate",
        "value_name": "last_freq_mode",
        "device_class": None,
        "enabled": True,
        "unit_of_measurement": None,
    },
    {
        "name": "Sensor Mode",
        "value_name": "sensor_mode",
        "device_class": None,
        "enabled": True,
        "unit_of_measurement": None,
    },
    {
        "name": "Last Sensor Mode",
        "value_name": "last_sensor_mode",
        "device_class": None,
        "enabled": True,
        "unit_of_measurement": None,
    },
]
LOCATION_SENSOR_TYPES = [
    {
        "name": "Battery",
        "value_name": "battery",
        "device_class": DEVICE_CLASS_BATTERY,
        "enabled": True,
        "unit_of_measurement": PERCENTAGE,
    },
    {
        "name": "Cell Tower Id",
        "value_name": "cellid",
        "device_class": None,
        "enabled": True,
        "unit_of_measurement": None,
    },
    {
        "name": "GSM Strength",
        "value_name": "gsm",
        "device_class": DEVICE_CLASS_SIGNAL_STRENGTH,
        "enabled": True,
        "unit_of_measurement": SIGNAL_STRENGTH_DECIBELS,
    },
    {
        "name": "Last Message Received",
        "value_name": "last_message",
        "device_class": DEVICE_CLASS_TIMESTAMP,
        "enabled": True,
        "unit_of_measurement": "ISO8601",
    },
    {
        "name": "GPS Satellites",
        "value_name": "satellites",
        "device_class": None,
        "enabled": True,
        "unit_of_measurement": None,
    },
]

BINARY_SENSOR_TYPES = [
    {
        "name": "Valid Signal",
        "value_name": "valid_signal",
        "device_class": DEVICE_CLASS_CONNECTIVITY,
        "enabled": True,
    },
    {
        "name": "Is Online",
        "value_name": "is_online",
        "device_class": DEVICE_CLASS_CONNECTIVITY,
        "enabled": True,
    },
]

# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_UPDATE_RATE = "update_rate"
DEFAULT_UPDATE_RATE = 30

# Defaults
DEFAULT_NAME = DOMAIN

# Dispatcher identifiers
TRACKER_ADDED = "tracker_added"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
