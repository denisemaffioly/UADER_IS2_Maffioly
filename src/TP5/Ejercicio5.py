import os
from collections import deque

class State:
    def scan(self):
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print(f"Sintonizando... Estación {self.stations[self.pos]} {self.name}")

    def get_state_data(self):
        return self.name, self.pos

    def set_state_data(self, pos):
        self.pos = pos

class AmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos = 0
        self.name = "AM"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.save_state()
        self.radio.state = self.radio.fmstate

class FmState(State):
    def __init__(self, radio):
        self.radio = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos = 0
        self.name = "FM"

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.save_state()
        self.radio.state = self.radio.amstate

class Radio:
    def __init__(self):
        self.fmstate = FmState(self)
        self.amstate = AmState(self)
        self.state = self.fmstate
        self.history = deque(maxlen=4)

    def save_state(self):
        state_name, pos = self.state.get_state_data()
        self.history.appendleft((state_name, pos))

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        self.save_state()
        self.state.scan()

    def undo(self, index):
        if index < len(self.history):
            state_name, pos = self.history[index]
            print(f"Restaurando estado anterior {index}: {state_name} en posición {pos}")
            if state_name == "FM":
                self.state = self.fmstate
            else:
                self.state = self.amstate
            self.state.set_state_data(pos)
        else:
            print("No hay suficiente historial para deshacer ese nivel.")


if __name__ == "__main__":
    os.system("clear")
    print("\nCrea un objeto radio y almacena las siguientes acciones")
    radio = Radio()
    
    actions = [radio.scan] * 3 + [radio.toggle_amfm] + [radio.scan] * 2
    for action in actions:
        action()

 
    print("\n--- Restaurando estados anteriores ---")
    radio.undo(0)  
    radio.scan()
    radio.undo(1) 
    radio.scan()
    radio.undo(3)  
    radio.scan()
