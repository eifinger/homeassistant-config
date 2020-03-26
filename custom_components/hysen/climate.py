"""
Platform for Hysen Electronic heating Thermostats power by broadlink.
(Beok, Floureon, Decdeal)
As discussed in https://community.home-assistant.io/t/floor-heat-thermostat/29908
             https://community.home-assistant.io/t/beta-for-hysen-thermostats-powered-by-broadlink/56267/55
Author: Mark Carter
"""
#*****************************************************************************************************************************
# Example Homeassistant Config

#climate:
#  - platform: hysen
#    scan_interval: 15
#    device:
#      house_thermostat:
#        name: House Thermostat
#        host: 192.168.0.xx
#        host_dns: dns.name.com
#        host_port: 80
#        mac: '34:EA:36:88:6B:7B'
#        target_temp_default: 20
#        target_temp_step: 0.5        
#        sync_clock_time_per_day: True
#        current_temp_from_sensor_override: 0 # if this is set to 1 always use the internal sensor to report current temp, if 1 always use external sensor to report current temp.
#        update_timeout:5

#*****************************************************************************************************************************

import logging
import binascii
import socket
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import datetime
import time
import random

from homeassistant.const import (ATTR_TEMPERATURE, ATTR_ENTITY_ID, ATTR_UNIT_OF_MEASUREMENT, CONF_NAME, CONF_HOST, CONF_MAC, CONF_TIMEOUT, CONF_CUSTOMIZE, STATE_UNAVAILABLE)

from homeassistant.components.climate import (ClimateDevice, ENTITY_ID_FORMAT, PLATFORM_SCHEMA)

from homeassistant.components.climate.const import (DOMAIN, SUPPORT_TARGET_TEMPERATURE,SUPPORT_PRESET_MODE, HVAC_MODE_OFF, HVAC_MODE_HEAT, HVAC_MODE_AUTO, PRESET_AWAY,
PRESET_NONE,CURRENT_HVAC_HEAT, CURRENT_HVAC_IDLE)

from homeassistant.helpers.entity import async_generate_entity_id

DEFAULT_NAME = 'Hysen Thermostat Controller'

VERSION = '2.0.3'

REQUIREMENTS = ['broadlink==0.13.0']

_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE

DEFAULT_RETRY = 2
DEFAULT_TIMEOUT = 5

CONF_WIFI_SSID = "ssid"
CONF_WIFI_PASSWORD ="password"
CONF_WIFI_SECTYPE = "sectype"
CONF_WIFI_TIMEOUT = "timeout"

SERVICE_SET_WIFI = "hysen_config_wifi"
SET_WIFI_SCHEMA = vol.Schema({
    vol.Optional(ATTR_ENTITY_ID,default="all"): cv.comp_entity_ids,
    vol.Required(CONF_WIFI_SSID): cv.string,
    vol.Required(CONF_WIFI_PASSWORD): cv.string,
    vol.Required(CONF_WIFI_SECTYPE): vol.Range(min=0, max=4),
    vol.Optional(CONF_WIFI_TIMEOUT,default=DEFAULT_TIMEOUT): vol.Range(min=0, max=99),
})

DEFAULT_LOOPMODE = 0                 # 12345,67 = 0   123456,7 = 1  1234567 = 2
                                     # loop_mode refers to index in [ "12345,67", "123456,7", "1234567" ]
                                     # loop_mode = 0 ("12345,67") means Saturday and Sunday follow the "weekend" schedule
                                     # loop_mode = 2 ("1234567") means every day (including Saturday and Sunday) follows the "weekday" schedule

DEFAULT_SENSORMODE = 0               # Sensor mode (SEN) sensor = 0 for internal sensor,
                                     # 1 for external sensor, 2 for internal control temperature, external limit temperature. Factory default: 0.

DEFAULT_MINTEMP = 5                  # Lower temperature limit for internal sensor (SVL) svl = 5..99. Factory default: 5C
DEFAULT_MAXTEMP = 35                 # Upper temperature limit for internal sensor (SVH) svh = 5..99. Factory default: 35C
DEFAULT_ROOMTEMPOFFSET=0             # Actual temperature calibration (AdJ) adj = -0.5. Prescision 0.1C
DEFAULT_ANTIFREEZE = 1               # Anti-freezing function (FrE) fre = 0 for anti-freezing function shut down, 1 for anti-freezing function open. Factory default: 0
DEFAULT_POWERONMEM = 1               # Power on memory (POn) poweronmem = 0 for power on memory off, 1 for power on memory on. Factory default: 0
DEFAULT_EXTERNALSENSORTEMPRANGE = 42 # Set temperature range for external sensor (OSV) osv = 5..99. Factory default: 42C
DEFAULT_DEADZONESENSORTEMPRANGE =  1 # Deadzone for floor temprature (dIF) dif = 1..9. Factory default: 2C

CONFIG_ADVANCED_LOOPMODE = "loop_mode"
CONFIG_ADVANCED_SENSORMODE = "sensor_mode"
CONFIG_ADVANCED_MINTEMP="min_temp"
CONFIG_ADVANCED_MAXTEMP="max_temp"
CONFIG_ADVANCED_ROOMTEMPOFFSET="roomtemp_offset"
CONFIG_ADVANCED_ANTIFREEZE="anti_freeze_function"
CONFIG_ADVANCED_POWERONMEM="poweron_mem"
CONFIG_ADVANCED_EXTERNALSENSORTEMPRANGE = "external_sensor_temprange"
CONFIG_ADVANCED_DEADZONESENSORTEMPRANGE = "deadzone_sensor_temprange"

