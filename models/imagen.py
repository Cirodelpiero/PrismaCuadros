from extensions import db


class Imagen(db.Model):
    __tablename__ = "imagenes"

    id_imagen = db.Column(db.Integer, primary_key=True)

    id_cuadro = db.Column(
        db.Integer,
        db.ForeignKey("cuadros.id_cuadro"),
        nullable=False
    )

    ruta_imagen = db.Column(
        db.String(255),
        nullable=False
    )

    es_principal = db.Column(
        db.Boolean,
        default=False
    )