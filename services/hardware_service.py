import requests
import os

NODEMCU_IP = os.getenv(
    "NODEMCU_IP"
)

def activate_corridor():

    requests.get(
        f"http://{NODEMCU_IP}/emergency"
    )

def normal_mode():

    requests.get(
        f"http://{NODEMCU_IP}/normal"
    )