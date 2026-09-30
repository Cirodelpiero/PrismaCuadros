from extensions import db


class CuadroMedida(db.Model):
    __tablename__ = "cuadro_medidas"

    id_cuadro_medida = db.Column(
        db.Integer,
        primary_key=True
    )

    id_cuadro = db.Column(
        db.Integer,
        db.ForeignKey("cuadros.id_cuadro"),
        nullable=False
    )

    id_medida = db.Column(
        db.Integer,
        db.ForeignKey("medidas.id_medida"),
        nullable=False
    )

    precio = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    medida = db.relationship("Medida")