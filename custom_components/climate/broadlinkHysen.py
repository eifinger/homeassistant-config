"""
Platform for Hysen Electronic heating Thermostats power by broadlink.
(Beok, Floureon, Decdeal) 
discussed in https://community.home-assistant.io/t/floor-heat-thermostat/29908
"""

import logging
import binascii
import socket
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import inspect
from datetime import timedelta

from homeassistant.components.climate import (ClimateDevice, PLATFORM_SCHEMA, SUPPORT_TARGET_TEMPERATURE,
                                                             ATTR_TEMPERATURE,
                                                             SUPPORT_OPERATION_MODE,SUPPORT_ON_OFF)

from homeassistant.const import (ATTR_TEMPERATURE,ATTR_UNIT_OF_MEASUREMENT,CONF_NAME, CONF_HOST, CONF_MAC, CONF_TIMEOUT, CONF_CUSTOMIZE)

REQUIREMENTS = ['broadlink==0.9.0']

_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE | SUPPORT_ON_OFF

CONF_TARGET_TEMP = 'target_temp_default'
CONF_TARGET_TEMP_STEP = 'target_temp_step'
CONF_OPERATIONS = 'operations'

STATE_IDLE =  "off"
STATE_HEAT = "heat"
STATE_AUTO = "auto"

HYSEN_POWERON    = 1
HYSEN_POWEROFF   = 0
HYSEN_MANUALMODE = 0
HYSEN_AUTOMODE   = 1