SERVICE_SET_ADVANCED = "hysen_set_advanced"
SET_ADVANCED_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Optional(CONFIG_ADVANCED_LOOPMODE,default=DEFAULT_LOOPMODE): vol.Range(min=0, max=2),
    vol.Optional(CONFIG_ADVANCED_SENSORMODE,default=DEFAULT_SENSORMODE): vol.Range(min=0, max=2),
    vol.Optional(CONFIG_ADVANCED_MINTEMP,default=DEFAULT_MINTEMP): vol.Range(min=5, max=99),
    vol.Optional(CONFIG_ADVANCED_MAXTEMP,default=DEFAULT_MAXTEMP): vol.Range(min=5, max=99),
    vol.Optional(CONFIG_ADVANCED_ROOMTEMPOFFSET,default=DEFAULT_ROOMTEMPOFFSET): vol.Coerce(float),
    vol.Optional(CONFIG_ADVANCED_ANTIFREEZE,default=DEFAULT_ANTIFREEZE): vol.Range(min=0, max=1),
    vol.Optional(CONFIG_ADVANCED_POWERONMEM,default=DEFAULT_POWERONMEM): vol.Range(min=0, max=1),
    vol.Optional(CONFIG_ADVANCED_EXTERNALSENSORTEMPRANGE,default=DEFAULT_EXTERNALSENSORTEMPRANGE): vol.Range(min=5, max=99),
    vol.Optional(CONFIG_ADVANCED_DEADZONESENSORTEMPRANGE,default=DEFAULT_DEADZONESENSORTEMPRANGE): vol.Range(min=1, max=99),
})

CONFIG_REMOTELOCK = "remotelock"

SERVICE_SET_REMOTELOCK = "hysen_set_remotelock"
SET_REMOTELOCK_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Required(CONFIG_REMOTELOCK): vol.Range(min=0, max=1),
})

CONFIG_WEEK_PERIOD1_START = 'week_period1_start'
CONFIG_WEEK_PERIOD1_TEMP = 'week_period1_temp'
CONFIG_WEEK_PERIOD2_START = 'week_period2_start'
CONFIG_WEEK_PERIOD2_TEMP = 'week_period2_temp'
CONFIG_WEEK_PERIOD3_START = 'week_period3_start'
CONFIG_WEEK_PERIOD3_TEMP = 'week_period3_temp'
CONFIG_WEEK_PERIOD4_START = 'week_period4_start'
CONFIG_WEEK_PERIOD4_TEMP = 'week_period4_temp'
CONFIG_WEEK_PERIOD5_START = 'week_period5_start'
CONFIG_WEEK_PERIOD5_TEMP = 'week_period5_temp'
CONFIG_WEEK_PERIOD6_START = 'week_period6_start'
CONFIG_WEEK_PERIOD6_TEMP = 'week_period6_temp'
CONFIG_WEEKEND_PERIOD1_START = 'weekend_period1_start'
CONFIG_WEEKEND_PERIOD1_TEMP = 'weekend_period1_temp'
CONFIG_WEEKEND_PERIOD2_START = 'weekend_period2_start'
CONFIG_WEEKEND_PERIOD2_TEMP = 'weekend_period2_temp'

SERVICE_SET_TIME_SCHEDULE = "hysen_set_timeschedule"
SET_TIME_SCHEDULE_SCHEMA = vol.Schema({
    vol.Required(ATTR_ENTITY_ID): cv.comp_entity_ids,
    vol.Required(CONFIG_WEEK_PERIOD1_START): cv.time,
    vol.Required(CONFIG_WEEK_PERIOD1_TEMP): vol.Coerce(float),
    vol.Required(CONFIG_WEEK_PERIOD2_START): cv.time,
    vol.Required(CONFIG_WEEK_PERIOD2_TEMP): vol.Coerce(float),
    vol.Required(CONFIG_WEEK_PERIOD3_START): cv.time,
    vol.Required(CONFIG_WEEK_PERIOD3_TEMP): vol.Coerce(float),
    vol.Required(CONFIG_WEEK_PERIOD4_START): cv.time,
    vol.Required(CONFIG_WEEK_PERIOD4_TEMP): vol.Coerce(float),
    vol.Required(CONFIG_WEEK_PERIOD5_START): cv.time,
    vol.Required(CONFIG_WEEK_PERIOD5_TEMP): vol.Coerce(float),
    vol.Required(CONFIG_WEEK_PERIOD6_START): cv.time,
    vol.Required(CONFIG_WEEK_PERIOD6_TEMP): vol.Coerce(float),
    vol.Required(CONFIG_WEEKEND_PERIOD1_START): cv.time,
    vol.Required(CONFIG_WEEKEND_PERIOD1_TEMP): vol.Coerce(float),
    vol.Required(CONFIG_WEEKEND_PERIOD2_START): cv.time,
    vol.Required(CONFIG_WEEKEND_PERIOD2_TEMP): vol.Coerce(float),
})

DEFAULT_OPERATIONS_LIST = [HVAC_MODE_OFF, HVAC_MODE_HEAT, HVAC_MODE_AUTO]
HYSEN_POWERON = 1
HYSEN_POWEROFF = 0
HYSEN_MANUALMODE = 0
HYSEN_AUTOMODE = 1

DEFAULT_TARGET_TEMP = 20
DEFAULT_TARGET_TEMP_STEP = 1
DEFAULT_CONF_SYNC_CLOCK_TIME_ONCE_PER_DAY = False

