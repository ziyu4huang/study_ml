
import os
from sys import platform

def check_platform() -> tuple:
    ipv4 = "127.0.0.1"
    gpu = 0
    cpu = 8
    try:
        if platform == "linux":
            ipv4 = os.popen("ip addr show eth0 |grep inet | grep -Fv inet6  | awk '{print $2}' | cut -d '/' -f 1").read().strip()
            cpu = 8
        if platform == "darwin":
            ipv4 = os.popen("ifconfig | grep \"inet \" | grep -Fv 127.0.0.1 | awk '{print $2}'").read().strip()
            gpu = 1
            cpu = 10
    except:
        pass
    print("Current IP: ", ipv4)

    return (ipv4, gpu, cpu)

