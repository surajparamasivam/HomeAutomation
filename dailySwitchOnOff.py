import appdaemon.plugins.hass.hassapi as hass
import datetime
import random

class DailyLightScheduler(hass.Hass):
    def initialize(self):
        # List of specific lights that should always be turned on
        self.fixed_lights = [
            "switch.parking_ts_right_switch_2",
            "switch.parking_ts_right_switch_6",
            "switch.parking_ts_left_switch_8"
        ]
        
        # List of lights to randomly choose from
        self.random_light_pool = [
            "switch.parking_ts_left_switch_1",
            "switch.parking_ts_left_switch_2",
            "switch.parking_ts_left_switch_3",
            "switch.parking_ts_left_switch_4",
            "switch.parking_ts_left_switch_5",
            "switch.parking_ts_left_switch_6",
            "switch.parking_ts_left_switch_7",
            "switch.parking_ts_right_switch_1",
            "switch.parking_ts_right_switch_3",
            "switch.parking_ts_right_switch_4",
            "switch.parking_ts_right_switch_5",
            "switch.parking_ts_right_switch_7",
            "switch.parking_ts_right_switch_8"
        ]
        
        # Number of random lights to turn on each day
        self.num_random_lights = 2
        
        # Schedule lights on at 15:00 (3:00 PM)
        self.run_daily(self.lights_on_handler, "15:00:00")
        
        # Schedule various check times
        self.run_daily(self.lights_off_handler, "17:00:00")
        self.run_daily(self.lights_off_handler, "01:00:00")
        
    def lights_on_handler(self, kwargs):
        # Turn on fixed lights
        for light in self.fixed_lights:
            self.turn_on(light)
            
        # Select and turn on random lights
        daily_random_lights = random.sample(self.random_light_pool, self.num_random_lights)
        for light in daily_random_lights:
            self.turn_on(light)
            
        # Schedule turn off after 1 hour
        self.run_in(self.lights_off_handler, 3600)
        
    def lights_off_handler(self, kwargs):
        # Turn off all lights (both fixed and random pool)
        all_lights = self.fixed_lights + self.random_light_pool
        for light in all_lights:
            if self.get_state(light) == "on":
                self.turn_off(light)
