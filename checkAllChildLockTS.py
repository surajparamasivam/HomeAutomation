import requests       
import time    
           
HA_URL = "http://192.168.1.139:8123"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"
                                                                                                                                                                                                    

class CheckChildLocks(hass.Hass):
    def initialize(self):        
        self.run_every(self.check_and_turn_on_switches, "now", 6 * 60 * 60)  # 6 hours in seconds
                                                                                                 
    def check_and_turn_on_switches(self, kwargs):
        switches = [                             
            "switch.office_ts_child_lock",  # Replace with your actual switch entity IDs
            "switch.bedroom_ts_child_lock",                                             
            "switch.parking_ts_right_child_lock",
            "switch.parking_ts_left_child_lock"  
        ]                                      

        for switch in switches:
            state = self.get_state(switch)
            if state == "off":            
                self.log(f"{switch} is off. Turning it on.")
                self.turn_on_switch(switch)                 
            else:                          
                self.log(f"{switch} is already on.")
                self.turn_off_switch(switch)        
                self.turn_on_switch(switch) 
                                           
    def turn_on_switch(self, switch):
        url = f"{HA_URL}/api/services/switch/turn_on"
        headers = {                                  
            "Authorization": f"Bearer {HA_TOKEN}",
            "Content-Type": "application/json",   
        }                                      
        payload = {"entity_id": switch}
                                       
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:                             
                self.log(f"Successfully turned on {switch}")
            else:                                           
                self.log(f"Failed to turn on {switch}. Status code: {response.status_code}")
        except Exception as e:                                                              
            self.log(f"Error turning on {switch}: {str(e)}")
                                                            
    def turn_off_switch(self, switch):
        url = f"{HA_URL}/api/services/switch/turn_off"
        headers = {                                   
            "Authorization": f"Bearer {HA_TOKEN}",
            "Content-Type": "application/json",   
        }                                      
        payload = {"entity_id": switch}
                                       
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:                             
                self.log(f"Successfully turned off {switch}")
            else:                                            
                self.log(f"Failed to turn off {switch}: {response.status_code} {response.text}")
        except Exception as e:                                                                  
            self.log(f"Error turning off {switch}: {str(e)}")