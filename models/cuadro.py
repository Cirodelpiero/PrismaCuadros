from extensions import db


class Cuadro(db.Model):
    __tablename__ = "cuadros"

    id_cuadro = db.Column(db.Integer, primary_key=True)

    id_categoria = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id_categoria"),
        nullable=False
    )

  

    id_luz = db.Column(
        db.Integer,
        db.ForeignKey("luz.id_luz"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    
    stock = db.Column(db.Integer, default=0)
    peso = db.Column(db.Numeric(6, 2))
    destacado = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # RELACIONES

    

    imagenes = db.relationship(
        "Imagen",
        backref="cuadro",
        lazy=True,
        cascade="all, delete-orphan"
    )

    medidas_disponibles = db.relationship(
        "CuadroMedida",
        backref="cuadro",
        lazy=True,
        cascade="all, delete-orphan"
    )