CONF_DEVICES = 'devices'
CONF_TARGET_TEMP = 'target_temp_default'
CONF_TARGET_TEMP_STEP = 'target_temp_step'
CONF_TIMEOUT = 'update_timeout'
CONF_SYNC_CLOCK_TIME_ONCE_PER_DAY = 'sync_clock_time_per_day'
CONF_GETCURERNTTEMP_FROM_SENSOR = "current_temp_from_sensor_override"

CONF_DNSHOST = 'host_dns'
CONF_HOST_PORT = 'host_port'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_DEVICES, default={}): {
        cv.string: vol.Schema({
            vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
            vol.Optional(CONF_DNSHOST): cv.string,
            vol.Optional(CONF_HOST): vol.Match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
            vol.Optional(CONF_HOST_PORT, default=80): vol.Range(min=1, max=65535),
            vol.Required(CONF_MAC): vol.Match("(?:[0-9a-fA-F]:?){12}"),
            vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): vol.Range(min=0, max=99),
            vol.Optional(CONF_TARGET_TEMP, default=DEFAULT_TARGET_TEMP): vol.Range(min=5, max=99),
            vol.Optional(CONF_TARGET_TEMP_STEP, default=DEFAULT_TARGET_TEMP_STEP): vol.Coerce(float),
            vol.Optional(CONF_SYNC_CLOCK_TIME_ONCE_PER_DAY, default=DEFAULT_CONF_SYNC_CLOCK_TIME_ONCE_PER_DAY): cv.boolean,
            vol.Optional(CONF_GETCURERNTTEMP_FROM_SENSOR, default=-1): vol.Range(min=-1, max=1),
        })
    },
})

async def devices_from_config(domain_config, hass, broadlink):
    hass_devices = []
    for device_id, config in domain_config[CONF_DEVICES].items():
        # Get device-specific parameters
        name = config.get(CONF_NAME)
        dns_name = config.get(CONF_DNSHOST)
        ip_addr = config.get(CONF_HOST)
        ip_port = config.get(CONF_HOST_PORT)
        mac_addr = config.get(CONF_MAC)
        timeout = config.get(CONF_TIMEOUT)

        if (dns_name != None and ip_addr == None):
            try:
                ip_addr = socket.gethostbyname(dns_name)
                _LOGGER.warning("Discovered Broadlink Hysen device address: %s, from name %s",ip_addr,dns_name)
            except Exception as error:
                _LOGGER.error("Failed resolve DNS name to IP for Broadlink Hysen device:%s, error:%s",dns_name,error)

        # Get Operation parameters for Hysen Climate device.
        operation_list = DEFAULT_OPERATIONS_LIST
        target_temp_default = config.get(CONF_TARGET_TEMP)
        target_temp_step = config.get(CONF_TARGET_TEMP_STEP)
        sync_clock_time_per_day = config.get(CONF_SYNC_CLOCK_TIME_ONCE_PER_DAY)
        get_current_temp_from_sensor_override = config.get(CONF_GETCURERNTTEMP_FROM_SENSOR)

        # Set up the Hysen Climate devices.
        # If IP and Mac given try to directly connect
        # If only Mac given try to discover connect
        try:
            if (ip_addr != None):
                blmac_addr = binascii.unhexlify(mac_addr.encode().replace(b':', b''))
                hass_devices.append(await create_broadlink_device(
                    device_id, timeout, hass, name,
                    broadlink.hysen((ip_addr, ip_port), blmac_addr, None),
                    target_temp_default, target_temp_step, operation_list,
                    sync_clock_time_per_day, get_current_temp_from_sensor_override))
            else:
                devices = broadlink.discover(timeout)
                devicecount = len(devices)
                if devicecount > 0 :
                    for device in devices:
                        if device.devtype == 0x4EAD : # Hysen device ID
                            devicemac = ''.join(format(x, '02x') for x in device.mac)
                            revmac = [devicemac[i:i+2] for i in range(0, len(devicemac), 2)]
                            stringmac = revmac[5] +":"+ revmac[4] +":"+ revmac[3]+":"+ revmac[2]+":"+ revmac[1]+":"+ revmac[0]
                            if (stringmac.capitalize() == mac_addr.capitalize()) :
                                hass_devices.append(await create_broadlink_device(
                                    device_id, timeout, hass, name, device,
                                    target_temp_default, target_temp_step, operation_list,
                                    sync_clock_time_per_day, get_current_temp_from_sensor_override))
                                _LOGGER.warning("Discovered Broadlink Hysen device : %s, at %s",stringmac,device.host[0])
                            else:
                                _LOGGER.error("Broadlink Hysen device MAC:%s not found.",mac_addr)
                else:
                    _LOGGER.error("No Broadlink Hysen device(s) found.")
                    return []
        except Exception as error:
            _LOGGER.error("Failed to connect to Broadlink Hysen device MAC:%s, IP:%s, Error:%s", mac_addr,ip_addr, error)
    return hass_devices

