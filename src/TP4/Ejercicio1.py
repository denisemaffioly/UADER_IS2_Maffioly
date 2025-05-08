import os
import platform

class Ping:
    def __init__(self):
        self.ping_cmd = "ping -n 1" if platform.system().lower() == "windows" else "ping -c 1"

    def execute(self, ip):
        if not ip.startswith("192."):
            raise ValueError("Dirección IP no permitida. Debe comenzar con '192.'")
        print(f"Ejecutando ping a {ip} (con validación)...")
        for i in range(10):
            response = os.system(f"{self.ping_cmd} {ip} >nul 2>&1" if platform.system().lower() == "windows"
                                 else f"{self.ping_cmd} {ip} >/dev/null 2>&1")
            print(f"Intento {i + 1}: {'Éxito' if response == 0 else 'Fallo'}")

    def executefree(self, ip):
        print(f"Ejecutando ping a {ip} (sin validación)...")
        for i in range(10):
            response = os.system(f"{self.ping_cmd} {ip} >nul 2>&1" if platform.system().lower() == "windows"
                                 else f"{self.ping_cmd} {ip} >/dev/null 2>&1")
            print(f"Intento {i + 1}: {'Éxito' if response == 0 else 'Fallo'}")


class PingProxy:
    def __init__(self):
        self.ping = Ping()

    def execute(self, ip):
        if ip == "192.168.0.254":
            print("Proxy detectó IP especial, redirigiendo a www.google.com sin validación.")
            self.ping.executefree("www.google.com")
        else:
            print("Proxy reenvía a Ping con validación.")
            self.ping.execute(ip)
