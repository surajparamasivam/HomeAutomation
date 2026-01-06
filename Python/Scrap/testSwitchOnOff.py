import hassapi as hass
import datetime

class SwitchMonitor(hass.Hass):
    def initialize(self):
        # Run check every minute
        time = datetime.time(0, 0, 0)  # Start at midnight
        self.run_minutely(self.check_switch_state, time)
        
        # Define the switch entity ID you want to monitor
        self.monitored_switch = "light.office_light"  # Replace with actual switch ID
        
        # Define the switch that needs to be controlled
        self.controlled_switch = "switch.office_ts_switch_3"  # Replace with actual switch ID
        
    def check_switch_state(self, kwargs):
        try:
            # Get current state of the monitored switch
            switch_state = self.get_state(self.monitored_switch)
            self.log(f"Current state of {self.monitored_switch}: {switch_state}")
            
            # Add your logic here to determine when to turn on the controlled switch
            # For example, turn on controlled switch if monitored switch is off
            if switch_state == "off":
                self.turn_on_controlled_switch()
                
        except Exception as e:
            self.error(f"Error checking switch state: {str(e)}")
            
    def turn_on_controlled_switch(self):
        try:
            # Turn on the controlled switch
            self.call_service("switch/turn_on",
                            entity_id=self.controlled_switch)
            self.log(f"Turned on {self.controlled_switch}")
            
        except Exception as e:
            self.error(f"Error turning on switch: {str(e)}")
