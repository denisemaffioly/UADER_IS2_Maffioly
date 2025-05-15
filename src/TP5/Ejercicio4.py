import os

class State:
    def scan(self):
        print("Sintonizando... Estación {} {}".format(self.stations[self.pos], self.name))
        self.pos = (self.pos + 1) % len(self.stations)

class AmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos = 0
        self.name = "AM"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate

class FmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos = 0
        self.name = "FM"

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.state = self.radio.amstate

class Radio:
    def __init__(self):
        self.fmstate = FmState(self)
        self.amstate = AmState(self)
        self.state = self.fmstate

        self.memories = [
            ("M1", "AM", "1250"),
            ("M2", "FM", "89.1"),
            ("M3", "AM", "1380"),
            ("M4", "FM", "103.9")
        ]

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.state.scan()

    def scan_memories(self):
        print("\n--- Barrido de memorias ---")
        for label, band, freq in self.memories:
            print(f"Sintonizando memoria {label}: Estación {freq} {band}")
        print("--- Fin del barrido de memorias ---\n")


if __name__ == "__main__":
    os.system("clear")
    print("\nCrea un objeto radio y almacena las siguientes acciones")
    
    radio = Radio()
    actions = [radio.scan] * 3 + [radio.scan_memories] + [radio.toggle_amfm] + [radio.scan] * 3 + [radio.scan_memories]
    actions *= 2

    print("Recorre las acciones ejecutando la acción, el objeto cambia la interfaz según el estado\n")
    for action in actions:
        action()
