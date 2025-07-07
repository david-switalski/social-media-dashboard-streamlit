# This module requires an http request to the streamlit cloud server

import requests
import time

url = ('https://social-media-dashboard-app-xpwxatitnjprnkp9v5cfde.streamlit.app/')

while True:
    successful_request = False

    while not successful_request:
        
        try: 
            response = requests.get(url)
            
            if response.status_code == 200:
                successful_request = True
                print("sucess")
            else:
                time.sleep(300)
            
        except requests.exceptions.RequestException:
            time.sleep(300)
        
        except Exception:
            time.sleep(300)
            
    t = 3
    time.sleep(t)

    
    
