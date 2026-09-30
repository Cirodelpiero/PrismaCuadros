from extensions import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(
    "password_hash",
    db.String(255),
    nullable=False
)
    telefono = db.Column(db.String(30))
    rol = db.Column(db.String(50))
    fecha_registro = db.Column(db.DateTime)