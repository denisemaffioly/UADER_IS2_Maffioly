
#1. Provea una clase que dado un número entero cualquiera retorne el factorial del mismo, debe asegurarse que todas las clases que lo invoquen utilicen la misma instancia de clase. 
class Factorial:

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Factorial, cls).__new__(cls)
        return cls._instancia

    def calcular(self, n):
        if n < 0:
            raise ValueError("El número debe ser no negativo.")
        return 1 if n == 0 or n == 1 else n * self.calcular(n - 1)
    
#2. Elabore una clase para el cálculo del valor de impuestos a ser utilizado por todas las clases que necesiten realizarlo. El cálculo de impuestos simplificado deberá recibir un valor de importe base imponible y deberá retornar la suma del cálculo de IVA (21%), IIBB (5%) y Contribuciones municipales (1,2%) sobre esa base imponible. 
class Impuesto:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Impuesto, cls).__new__(cls)
        return cls._instancia

    def calcular_total_impuestos(self, base):
        iva = base * 0.21
        iibb = base * 0.05
        contribuciones = base * 0.012
        total_impuestos = iva + iibb + contribuciones
        return total_impuestos

#3. Genere una clase donde se instancie una comida rápida “hamburguesa” que pueda ser entregada en mostrador, retirada por el cliente o enviada por delivery. A los efectos prácticos bastará que la clase imprima el método de entrega. 
class Hamburguesa:
    def __init__(self):
        pass

    def entregar_en_mostrador(self):
        print("La hamburguesa será entregada en el mostrador.")

    def entregar_por_retiro(self):
        print("La hamburguesa será retirada por el cliente.")

    def entregar_por_delivery(self):
        print("La hamburguesa será enviada por delivery.")

#4. Implemente una clase “factura” que tenga un importe correspondiente al total de la factura pero de acuerdo a la condición impositiva del cliente (IVA Responsable, IVA No Inscripto, IVA Exento) genere facturas que indiquen tal condición. 
class Factura:
    def __init__(self, total, condicion_iva):
        self.total = total
        self.condicion_iva = condicion_iva

    def mostrar(self):
        print(f"Factura")
        print(f"Importe total: ${self.total:.2f}")
        print(f"Condición impositiva del cliente: {self.condicion_iva}")

#6. Dado una clase que implemente el patrón “prototipo” verifique que una clase generada a partir de ella permite por su parte obtener también copias de sí misma. 
import copy

class Prototipo:
    def clonar(self):
        return copy.deepcopy(self)

class ObjetoConcreto(Prototipo):
    def __init__(self, nombre, datos):
        self.nombre = nombre
        self.datos = datos

    def mostrar(self):
        print(f"Nombre: {self.nombre}, Datos: {self.datos}")

#7. Imagine una situación donde pueda ser de utilidad el patrón “abstract factory”.
#Creamos una fábrica por plataforma que sepa cómo crear todos los elementos de su sistema. El cliente solo pregunta a la fábrica por los objetos, sin saber su clase concreta.

class Boton:
    def dibujar(self): pass

class Menu:
    def mostrar(self): pass

class BotonWindows(Boton):
    def dibujar(self): print("Botón estilo Windows")

class MenuWindows(Menu):
    def mostrar(self): print("Menú estilo Windows")

class BotonMac(Boton):
    def dibujar(self): print("Botón estilo Mac")

class MenuMac(Menu):
    def mostrar(self): print("Menú estilo Mac")

class FabricaGUI:
    def crear_boton(self): pass
    def crear_menu(self): pass

class FabricaWindows(FabricaGUI):
    def crear_boton(self): return BotonWindows()
    def crear_menu(self): return MenuWindows()

class FabricaMac(FabricaGUI):
    def crear_boton(self): return BotonMac()
    def crear_menu(self): return MenuMac()
