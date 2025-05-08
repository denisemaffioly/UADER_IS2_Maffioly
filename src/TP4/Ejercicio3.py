# Clase base Componente
class Componente:
    def __init__(self, nombre):
        self.nombre = nombre

    def mostrar(self, nivel=0):
        raise NotImplementedError("Este método debe ser implementado por las subclases")


# Clase Pieza (hoja del árbol)
class Pieza(Componente):
    def mostrar(self, nivel=0):
        print("  " * nivel + f"- Pieza: {self.nombre}")


# Clase SubConjunto (compuesto)
class SubConjunto(Componente):
    def __init__(self, nombre):
        self.nombre = nombre
        self.componentes = []

    def agregar(self, componente):
        self.componentes.append(componente)

    def mostrar(self, nivel=0):
        print("  " * nivel + f"+ SubConjunto: {self.nombre}")
        for componente in self.componentes:
            componente.mostrar(nivel + 1)
