"""
Sistema de pagos versión 1.2
Automatización de pagos usando patrón Singleton, Cadena de Responsabilidad e Iterador.
"""

import json
from abc import ABC, abstractmethod


class ClaveBanco:
    """
    Singleton que carga claves desde sitedata.json.
    """
    _instancia = None
    _claves = {}

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            with open("sitedata.json", "r", encoding="utf-8") as archivo:
                cls._claves = json.load(archivo)
        return cls._instancia

    def get_clave(self, token):
        """
        Devuelve la clave asociada a un token (banco).
        """
        return self._claves.get(token)


class PedidoPago:
    """
    Representa un pedido de pago con número, monto, banco utilizado y clave.
    """
    def __init__(self, numero, monto, token, clave):
        self.numero = numero
        self.monto = monto
        self.token = token
        self.clave = clave

    def __str__(self):
        return f"Pedido #{self.numero} | Monto: ${self.monto} | Token: {self.token} | Clave: {self.clave}"


class HistorialPagos:
    """
    Historial que almacena pagos realizados, implementa un iterador.
    """
    def __init__(self):
        self._pagos = []

    def agregar_pago(self, pago):
        """
        Agrega un pago al historial.
        """
        self._pagos.append(pago)

    def listar_pagos(self):
        """
        Iterador que devuelve pagos uno por uno.
        """
        for pago in self._pagos:
            yield pago


class CuentaPago(ABC):
    """
    Clase abstracta para representar una cuenta de pago.
    """
    def __init__(self, token, saldo):
        self.token = token
        self.saldo = saldo
        self._siguiente = None

    def set_siguiente(self, siguiente):
        """
        Define el siguiente manejador en la cadena.
        """
        self._siguiente = siguiente

    def procesar_pago(self, numero, monto, historial):
        """
        Intenta procesar el pago; si no puede, pasa al siguiente en la cadena.
        """
        if self.saldo >= monto:
            self.saldo -= monto
            clave = ClaveBanco().get_clave(self.token)
            pago = PedidoPago(numero, monto, self.token, clave)
            historial.agregar_pago(pago)
            print(f"[✔] Pago procesado: {pago}")
            return True

        if self._siguiente:
            return self._siguiente.procesar_pago(numero, monto, historial)

        print(f"[✖] No se pudo procesar el pago #{numero} por falta de saldo.")
        return False


class SistemaPagos:
    """
    Componente principal que gestiona los pagos.
    """
    def __init__(self):
        self.historial = HistorialPagos()
        self.cuenta1 = CuentaPagoConcreta("token1", 1000)
        self.cuenta2 = CuentaPagoConcreta("token2", 2000)
        self.cuenta1.set_siguiente(self.cuenta2)
        self.cuenta2.set_siguiente(self.cuenta1)
        self.turno = True  # True = token1 primero, False = token2 primero
        self.contador_pedidos = 1

    def realizar_pago(self, monto):
        """
        Realiza un nuevo pago alternando entre cuentas.
        """
        numero = self.contador_pedidos
        self.contador_pedidos += 1

        if self.turno:
            self.cuenta1.procesar_pago(numero, monto, self.historial)
        else:
            self.cuenta2.procesar_pago(numero, monto, self.historial)

        self.turno = not self.turno

    def mostrar_historial(self):
        """
        Muestra todos los pagos realizados.
        """
        print("\n--- Historial de pagos ---")
        for pago in self.historial.listar_pagos():
            print(pago)
        print("--- Fin del historial ---\n")


class CuentaPagoConcreta(CuentaPago):
    """Implementación concreta de CuentaPago."""
    pass


if __name__ == "__main__":
    sistema = SistemaPagos()
    # Se realizan 6 pagos de $500
    for _ in range(6):
        sistema.realizar_pago(500)

    sistema.mostrar_historial()