DEFAULT_NAME = 'Broadlink Hysen Climate'
DEFAULT_TIMEOUT = 10
DEFAULT_RETRY = 3
DEFAULT_TARGET_TEMP = 20
DEFAULT_TARGET_TEMP_STEP = 1
DEFAULT_OPERATION_LIST = [STATE_HEAT, STATE_AUTO]


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_MAC): cv.string,
    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int, 
    vol.Optional(CONF_TARGET_TEMP, default=DEFAULT_TARGET_TEMP): cv.positive_int,
    vol.Optional(CONF_TARGET_TEMP_STEP, default=DEFAULT_TARGET_TEMP_STEP): cv.positive_int,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Broadlink Hysen Climate platform."""
    name = config.get(CONF_NAME)
    ip_addr = config.get(CONF_HOST)
    mac_addr = binascii.unhexlify(config.get(CONF_MAC).encode().replace(b':', b''))
    target_temp_default = config.get(CONF_TARGET_TEMP)
    target_temp_step = config.get(CONF_TARGET_TEMP_STEP)
    operation_list =  DEFAULT_OPERATION_LIST
    
    import broadlink
    
    broadlink_device = broadlink.hysen((ip_addr, 80), mac_addr, None)
    broadlink_device.timeout = config.get(CONF_TIMEOUT)

    try:
        broadlink_device.auth()
        add_devices([
                    BroadlinkHysenClimate(hass, name, broadlink_device, target_temp_default, target_temp_step, operation_list)
                    ])
    except socket.timeout:
        _LOGGER.error("Failed to connect to Broadlink Hysen Device IP:%s",ip_addr)


class BroadlinkHysenClimate(ClimateDevice):

    def __init__(self, hass, name, broadlink_device,target_temp_default, target_temp_step, operation_list):
        """Initialize the Broadlink Hysen Climate device."""
        self.hass = hass
        self._name = name
        self.HysenData = []        
        self._broadlink_device = broadlink_device

        self._target_temperature = target_temp_default
        self._target_temperature_step = target_temp_step
        self._unit_of_measurement = hass.config.units.temperature_unit

        self._min_temp = 0
        self._max_temp = 0
        self._current_temperature = 0        
        self._power_state = HYSEN_POWEROFF        #On = 1  #Off = 0
        self._auto_state = HYSEN_MANUALMODE       #Manual =0   #Auto, =1
        self._current_operation = STATE_IDLE      
        self._operation_list = operation_list
        self._loop_mode = 0                       #12345,67 = 1   123456,7 = 2  1234567 = 3        
        self._is_heating_active = 0               #Demand = 1, No Demand = 0

        self.remote_lock = 0
        self.auto_override = 0
        self.sensor_mode = 0
        self.external_sensor_temprange = 0
        self.deadzone_sensor_temprange = 0
        self.roomtemp_offset = 0
        self.anti_freeze_function = 0
        self.poweron_mem = 0
        self.external_temp = 0
        self.clock_hour = 0
        self.clock_min = 0
        self.clock_sec = 0
        self.day_of_week = 0
        self.week_day = 0
        self.week_end = 0


        self.update()

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
        return self._current_temperature
        
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
    def current_operation(self):
        """Return current operation ie. heat, idle."""
        return self._current_operation

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return self._operation_list
        
    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS        

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        attr = {}
        attr['remote_lock'] = self.remote_lock
        attr['power_state'] = self._power_state
        attr['heating_active'] = self._is_heating_active
        attr['auto_override'] = self.auto_override
        attr['sensor_mode'] = self.sensor_mode
        attr['external_sensor_temprange'] = self.external_temp
        attr['deadzone_sensor_temprange'] = self.deadzone_sensor_temprange
        attr['loop_mode'] = self._loop_mode
        attr['roomtemp_offset'] = self.roomtemp_offset
        attr['anti_freeze_function'] = self.anti_freeze_function
        attr['poweron_mem'] = self.poweron_mem
        attr['external_temp'] =  self.external_temp
        attr['clock_hour'] = self.clock_hour
        attr['clock_min'] = self.clock_min
        attr['clock_sec'] = self.clock_sec
        attr['day_of_week'] = self.day_of_week
        attr['week_day'] = self.week_day
        attr['week_end'] = self.week_end
        return attr
    @property
    def is_on(self):
        """Return the list of available operation modes."""
        if self._power_state == HYSEN_POWERON :
            return True
        else:
            return False
    
    def turn_on(self):
        self._broadlink_device.set_power(HYSEN_POWERON)
        return True

    def turn_off(self):
        self._broadlink_device.set_power(HYSEN_POWEROFF)
        return True

    def set_temperature(self, **kwargs):
        """Set new target temperatures."""
        if kwargs.get(ATTR_TEMPERATURE) is not None:
            self._target_temperature = kwargs.get(ATTR_TEMPERATURE)
            if (self._power_state == HYSEN_POWERON):
                self.send_tempset_command(kwargs.get(ATTR_TEMPERATURE))
            self.schedule_update_ha_state()

    def set_operation_mode(self, operation_mode):
        """Set new opmode """
        self._current_operation = operation_mode
        self.set_operation_mode_command(operation_mode)
        self.schedule_update_ha_state()

    def send_tempset_command(self,target_temperature):
        for retry in range(DEFAULT_RETRY):
          try:
             self._broadlink_device.set_temp(target_temperature)
             break
          except (socket.timeout, ValueError):
               try:
                  self._broadlink_device.auth()
               except socket.timeout:
                    if retry == DEFAULT_RETRY-1:
                       _LOGGER.error("Failed to send SetTemp command to Broadlink Hysen Device")        

    def send_power_command(self,target_state):
        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_power(target_state)
                break
            except (socket.timeout, ValueError):
                try:
                    self._broadlink_device.auth()
                except socket.timeout:
                    if retry == DEFAULT_RETRY-1:
                       _LOGGER.error("Failed to send Power command to Broadlink Hysen Device")

    def send_mode_command(self,target_state,loopmode=1,sensor=0):
        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_mode(target_state,loopmode,sensor)
                break
            except (socket.timeout, ValueError):
                try:
                    self._broadlink_device.auth()
                except socket.timeout:
                    if retry == DEFAULT_RETRY-1:
                       _LOGGER.error("Failed to send OpMode-Heat/Manual command to Broadlink Hysen Device")

  # Change controller mode
  # auto_mode = 1 for auto (scheduled/timed) mode, 0 for manual mode.
  # Manual mode will activate last used temperature.  In typical usage call set_temp to activate manual control and set temp.
  # loop_mode refers to index in [ "12345,67", "123456,7", "1234567" ]
  # E.g. loop_mode = 0 ("12345,67") means Saturday and Sunday follow the "weekend" schedule
  # loop_mode = 2 ("1234567") means every day (including Saturday and Sunday) follows the "weekday" schedule
    def set_operation_mode_command(self,operation_mode):
        if operation_mode == STATE_HEAT:
               if self._power_state == HYSEN_POWEROFF:
                  self.send_power_command(HYSEN_POWERON)
               self.send_mode_command(HYSEN_MANUALMODE,self._loop_mode)
        elif operation_mode == STATE_AUTO:
               if self._power_state == HYSEN_POWEROFF:
                  self.send_power_command(HYSEN_POWERON)
               self.send_mode_command(HYSEN_AUTOMODE,self._loop_mode)
        else:
          _LOGGER.error("Unknown command for Broadlink Hysen Device")
          return

    # set time on device
    # n.b. day=1 is Monday, ..., day=7 is Sunday
    def set_time(self, hour, minute, second, day):
        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_time(self, hour, minute, second, day)
                break
            except (socket.timeout, ValueError):
                try:
                    self._broadlink_device.auth()
                except socket.timeout:
                    if retry == DEFAULT_RETRY-1:
                       _LOGGER.error("Failed to send Set Time command to Broadlink Hysen Device")
    # Advanced settings
    # Sensor mode (SEN) sensor = 0 for internal sensor, 1 for external sensor, 2 for internal control temperature, external limit temperature. Factory default: 0.
    # Set temperature range for external sensor (OSV) osv = 5..99. Factory default: 42C
    # Deadzone for floor temprature (dIF) dif = 1..9. Factory default: 2C
    # Upper temperature limit for internal sensor (SVH) svh = 5..99. Factory default: 35C
    # Lower temperature limit for internal sensor (SVL) svl = 5..99. Factory default: 5C
    # Actual temperature calibration (AdJ) adj = -0.5. Prescision 0.1C
    # Anti-freezing function (FrE) fre = 0 for anti-freezing function shut down, 1 for anti-freezing function open. Factory default: 0
    # Power on memory (POn) poweron = 0 for power on memory off, 1 for power on memory on. Factory default: 0
    # loop_mode refers to index in [ "12345,67", "123456,7", "1234567" ]
    # E.g. loop_mode = 0 ("12345,67") means Saturday and Sunday follow the "weekend" schedule
    # loop_mode = 2 ("1234567") means every day (including Saturday and Sunday) follows the "weekday" schedule
    def set_advanced(self, loop_mode, sensor, osv, dif, svh, svl, adj, fre, poweron):
        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_advanced(self, loop_mode, sensor, osv, dif, svh, svl, adj, fre, poweron)
                break
            except (socket.timeout, ValueError):
                try:
                    self._broadlink_device.auth()
                except socket.timeout:
                    if retry == DEFAULT_RETRY-1:
                       _LOGGER.error("Failed to send Set Advanced to Broadlink Hysen Device")

    # Set timer schedule
    # Format is the same as you get from get_full_status.
    # weekday is a list (ordered) of 6 dicts like:
    # {'start_hour':17, 'start_minute':30, 'temp': 22 }
    # Each one specifies the thermostat temp that will become effective at start_hour:start_minute
    # weekend is similar but only has 2 (e.g. switch on in morning and off in afternoon)
    def set_schedule(self,weekday,weekend):
        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_schedule(self,weekday,weekend)
                break
            except (socket.timeout, ValueError):
                try:
                    self._broadlink_device.auth()
                except socket.timeout:
                    if retry == DEFAULT_RETRY-1:
                       _LOGGER.error("Failed to send Set Advanced to Broadlink Hysen Device")

    def set_lock(self,remote_lock):
        for retry in range(DEFAULT_RETRY):
            try:
                self._broadlink_device.set_power(self, self._power_state, remote_lock=0)
                break
            except (socket.timeout, ValueError):
                try:
                    self._broadlink_device.auth()
                except socket.timeout:
                    if retry == DEFAULT_RETRY-1:
                       _LOGGER.error("Failed to send Set Lock to Broadlink Hysen Device")

    def update(self):
        """Get the latest data from the sensor."""
        for retry in range(DEFAULT_RETRY):
            try:
              self.HysenData = self._broadlink_device.get_full_status()
              if self.HysenData is not None:
                 self._current_temperature = self.HysenData['room_temp']
                 self._target_temperature = self.HysenData['thermostat_temp']
                 self._min_temp = self.HysenData['svl']
                 self._max_temp = self.HysenData['svh']
                 self._loop_mode = int(self.HysenData['loop_mode'])-1
                 self._power_state = self.HysenData['power']
                 self._auto_state = self.HysenData['auto_mode']
                 self._is_heating_active = self.HysenData['active']

                 self.remote_lock = self.HysenData['remote_lock']
                 self.auto_override = self.HysenData['temp_manual']
                 self.sensor_mode = self.HysenData['sensor']
                 self.external_sensor_temprange = self.HysenData['osv']
                 self.deadzone_sensor_temprange = self.HysenData['dif']
                 self.roomtemp_offset = self.HysenData['room_temp_adj']
                 self.anti_freeze_function = self.HysenData['fre']
                 self.poweron_mem = self.HysenData['poweron']
                 self.external_temp = self.HysenData['external_temp']
                 self.clock_hour = self.HysenData['hour']
                 self.clock_min = self.HysenData['min']
                 self.clock_sec = self.HysenData['sec']
                 self.day_of_week = self.HysenData['dayofweek']
                 self.week_day = self.HysenData['weekday']
                 self.week_end = self.HysenData['weekend']

                 if self._power_state == HYSEN_POWERON :
                    if self._auto_state == HYSEN_AUTOMODE:
                       self._current_operation = STATE_AUTO
                    else:
                       self._current_operation = STATE_HEAT
                 else:
                     self._target_temperature = self._min_temp
                     self._current_operation = STATE_IDLE

            except socket.timeout as error:
                  if retry < 1:
                    _LOGGER.error("Failed to get Data from Hysen Device:%s",error)
                    return
            except (vol.Invalid, vol.MultipleInvalid) as error:
                  _LOGGER.warning("%s %s",error, error.__str__)
                  pass  
            


