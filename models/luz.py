from extensions import db

class Luz(db.Model):
    __tablename__ = "luz"

    id_luz = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)