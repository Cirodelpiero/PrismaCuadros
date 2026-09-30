class Producto:

    def __init__(self, id, nombre, precio, stock):

        self.id = int(id)
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)



    def vender_unidad(self):

        if self.stock > 0:
            self.stock -= 1

    
    
    def stock_bajo(self):
        return self.stock <= 5
    

    def agotado(self):
        return self.stock == 0