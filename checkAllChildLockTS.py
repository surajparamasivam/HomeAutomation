
import hassapi as hass
import datetime

class ChildLockChecker(hass.Hass):
    def initialize(self):
        # Run every 6 hours
        self.run_every(self.check_child_locks, 
                      datetime.datetime.now(), 
                      6 * 60 * 60)  # 6 hours in seconds

    def check_child_locks(self, kwargs):
        # List of touch switches to check
        touch_switches = [
            "switch.office_ts_child_lock",  # Replace with your actual switch entity IDs
            "switch.bedroom_ts_child_lock",
            "switch.parking_ts_right_child_lock",
            "switch.parking_ts_left_child_lock"
        ]

        for switch in touch_switches:
            try:
                # Get current child lock state
                child_lock_state = self.get_state(f"{switch}_child_lock")
                
                # If child lock is off or in unknown state, turn it on
                if child_lock_state != "on":
                    self.call_service("switch/turn_on", 
                                    entity_id=f"{switch}_child_lock")
                    self.log(f"Turned on child lock for {switch}")
                else:
                    self.log(f"Child lock already enabled for {switch}")
                    
            except Exception as e:
                self.error(f"Error checking/setting child lock for {switch}: {str(e)}")
