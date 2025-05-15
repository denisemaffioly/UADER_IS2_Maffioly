class Emisor:
    def __init__(self):
        self.observadores = []

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def emitir_id(self, id_emitido):
        print(f"\n Emisor: Emite ID -> {id_emitido}")
        for obs in self.observadores:
            obs.notificar(id_emitido)

class Observador:
    def __init__(self, id_propietario):
        self.id_propietario = id_propietario

    def notificar(self, id_emitido):
        if id_emitido == self.id_propietario:
            print(f"Observador {self.id_propietario}: ¡ID recibido y coincide!")

emisor = Emisor()

obs1 = Observador("AB12")
obs2 = Observador("XZ98")
obs3 = Observador("J4K9")
obs4 = Observador("QWER")

emisor.agregar_observador(obs1)
emisor.agregar_observador(obs2)
emisor.agregar_observador(obs3)
emisor.agregar_observador(obs4)

ids_a_emitir = ["AB12", "ZZZZ", "QWER", "LMNO", "XZ98", "1234", "J4K9", "AAAA"]

for id_actual in ids_a_emitir:
    emisor.emitir_id(id_actual)
