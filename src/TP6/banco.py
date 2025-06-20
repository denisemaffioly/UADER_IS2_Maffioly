import json
from abc import ABC, abstractmethod


class ClaveBanco:
    _instancia = None
    _claves = {}

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            try:
                with open("sitedata.json", "r", encoding="utf-8") as archivo:
                    cls._claves = json.load(archivo)
            except FileNotFoundError:
                print("[!] Error: El archivo 'sitedata.json' no fue encontrado.")
                print("    Las operaciones que requieran claves bancarias podrían fallar.")
                cls._claves = {}

    def get_clave(self, token):
     return self._claves.get(token)


def obtener_clave_bancaria(token="token1"):
   return ClaveBanco().get_clave(token)


class PedidoPago:
    def __init__(self, numero, monto, token, clave):
        self.numero = numero
        self.monto = monto
        self.token = token
        self.clave = clave

    def __str__(self):
        return f"Pedido #{self.numero} | Monto: ${self.monto} | Token: {self.token} | Clave: {self.clave}"


class HistorialPagos:
   def __init__(self):
        self._pagos = []

    def agregar_pago(self, pago):
        self._pagos.append(pago)

    def listar_pagos(self):
        for pago in self._pagos:
            yield pago


class CuentaPago(ABC):
    def __init__(self, token, saldo):
        self.token = token
        self.saldo = saldo
        self._siguiente = None 

    def set_siguiente(self, siguiente):
        self._siguiente = siguiente

    def procesar_pago(self, numero, monto, historial):
       
        if self.saldo >= monto:
            self.saldo -= monto
            clave = ClaveBanco().get_clave(self.token)
            pago = PedidoPago(numero, monto, self.token, clave)
            historial.agregar_pago(pago)
            print(f"[✔] Pago procesado: {pago}")
            return True

        if self._siguiente:
            print(f"[>] Cuenta {self.token} no tiene saldo suficiente para pago #{numero} (${monto}). Pasando a la siguiente cuenta...")
            return self._siguiente.procesar_pago(numero, monto, historial)

        print(f"[✖] No se pudo procesar el pago #{numero} por falta de saldo en todas las cuentas disponibles.")
        return False


class SistemaPagos:
    
    def __init__(self):
        
        self.historial = HistorialPagos()
        self.cuenta1 = CuentaPagoConcreta("token1", 1000)
        self.cuenta2 = CuentaPagoConcreta("token2", 2000)
        self.cuenta1.set_siguiente(self.cuenta2)
        self.cuenta2.set_siguiente(self.cuenta1)
        self.turno = True  
        self.contador_pedidos = 1

    def realizar_pago(self, monto):
       numero = self.contador_pedidos
        self.contador_pedidos += 1

        print(f"\n--- Intentando procesar pago #{numero} por ${monto} ---")
        if self.turno:
            print(f"Inicio de procesamiento con {self.cuenta1.token} (saldo actual: ${self.cuenta1.saldo})")
            pago_procesado = self.cuenta1.procesar_pago(numero, monto, self.historial)
        else:
            print(f"Inicio de procesamiento con {self.cuenta2.token} (saldo actual: ${self.cuenta2.saldo})")
            pago_procesado = self.cuenta2.procesar_pago(numero, monto, self.historial)

        self.turno = not self.turno 

    def mostrar_historial(self):
        print("\n--- Historial de Pagos Realizados ---")
        if not list(self.historial.listar_pagos()): 
            print("No hay pagos registrados en el historial.")
        else:
            for pago in self.historial.listar_pagos():
                print(pago)
        print("--- Fin del Historial ---\n")


class CuentaPagoConcreta(CuentaPago):
    pass


if __name__ == "__main__":
    print("--- Demostración de funcionalidad de obtención de claves (Punto 2.f) ---")
    print(f"Clave para 'token1' (por defecto): {obtener_clave_bancaria()}")
    print(f"Clave para 'token2': {obtener_clave_bancaria('token2')}")
    print(f"Clave para 'token_inexistente': {obtener_clave_bancaria('token_inexistente')} (esperado: None)")
    print("-------------------------------------------------------------------\n")

    sistema = SistemaPagos()
    print("--- Demostración del Sistema de Pagos (Punto 2.b y 2.h) ---")
    for i in range(6):
        sistema.realizar_pago(500)

    sistema.mostrar_historial()