async def create_broadlink_device(
        device_id, timeout, hass, name, broadlink_device, target_temp_default,
        target_temp_step, operation_list, sync_clock_time_per_day,
        get_current_temp_from_sensor_override):
    broadlink_device.timeout = timeout
    broadlink_device.auth()
    entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, device_id, hass=hass)
    return BroadlinkHysenClimate(
        entity_id,
        hass, name, broadlink_device, target_temp_default,
        target_temp_step, operation_list, sync_clock_time_per_day,
        get_current_temp_from_sensor_override)

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the Broadlink Hysen Climate platform."""
    import broadlink
    """Set up service to allow setting Hysen Climate device Wifi setup."""
    #To get the hysen thermostat in the mode to allow setting of the Wi-fi parameters.
    #With the device off Press and hold on the“power” button, then press the “time” button
    #Enter to the advanced setting, then press the “auto” button 9 times until “FAC” appears on the display
    #Press the“up” button up to “32”, then Press the “power” key, and the thermostat will be shutdown.
    #Press and hold on the “power” button, then press the “time”, the wifi icon beging flashing WiFi fast flashing show.
    #From Delevopler tools in HA select the climate.hysen_config_wifi service enter the JSON {"ssid":"yourssid","password":"yourpassword","sectype":4}
    #Security mode options are (0 - none, 1 = WEP, 2 = WPA1, 3 = WPA2, 4 = WPA1/2)
    #run call service, the wifi icon on the device should stop fast flashing and go stable.
    #In you router find the thermostat and set it to have a fixed IP, then set it up in your HA config file.

    #Example for service call (hysen_config_wifi) setting
    """
    {"ssid":"yoursid","password":"yourpassword","sectype":4,"timeout":5}
    """
    async def async_hysen_set_wifi(thermostat,service):
                ssid  = service.data.get(CONF_WIFI_SSID)
                password  = service.data.get(CONF_WIFI_PASSWORD)
                sectype  = service.data.get(CONF_WIFI_SECTYPE)
                timeout = service.data.get(CONF_WIFI_TIMEOUT)
                try:
                  broadlink.setup(ssid, password, sectype)
                except Exception as error:
                  _LOGGER.error("Failed to send Wifi setup to Broadlink Hysen Device(s):%s",error)
                  return False
                _LOGGER.warning("Wifi setup to Broadlink Hysen Device(s) sent.")
                try:
                  devices = broadlink.discover(timeout)
                  devicecount = len(devices)
                  if devicecount > 0 :
                     for device in devices:
                         if device.devtype == 0x4EAD : # Hysen device ID
                            divicemac = ''.join(format(x, '02x') for x in device.mac)
                            revmac = [divicemac[i:i+2] for i in range(0, len(divicemac), 2)]
                            stringmac = revmac[5] +":"+ revmac[4] +":"+ revmac[3]+":"+ revmac[2]+":"+ revmac[1]+":"+ revmac[0]

                            _LOGGER.warning("Discovered Broadlink Hysen device : %s, at %s",stringmac,device.host[0])
                  else:
                      _LOGGER.warning("No Broadlink Hysen device(s) found.")
                except Exception as error:
                  _LOGGER.error("Failed to discover Broadlink Hysen Device(s):",error)
                  return False
                return True

    # Advanced settings
    # Sensor mode (SEN) sensor = 0 for internal sensor, 1 for external sensor, 2 for internal control temperature, external limit temperature. Factory default: 0.
    # Set temperature range for external sensor (OSV) osv = 5..99. Factory default: 42C
    # Deadzone for floor temprature (hysteresis) (dIF) dif = 1..9. Factory default: 2C
    # Upper temperature limit for internal sensor (SVH) svh = 5..99. Factory default: 35C
    # Lower temperature limit for internal sensor (SVL) svl = 5..99. Factory default: 5C
    # Actual temperature calibration (AdJ) adj = -0.5. Prescision 0.1C
    # Anti-freezing function (FrE) fre = 0 for anti-freezing function shut down, 1 for anti-freezing function open. Factory default: 0
    # Power on memory (POn) poweronmem = 0 for power on memory off, 1 for power on memory on. Factory default: 0
    # loop_mode refers to index in [ "12345,67", "123456,7", "1234567" ]
    # E.g. loop_mode = 0 ("12345,67") means Saturday and Sunday follow the "weekend" schedule
    # loop_mode = 2 ("1234567") means every day (including Saturday and Sunday) follows the "weekday" schedule

   #Example for service call (hysen_set_advanced) setting
    """
    {"entity_id":"climate.house_thermostat","poweron_mem":"1"}
    """
    async def async_hysen_set_advanced(thermostat,service):
                entity_id = service.data.get(ATTR_ENTITY_ID)
                if thermostat.entity_id not in entity_id:
                  _LOGGER.error("Broadlink Hysen Device entity_id not found:%s",entity_id)
                  return False
                loop_mode = service.data.get(CONFIG_ADVANCED_LOOPMODE)
                sensor_mode = service.data.get(CONFIG_ADVANCED_SENSORMODE)
                external_sensor_temprange = service.data.get(CONFIG_ADVANCED_EXTERNALSENSORTEMPRANGE)
                deadzone_sensor_temprange = service.data.get(CONFIG_ADVANCED_DEADZONESENSORTEMPRANGE)
                max_temp = service.data.get(CONFIG_ADVANCED_MAXTEMP)
                min_temp = service.data.get(CONFIG_ADVANCED_MINTEMP)
                roomtemp_offset = service.data.get(CONFIG_ADVANCED_ROOMTEMPOFFSET)
                anti_freeze_function = service.data.get(CONFIG_ADVANCED_ANTIFREEZE)
                poweron_mem = service.data.get(CONFIG_ADVANCED_POWERONMEM)
                try:
                  thermostat.set_advanced(loop_mode, sensor_mode, external_sensor_temprange, deadzone_sensor_temprange, max_temp, min_temp, roomtemp_offset, anti_freeze_function, poweron_mem)
                except Exception as error:
                  _LOGGER.error("Failed to send Advanced setup to Broadlink Hysen Device:%s,:",entity_id,error)
                  return False
                _LOGGER.info("Advanced setup sent to Broadlink Hysen Device:%s",entity_id)
                return True

    # Set timer schedule
    # Format is the same as you get from get_full_status.
    # weekday is a list (ordered) of 6 dicts like:
    # {'start_hour':17, 'start_minute':30, 'temp': 22 }
    # Each one specifies the thermostat temp that will become effective at start_hour:start_minute
    # weekend is similar but only has 2 (e.g. switch on in morning and off in afternoon)

    #Example sfor service call (hysen_set_heatingschedule)
    """
    {"entity_id":"climate.house_thermostat",
    "week_period1_start":"06:30",
    "week_period1_temp":"20.5",
    "week_period2_start":"09:00",
    "week_period2_temp":"17.0",
    "week_period3_start":"13:00",
    "week_period3_temp":"17.0",
    "week_period4_start":"13:00",
    "week_period4_temp":"17.0",
    "week_period5_start":"17:00",
    "week_period5_temp":"20.5",
    "week_period6_start":"22:00",
    "week_period6_temp":"17.0",
    "weekend_period1_start":"7:30",
    "weekend_period1_temp":"20.5",
    "weekend_period2_start":"22:30",
    "weekend_period2_temp":"17.0"}
    """
    async def async_hysen_set_time_schedule(thermostat,service):
               entity_id = service.data.get(ATTR_ENTITY_ID)
               if thermostat.entity_id not in entity_id:
                  _LOGGER.error("Broadlink Hysen Device entity_id not found:%s",entity_id)
                  return False
               WEEK_PERIOD1_START  = service.data.get(CONFIG_WEEK_PERIOD1_START)
               WEEK_PERIOD1_TEMP   = service.data.get(CONFIG_WEEK_PERIOD1_TEMP)
               WEEK_PERIOD2_START  = service.data.get(CONFIG_WEEK_PERIOD2_START)
               WEEK_PERIOD2_TEMP   = service.data.get(CONFIG_WEEK_PERIOD2_TEMP)
               WEEK_PERIOD3_START  = service.data.get(CONFIG_WEEK_PERIOD3_START)
               WEEK_PERIOD3_TEMP   = service.data.get(CONFIG_WEEK_PERIOD3_TEMP)
               WEEK_PERIOD4_START  = service.data.get(CONFIG_WEEK_PERIOD4_START)
               WEEK_PERIOD4_TEMP   = service.data.get(CONFIG_WEEK_PERIOD4_TEMP)
               WEEK_PERIOD5_START  = service.data.get(CONFIG_WEEK_PERIOD5_START)
               WEEK_PERIOD5_TEMP   = service.data.get(CONFIG_WEEK_PERIOD5_TEMP)
               WEEK_PERIOD6_START  = service.data.get(CONFIG_WEEK_PERIOD6_START)
               WEEK_PERIOD6_TEMP   = service.data.get(CONFIG_WEEK_PERIOD6_TEMP)
               WEEKEND_PERIOD1_START  = service.data.get(CONFIG_WEEKEND_PERIOD1_START)
               WEEKEND_PERIOD1_TEMP   = service.data.get(CONFIG_WEEKEND_PERIOD1_TEMP)
               WEEKEND_PERIOD2_START  = service.data.get(CONFIG_WEEKEND_PERIOD2_START)
               WEEKEND_PERIOD2_TEMP   = service.data.get(CONFIG_WEEKEND_PERIOD2_TEMP)
               week_period_1 = dict()
               week_period_1["start_hour"] = int(WEEK_PERIOD1_START.strftime('%H'))
               week_period_1["start_minute"] = int(WEEK_PERIOD1_START.strftime('%M'))
               week_period_1["temp"] = float(WEEK_PERIOD1_TEMP)
               week_period_2 = dict()
               week_period_2["start_hour"] = int(WEEK_PERIOD2_START.strftime('%H'))
               week_period_2["start_minute"] = int(WEEK_PERIOD2_START.strftime('%M'))
               week_period_2["temp"] = float(WEEK_PERIOD2_TEMP)
               week_period_3 = dict()
               week_period_3["start_hour"] = int(WEEK_PERIOD3_START.strftime('%H'))
               week_period_3["start_minute"] = int(WEEK_PERIOD3_START.strftime('%M'))
               week_period_3["temp"] = float(WEEK_PERIOD3_TEMP)
               week_period_4 = dict()
               week_period_4["start_hour"] = int(WEEK_PERIOD4_START.strftime('%H'))
               week_period_4["start_minute"] = int(WEEK_PERIOD4_START.strftime('%M'))
               week_period_4["temp"] = float(WEEK_PERIOD4_TEMP)
               week_period_5 = dict()
               week_period_5["start_hour"] = int(WEEK_PERIOD5_START.strftime('%H'))
               week_period_5["start_minute"] = int(WEEK_PERIOD5_START.strftime('%M'))
               week_period_5["temp"] = float(WEEK_PERIOD5_TEMP)
               week_period_6 = dict()
               week_period_6["start_hour"] = int(WEEK_PERIOD6_START.strftime('%H'))
               week_period_6["start_minute"] = int(WEEK_PERIOD6_START.strftime('%M'))
               week_period_6["temp"] = float(WEEK_PERIOD6_TEMP)
               weekend_period_1 = dict()
               weekend_period_1["start_hour"] = int(WEEKEND_PERIOD1_START.strftime('%H'))
               weekend_period_1["start_minute"] = int(WEEKEND_PERIOD1_START.strftime('%M'))
               weekend_period_1["temp"] = float(WEEKEND_PERIOD1_TEMP)
               weekend_period_2 = dict()
               weekend_period_2["start_hour"] = int(WEEKEND_PERIOD2_START.strftime('%H'))
               weekend_period_2["start_minute"] = int(WEEKEND_PERIOD2_START.strftime('%M'))
               weekend_period_2["temp"] = float(WEEKEND_PERIOD2_TEMP)

               weekday = [week_period_1, week_period_2,
                          week_period_3, week_period_4,
                          week_period_5, week_period_6]
               weekend = [weekend_period_1, weekend_period_2]
               try:
                    thermostat.set_schedule(weekday, weekend)
               except Exception as error:
                   _LOGGER.error("Failed to send Time schedule setup to Broadlink Hysen Device:%s,:",entity_id,error)
                   return False
               _LOGGER.info("Time schedule sent to Broadlink Hysen Device:%s",entity_id)
               return True

    #Example for service call (hysen_set_remotelock) setting
    """
    {"entity_id":"climate.house_thermostat","remotelock":1}
    """
    async def async_hysen_set_remotelock(thermostat,service):
                entity_id = service.data.get(ATTR_ENTITY_ID)
                if thermostat.entity_id not in entity_id:
                  _LOGGER.error("Broadlink Hysen Device entity_id not found:%s",entity_id)
                  return False
                tamper_lock = service.data.get(CONFIG_REMOTELOCK)
                try:
                  thermostat.set_lock(tamper_lock)
                except Exception as error:
                  _LOGGER.error("Failed to send Tamper Lock setting to Broadlink Hysen Device:%s,:",entity_id,error)
                  return False
                _LOGGER.info("Remote Lock setting sent to Broadlink Hysen Device:%s",entity_id)
                return True

    hass.data[DOMAIN].async_register_entity_service(
        SERVICE_SET_WIFI, SET_WIFI_SCHEMA,
        async_hysen_set_wifi
        )

    hass.data[DOMAIN].async_register_entity_service(
        SERVICE_SET_ADVANCED, SET_ADVANCED_SCHEMA,
        async_hysen_set_advanced
        )

    hass.data[DOMAIN].async_register_entity_service(
        SERVICE_SET_TIME_SCHEDULE, SET_TIME_SCHEDULE_SCHEMA,
        async_hysen_set_time_schedule
        )

    hass.data[DOMAIN].async_register_entity_service(
        SERVICE_SET_REMOTELOCK, SET_REMOTELOCK_SCHEMA,
        async_hysen_set_remotelock
        )

    hass_devices = await devices_from_config(config, hass, broadlink)

    if hass_devices:
        async_add_devices(hass_devices)

class BroadlinkHysenClimate(ClimateDevice):

    def __init__(self, entity_id, hass, name, broadlink_device, target_temp_default,
                 target_temp_step, operation_list,sync_clock_time_per_day,get_current_temp_from_sensor_override):
        """Initialize the Broadlink Hysen Climate device."""
        self.entity_id = entity_id
        self._hass = hass
        self._name = name
        self._HysenData = []
        self._broadlink_device = broadlink_device

        self._sync_clock_time_per_day = sync_clock_time_per_day
        self._current_day_of_week = 0

        self._get_current_temp_from_sensor_override = get_current_temp_from_sensor_override

        self._target_temperature = target_temp_default
        self._target_temperature_step = target_temp_step
        self._unit_of_measurement = hass.config.units.temperature_unit

        self._power_state = HYSEN_POWEROFF
        self._auto_state = HYSEN_MANUALMODE
        self._current_operation = STATE_UNAVAILABLE
        self._operation_list = operation_list

        self._away_mode = False
        self._awaymodeLastState = HVAC_MODE_OFF

        self._is_heating_active = 0
        self._auto_override = 0
        self._remote_lock = 0

        self._loop_mode = DEFAULT_LOOPMODE
        self._sensor_mode = DEFAULT_SENSORMODE
        self._min_temp = DEFAULT_MINTEMP
        self._max_temp = DEFAULT_MAXTEMP
        self._roomtemp_offset = DEFAULT_ROOMTEMPOFFSET
        self._anti_freeze_function = DEFAULT_ANTIFREEZE
        self._poweron_mem = DEFAULT_POWERONMEM

        self._external_sensor_temprange = DEFAULT_EXTERNALSENSORTEMPRANGE
        self._deadzone_sensor_temprange = DEFAULT_DEADZONESENSORTEMPRANGE
        self._room_temp = 0
        self._external_temp = 0

        self._clock_hour = 0
        self._clock_min = 0
        self._clock_sec = 0
        self._day_of_week = 1

        self._week_day = ""
        self._week_end = ""
        
        #Sync the time on startup
#        self.set_time(datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second, datetime.datetime.today().weekday())

        self._available = False  # should become True after first update()

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        try:
            await self._hass.async_add_executor_job(self._broadlink_device.auth)
        except Exception as error:
            _LOGGER.error("Failed to Auth. Broadlink Hysen device:%s, on adding to HA, %s",self.entity_id,error)

    @property
    def available(self) -> bool:
        """Return True if the device is currently available."""
        return self._available

    @property
    def should_poll(self):
        """Return the polling state."""
        return True

    @property
    def name(self):
        """Return the name of the climate device."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def current_temperature(self):
        """Return the current temperature."""
        # sensor = 0 for internal sensor, 1 for external sensor, 2 for internal control temperature, external limit temperature.
        if self._get_current_temp_from_sensor_override == 0:
            return self._room_temp
        elif self._get_current_temp_from_sensor_override == 1:
            return self._external_temp
        else:
            if self._sensor_mode == 1:
                return self._external_temp
            else:
                return self._room_temp

    @property
    def min_temp(self):
        """Return the polling state."""
        return self._min_temp

    @property
    def max_temp(self):
        """Return the polling state."""
        return self._max_temp

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return self._target_temperature_step

    @property
    def hvac_mode(self):
        """Return current operation ie. heat, idle."""
        return self._current_operation

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        return self._operation_list

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    def preset_modes(self):
        """Return valid preset modes."""
        return [
            PRESET_AWAY,PRESET_NONE
        ]

    @property
    def is_away_mode_on(self):
        """Return if away mode is on."""
        return self._away_mode

    @property
    def hvac_action(self):
        """Return current HVAC action."""
        if self._is_heating_active == 1:
            return CURRENT_HVAC_HEAT
        else:
            return CURRENT_HVAC_IDLE

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        attr = {}
        attr['sfw_version'] = VERSION
        attr['power_state'] = self._power_state
        attr['away_mode'] = self._away_mode
        attr['sensor_mode'] = self._sensor_mode
        attr['room_temp'] = self._room_temp
        attr['external_temp'] = self._external_temp
        attr['heating_active'] = self._is_heating_active
        attr['auto_override'] = self._auto_override
        attr['external_sensor_temprange'] = self._external_sensor_temprange
        attr['deadzone_sensor_temprange'] = self._deadzone_sensor_temprange
        attr['loop_mode'] = self._loop_mode
        attr['roomtemp_offset'] = float(self._roomtemp_offset)
        attr['anti_freeze_function'] = self._anti_freeze_function
        attr['poweron_mem'] = self._poweron_mem
        attr['remote_lock'] = self._remote_lock
        attr['clock_hour'] = self._clock_hour
        attr['clock_min'] = self._clock_min
        attr['clock_sec'] = self._clock_sec
        attr['day_of_week'] = self._day_of_week
        attr['week_day'] = str(self._week_day).replace("'",'"')
        attr['week_end'] = str(self._week_end).replace("'",'"')
        return attr

    def turn_on(self):
        self.send_power_command(HYSEN_POWERON,self._remote_lock)
        self._away_mode = False
        return True

    def turn_off(self):
        self.send_power_command(HYSEN_POWEROFF,self._remote_lock)
        self._away_mode = False
        return True

    def set_temperature(self, **kwargs):
        """Set new target temperatures."""
        if kwargs.get(ATTR_TEMPERATURE) is not None:
            self._target_temperature = kwargs.get(ATTR_TEMPERATURE)
            if (self._power_state == HYSEN_POWERON):
                self.send_tempset_command(self._target_temperature)
            self.schedule_update_ha_state()

    def set_hvac_mode(self, operation_mode):
        """Set new opmode """
        self._current_operation = operation_mode
        if self._away_mode == True:
            self.set_preset_mode(PRESET_NONE)
        self.set_operation_mode_command(operation_mode)
        self.schedule_update_ha_state()

    def set_preset_mode(self, preset_mode):
        if preset_mode == PRESET_AWAY:
            if self._away_mode == False:
                self._awaymodeLastState = self._current_operation
                self._away_mode = True
                self.set_operation_mode_command(HVAC_MODE_OFF)
        elif preset_mode == PRESET_NONE:
            if self._away_mode == True:
                self._away_mode = False
                self.set_operation_mode_command(self._awaymodeLastState)
        else:
            _LOGGER.error("Unknown mode: %s", preset_mode)
        self.schedule_update_ha_state()

    def send_tempset_command(self, target_temperature):
        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_temp(target_temperature)
                break
            except socket.timeout:
                try:
                    self._broadlink_device.auth()
                except Exception as error:
                        if retry == DEFAULT_RETRY-1:
                            _LOGGER.error(
                                "Failed to send SetTemp command to Broadlink Hysen Device:%s, :%s",self.entity_id,error)

    def send_power_command(self, target_state,remote_lock):
        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_power(target_state,remote_lock)
                break
            except socket.timeout:
                try:
                    self._broadlink_device.auth()
                except Exception as error:
                    if retry == DEFAULT_RETRY-1:
                        _LOGGER.error(
                            "Failed to send Power command to Broadlink Hysen Device:%s, :%s",self.entity_id,error)

    def send_mode_command(self, target_state, loopmode, sensor):
        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_mode(target_state, loopmode, sensor)
                break
            except socket.timeout:
                try:
                    self._broadlink_device.auth()
                except Exception as error:
                    if retry == DEFAULT_RETRY-1:
                        _LOGGER.error(
                            "Failed to send OpMode-Heat/Manual command to Broadlink Hysen Device:%s, :%s",self.entity_id,error)

    def set_operation_mode_command(self, operation_mode):
        if operation_mode == HVAC_MODE_HEAT:
            if self._power_state == HYSEN_POWEROFF:
                self.send_power_command(HYSEN_POWERON,self._remote_lock)
            self.send_mode_command(HYSEN_MANUALMODE, self._loop_mode,self._sensor_mode)
        elif operation_mode == HVAC_MODE_AUTO:
            if self._power_state == HYSEN_POWEROFF:
                self.send_power_command(HYSEN_POWERON,self._remote_lock)
            self.send_mode_command(HYSEN_AUTOMODE, self._loop_mode,self._sensor_mode)
        elif operation_mode == HVAC_MODE_OFF:
                  self.send_power_command(HYSEN_POWEROFF,self._remote_lock)
        else:
            _LOGGER.error("Unknown command for Broadlink Hysen Device: %s",self.entity_id)
        return

    def set_time(self, hour, minute, second, day):
        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_time(hour, minute, second, day)
                break
            except socket.timeout:
                try:
                    self._broadlink_device.auth()
                except Exception as error:
                    if retry == DEFAULT_RETRY-1:
                        _LOGGER.error(
                            "Failed to send Set Time command to Broadlink Hysen Device: %s, :%s",self.entity_id,error)

    def set_advanced(self, loop_mode=None, sensor=None, osv=None, dif=None,
                     svh=None, svl=None, adj=None, fre=None, poweronmem=None):
        loop_mode = self._loop_mode if loop_mode is None else loop_mode
        sensor = self._sensor_mode if sensor is None else sensor
        osv = self._external_sensor_temprange if osv is None else osv
        dif = self._deadzone_sensor_temprange if dif is None else dif
        svh = self._max_temp if svh is None else svh
        svl = self._min_temp if svl is None else svl
        adj = self._roomtemp_offset if adj is None else adj
        fre = self._anti_freeze_function if fre is None else fre
        poweronmem = self._poweron_mem if poweronmem is None else poweronmem

       # Fix for native broadlink.py set_advanced breaking loopmode and operation_mode
        if self._current_operation == HVAC_MODE_HEAT:
            current_mode = HYSEN_MANUALMODE
        else:
            current_mode = HYSEN_AUTOMODE
        mode_byte = ( (loop_mode + 1) << 4) + current_mode

        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_advanced(
                    mode_byte, sensor, osv, dif, svh, svl, adj, fre, poweronmem)
                break
            except socket.timeout:
                try:
                    self._broadlink_device.auth()
                except Exception as error:
                    if retry == DEFAULT_RETRY-1:
                        _LOGGER.error(
                            "Failed to send Set Advanced to Broadlink Hysen Device: %s, :%s",self.entity_id,error)

    def set_schedule(self, weekday, weekend):
        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_schedule(weekday, weekend)
                break
            except socket.timeout:
                try:
                    self._broadlink_device.auth()
                except Exception as error:
                    if retry == DEFAULT_RETRY-1:
                        _LOGGER.error(
                            "Failed to send Set Schedule to Broadlink Hysen Device: %s, :%s",self.entity_id,error)

    def set_lock(self, remote_lock):
        for retry in range(DEFAULT_RETRY):
            try:
                if self._away_mode == False:
                    self._broadlink_device.set_power(self._power_state, remote_lock)
                else:
                    self._broadlink_device.set_power(0, remote_lock)
                break
            except socket.timeout:
                try:
                    self._broadlink_device.auth()
                except Exception as error:
                    if retry == DEFAULT_RETRY-1:
                        _LOGGER.error(
                            "Failed to send Set Lock to Broadlink Hysen Device: %s, :%s",self.entity_id,error)

    def update(self):
        """Get the latest data from the thermostat."""
        time.sleep(random.uniform(0.1, 0.5))
        for retry in range(DEFAULT_RETRY):
            try:
                self._HysenData = self._broadlink_device.get_full_status()
                if self._HysenData is not None:
                    self._room_temp = self._HysenData['room_temp']
                    self._target_temperature = self._HysenData['thermostat_temp']
                    self._min_temp = self._HysenData['svl']
                    self._max_temp = self._HysenData['svh']
                    self._loop_mode = int(self._HysenData['loop_mode'])-1
                    self._power_state = self._HysenData['power']
                    self._auto_state = self._HysenData['auto_mode']
                    self._is_heating_active = self._HysenData['active']

                    self._remote_lock = self._HysenData['remote_lock']
                    self._auto_override = self._HysenData['temp_manual']
                    self._sensor_mode = self._HysenData['sensor']
                    self._external_sensor_temprange = self._HysenData['osv']
                    self._deadzone_sensor_temprange = self._HysenData['dif']
                    self._roomtemp_offset = self._HysenData['room_temp_adj']
                    self._anti_freeze_function = self._HysenData['fre']
                    self._poweron_mem = self._HysenData['poweron']
                    self._external_temp = self._HysenData['external_temp']
                    self._clock_hour = self._HysenData['hour']
                    self._clock_min = self._HysenData['min']
                    self._clock_sec = self._HysenData['sec']
                    self._day_of_week = self._HysenData['dayofweek']
                    self._week_day = self._HysenData['weekday']
                    self._week_end = self._HysenData['weekend']

                    self._available = True
                    if self._power_state == HYSEN_POWERON:
                        if self._auto_state == HYSEN_AUTOMODE:
                            self._current_operation = HVAC_MODE_AUTO
                        else:
                            self._current_operation = HVAC_MODE_HEAT
                    elif self._power_state == HYSEN_POWEROFF:
                         self._target_temperature = self._min_temp
                         self._current_operation = HVAC_MODE_OFF
                    else:
                         self._current_operation = STATE_UNAVAILABLE
                         self._available = False
                else:
                    _LOGGER.error("Failed to get Update from Broadlink Hysen Device: %s, GetFullStatus returned None!",self.entity_id)
                    self._current_operation = STATE_UNAVAILABLE
                    self._available = False

            except Exception as error:
                if retry < 1:
                    _LOGGER.error("Failed to get Data from Broadlink Hysen Device:%s,:%s",self.entity_id,error)
                    self._current_operation = STATE_UNAVAILABLE
                    self._room_temp = 0
                    self._external_temp = 0
                    self._available = False
                return

        """Sync the clock once per day if required."""        
        try:
          if self._sync_clock_time_per_day == True:
             now_day_of_the_week = (datetime.datetime.today().weekday()) + 1
             if self._current_day_of_week < now_day_of_the_week:
                currentDT = datetime.datetime.now()
                if currentDT.time() > datetime.time(hour=3): #Set am 3am
                    self.set_time(currentDT.hour, currentDT.minute, currentDT.second, now_day_of_the_week)
                    self._current_day_of_week = now_day_of_the_week
                    _LOGGER.info("Broadlink Hysen Device:%s Clock Sync Success...",self.entity_id)
        except Exception as error:
          _LOGGER.error("Failed to Clock Sync Hysen Device:%s,:%s",self.entity_id,error)
