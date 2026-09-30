from models.cuadro import Cuadro
from extensions import db

def obtener_cuadros():
    """Devuelve todos los cuadros guardados en la base de datos."""
    return Cuadro.query.all()


def buscar_cuadro(id_cuadro):
    return db.session.get(Cuadro, id_cuadro)   

def crear_cuadro(cuadro):
    try:
        db.session.add(cuadro)
        db.session.commit()
        return cuadro

    except Exception as error:
        db.session.rollback()
        print(f"Error al crear cuadro: {error}")
        return None

def editar_cuadro(cuadro):
    try:
        db.session.commit()
        return cuadro

    except Exception as error:
        db.session.rollback()
        print(f"Error al editar cuadro: {error}")
        return None

def eliminar_cuadro(id_cuadro):

    cuadro = db.session.get(Cuadro, id_cuadro)

    if cuadro is None:
        return False

    db.session.delete(cuadro)
    db.session.commit()

    return True

def obtener_destacados():
    return Cuadro.query.filter_by(destacado=True).all()

def obtener_cuadros_por_categoria(id_categoria):
    return Cuadro.query.filter_by(id_categoria=id_categoria).all()