from models.producto import Producto

class Remera(Producto):
    def __init__(self, id, nombre, precio, stock, banda, imagen_principal, talle):
        super().__init__(id, nombre, precio, stock, banda,imagen_principal)
        self.talle = talle
        

  
    def mostrar_info(self):
        base = super().mostrar_info()
        return f"{base} - Talle: {self.talle}"     