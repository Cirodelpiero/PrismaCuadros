from extensions import db

class Medida(db.Model):
    __tablename__ = "medidas"

    id_medida = db.Column(db.Integer, primary_key=True)
    ancho = db.Column(db.Numeric(5,2), nullable=False)
    alto = db.Column(db.Numeric(5,2), nullable=False)
    espesor = db.Column(db.Numeric(5,2))