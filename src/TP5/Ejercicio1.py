def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

class ManejadorBase:
    def __init__(self, siguiente=None):
        self.siguiente = siguiente

    def manejar(self, numero):
        if self.siguiente:
            self.siguiente.manejar(numero)
        else:
            print(f"{numero} no fue consumido.")

class ManejadorPrimos(ManejadorBase):
    def manejar(self, numero):
        if es_primo(numero):
            print(f"{numero} fue consumido por ManejadorPrimos.")
        else:
            super().manejar(numero)

class ManejadorPares(ManejadorBase):
    def manejar(self, numero):
        if numero % 2 == 0:
            print(f"{numero} fue consumido por ManejadorPares.")
        else:
            super().manejar(numero)

manejador = ManejadorPrimos(ManejadorPares())

for i in range(1, 101):
    manejador.manejar(i)
