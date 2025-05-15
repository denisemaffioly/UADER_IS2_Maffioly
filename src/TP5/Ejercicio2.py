class Cadena:
    def __init__(self, texto):
        self.texto = texto

    def obtener_iterador(self, reverso=False):
        return IteradorCadena(self.texto, reverso)


class IteradorCadena:
    def __init__(self, texto, reverso):
        self.texto = texto
        self.reverso = reverso
        self.posicion = len(texto) - 1 if reverso else 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.reverso:
            if self.posicion < 0:
                raise StopIteration
            caracter = self.texto[self.posicion]
            self.posicion -= 1
            return caracter
        else:
            if self.posicion >= len(self.texto):
                raise StopIteration
            caracter = self.texto[self.posicion]
            self.posicion += 1
            return caracter
