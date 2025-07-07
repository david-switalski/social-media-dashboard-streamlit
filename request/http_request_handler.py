# This module requires an http request to the streamlit cloud server

import requests
import time
import datetime

url = ('https://social-media-dashboard-app-xpwxatitnjprnkp9v5cfde.streamlit.app/')

while True:
    successful_request = False

    while not successful_request:
        
        try: 
            response = requests.get(url)
            
            if response.status_code == 200:
                successful_request = True
                print(f"[{datetime.datetime.now()}] Success: Request sent successfully. Status code: {response.status_code}")
            else:
                print(f"[{datetime.datetime.now()}] HTTP status error: {response.status_code}. Retrying in 5 minutes...")
                time.sleep(300)
            
        except requests.exceptions.RequestException as e:
            print(f"[{datetime.datetime.now()}] Error de conexión: {e}. Retrying in 5 minutes...")
            time.sleep(300)
        
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Error inesperado: {e}. Retrying in 5 minutes...")
            time.sleep(300)
            
    t = 3
    print(f"[{datetime.datetime.now()}] Successful request. Waiting {t} seconds for the next iteration...")
    time.sleep(t)

    
    
