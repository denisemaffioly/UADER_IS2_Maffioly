# archivo: decorator_ejemplo.py

class Numero:
    def __init__(self, valor):
        self.valor = valor

    def calcular(self):
        return self.valor


class Operacion:
    def __init__(self, numero):
        self.numero = numero

    def calcular(self):
        return self.numero.calcular()


class SumarDos(Operacion):
    def calcular(self):
        return self.numero.calcular() + 2


class MultiplicarPorDos(Operacion):
    def calcular(self):
        return self.numero.calcular() * 2


class DividirEntreTres(Operacion):
    def calcular(self):
        return self.numero.calcular() / 3


# Uso del patrón Decorator
numero = Numero(9)
print("Número:", numero.calcular())

num_suma = SumarDos(numero)
print("Sumarle 2:", num_suma.calcular())

num_mult = MultiplicarPorDos(num_suma)
print("Multiplicarlo por 2:", num_mult.calcular())

num_final = DividirEntreTres(num_mult)
print("Dividido 3:", num_final.calcular())
