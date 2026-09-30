from models.producto import Producto

class Taza(Producto): 
    def __init__(self, id, nombre, precio, stock, banda, imagen_principal, material, capacidad):
        super().__init__(id, nombre, precio, stock, banda, imagen_principal)
        self.material = material
        self.capacidad = capacidad

    def mostrar_info(self):
        base = super().mostrar_info()
        return f"{base} - Material: {self.material} - Capacidad: {self.material}"    

#taza1 = Taza("Taza RHCP", 20, 30, "RHCP", "ceramica")
#print(taza1.mostrar_info())  
