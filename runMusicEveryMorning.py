import appdaemon.plugins.hass.hassapi as hass
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class MorningMusic(hass.Hass):
    def initialize(self):
        # TV Configuration
        self.tv_entity = "media_player.samsung_cu7700_75_2"  # Updated TV entity ID
        self.ha_url = "http://192.168.1.139:8123"
        self.ha_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMGQ4ODNlM2U3NGI0NWRjOWQ1NjY1OTI4ZGViY2JiNiIsImlhdCI6MTczMjU0OTE5MiwiZXhwIjoyMDQ3OTA5MTkyfQ.OTK4S8S-FoIBj3hMaqb-8aKKcBriq54B9YmbgkgmkPk"
        
        # Spotify Configuration
        self.spotify_client_id = "03f5bae7bf764fbebbf86ce68b2586d4"
        self.spotify_client_secret = "a3e55db8727d4f75b76d8eef90233922"
        self.spotify_redirect_uri = "http://localhost:8888/callback"
        self.morning_playlist_id = "spotify:playlist:023ZDpHY9o4NUaHjrqqEow?si=DyEYz4v1T1aXlrG2Ch54Jg"  # The Spotify playlist ID to play
        
        # Initialize Spotify client
        try:
            self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=self.spotify_client_id,
                client_secret=self.spotify_client_secret,
                redirect_uri=self.spotify_redirect_uri,
                scope="user-modify-playback-state user-read-playback-state"
            ))
            self.log("Successfully initialized Spotify client")
        except Exception as e:
            self.log(f"Error initializing Spotify client: {str(e)}")
            self.spotify = None
        
        # Schedule the function to run at 5 AM every day
        self.run_daily(self.morning_routine, "05:00:00")

    def morning_routine(self, kwargs):
        try:
            # Step 1: Turn on TV if it's off
            tv_state = self.get_state(self.tv_entity)
            if tv_state == "off" or tv_state == "unavailable":
                self.turn_on_tv()
                self.log("Turning on the TV")
                # Wait for TV to fully turn on
                self.run_in(self.setup_tv_for_music, 15)  # Wait 15 seconds
            else:
                self.setup_tv_for_music(None)
        except Exception as e:
            self.log(f"Error in morning routine: {str(e)}")

    def setup_tv_for_music(self, kwargs):
        try:
            # Step 2: Set TV source to TV
            self.select_source("TV")
            self.log("Setting TV source")
            
            # Step 3: Set initial volume to 18%
            self.set_volume(0.18)
            self.log("Setting initial TV volume to 18%")
            
            # Schedule volume increases
            self.run_in(lambda kwargs: self.set_volume(0.20), 1800)  # Increase to 20% after 30 minutes
            self.run_in(lambda kwargs: self.set_volume(0.22), 3600)  # Increase to 22% after 1 hour
            
            # Step 4: Start playing Spotify playlist
            self.play_morning_playlist()
        except Exception as e:
            self.log(f"Error in setup_tv_for_music: {str(e)}")

    def turn_on_tv(self):
        headers = {
            "Authorization": f"Bearer {self.ha_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "entity_id": self.tv_entity
        }
        url = f"{self.ha_url}/api/services/media_player/turn_on"
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                self.log("Successfully turned on the TV")
            else:
                self.log(f"Failed to turn on TV. Status code: {response.status_code}")
        except Exception as e:
            self.log(f"Error turning on TV: {str(e)}")

    def set_volume(self, volume_level):
        headers = {
            "Authorization": f"Bearer {self.ha_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "entity_id": self.tv_entity,
            "volume_level": volume_level
        }
        url = f"{self.ha_url}/api/services/media_player/volume_set"
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                self.log(f"Successfully set TV volume to {int(volume_level * 100)}%")
            else:
                self.log(f"Failed to set TV volume. Status code: {response.status_code}")
        except Exception as e:
            self.log(f"Error setting TV volume: {str(e)}")

    def select_source(self, source):
        headers = {
            "Authorization": f"Bearer {self.ha_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "entity_id": self.tv_entity,
            "source": source
        }
        url = f"{self.ha_url}/api/services/media_player/select_source"
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                self.log(f"Successfully switched TV source to {source}")
            else:
                self.log(f"Failed to switch TV source. Status code: {response.status_code}")
        except Exception as e:
            self.log(f"Error switching TV source: {str(e)}")

    def play_morning_playlist(self):
        if not self.spotify:
            self.log("Spotify client not initialized")
            return
            
        try:
            # Get available devices
            devices = self.spotify.devices()
            
            # Find TV device (assuming it's named similarly to your TV)
            tv_device = None
            for device in devices['devices']:
                if "Samsung" in device['name']:
                    tv_device = device
                    break
            
            if tv_device:
                # Start playback on TV
                self.spotify.start_playback(
                    device_id=tv_device['id'],
                    context_uri=f"spotify:playlist:{self.morning_playlist_id}"
                )
                self.log("Successfully started Spotify playlist on TV")
            else:
                self.log("Could not find TV in Spotify devices")
        except Exception as e:
            self.log(f"Error playing Spotify playlist: {str(e)}")
