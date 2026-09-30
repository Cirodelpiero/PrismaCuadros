import os
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db
from models.cuadro import Cuadro
from models.imagen import Imagen
from models.categoria import Categoria
from models.medida import Medida
from models.luz import Luz
from models.usuario import Usuario
from models.cuadro_medida import CuadroMedida
from services.cuadro_service import (
    obtener_cuadros,
    buscar_cuadro,
    crear_cuadro,
    editar_cuadro,
    eliminar_cuadro,
    obtener_destacados,
    obtener_cuadros_por_categoria
)




app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "prisma-studio-2026"
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def inicio():

    cuadros = obtener_cuadros()
    destacados = obtener_destacados()
    categorias = Categoria.query.all()
    usuario = None

    if "usuario_id" in session:
        usuario = db.session.get(
            Usuario,
            session["usuario_id"]
        )

    return render_template(
        "index.html",
        cuadros=cuadros,
        destacados=destacados,
        categorias=categorias,
        usuario = usuario
    )

@app.route("/dashboard")
def dashboard():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    usuario = db.session.get(
        Usuario,
        session["usuario_id"]
    )

    if usuario is None or usuario.rol != "admin":
        return redirect(url_for("inicio"))

    cuadros = obtener_cuadros()

    return render_template(
        "dashboard.html",
        cuadros=cuadros
    )


@app.route("/cuadro/<int:id_cuadro>")
def ver_cuadro(id_cuadro):

    cuadro = buscar_cuadro(id_cuadro)

    if cuadro is None:
        return "Cuadro no encontrado", 404

    return render_template(
        "detalle_cuadro.html",
        cuadro=cuadro
    )

@app.route("/crear", methods=["GET", "POST"])
def crear():

    categorias = Categoria.query.all()
    medidas = Medida.query.all()
    luces = Luz.query.all()

    if request.method == "POST":

        # Obtener todas las medidas marcadas
        medidas_seleccionadas = request.form.getlist(
            "medidas_seleccionadas"
        )

        if not medidas_seleccionadas:
            return "Debes seleccionar al menos una medida"

        # La primera seleccionada se usa temporalmente
        # como medida/precio base del cuadro
        primera_medida = medidas_seleccionadas[0]

        primer_precio = request.form.get(
            f"precio_{primera_medida}"
        )

        if not primer_precio:
            return "Debes indicar el precio de la medida seleccionada"

        nuevo_cuadro = Cuadro(
            nombre=request.form["nombre"],
            descripcion=request.form.get("descripcion", ""),
            stock=request.form["stock"],
            peso=request.form.get("peso") or None,
            id_categoria=request.form["id_categoria"],
            id_luz=request.form["id_luz"],
            destacado="destacado" in request.form,
        )

        db.session.add(nuevo_cuadro)

        # Necesitamos obtener el id_cuadro antes del commit
        db.session.flush()

        # Guardar todas las medidas y sus precios
        for id_medida in medidas_seleccionadas:

            precio = request.form.get(
                f"precio_{id_medida}"
            )

            if not precio:
                continue

            nueva_medida = CuadroMedida(
                id_cuadro=nuevo_cuadro.id_cuadro,
                id_medida=id_medida,
                precio=precio
            )

            db.session.add(nueva_medida)

        # IMAGEN PRINCIPAL

        imagen_principal = request.files["imagen_principal"]

        if imagen_principal and imagen_principal.filename != "":

            nombre_archivo = imagen_principal.filename

            imagen_principal.save(
                "static/img/imgCuadros/" + nombre_archivo
            )

            nueva_imagen = Imagen(
                id_cuadro=nuevo_cuadro.id_cuadro,
                ruta_imagen=nombre_archivo,
                es_principal=True
            )

            db.session.add(nueva_imagen)

        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "crearCuadro.html",
        categorias=categorias,
        medidas=medidas,
        luces=luces
    )


@app.route("/editar/<int:id_cuadro>", methods=["GET", "POST"])
def editar(id_cuadro):

    cuadro = buscar_cuadro(id_cuadro)

    if cuadro is None:
        return "Cuadro no encontrado", 404

    categorias = Categoria.query.all()
    medidas = Medida.query.all()
    luces = Luz.query.all()

    if request.method == "POST":

        medidas_seleccionadas = request.form.getlist(
            "medidas_seleccionadas"
        )

        if not medidas_seleccionadas:
            return "Debes seleccionar al menos una medida"

        # Primera medida seleccionada
        primera_medida = medidas_seleccionadas[0]

        primer_precio = request.form.get(
            f"precio_{primera_medida}"
        )

        if not primer_precio:
            return "Debes indicar el precio de la medida seleccionada"


        # DATOS GENERALES DEL CUADRO

        cuadro.nombre = request.form["nombre"]

        cuadro.descripcion = request.form.get(
            "descripcion",
            ""
        )

        cuadro.stock = request.form["stock"]

        cuadro.peso = (
            request.form.get("peso") or None
        )

        cuadro.id_categoria = request.form["id_categoria"]

        cuadro.id_luz = request.form["id_luz"]

        cuadro.destacado = (
            "destacado" in request.form
        )





        # --------------------------------
        # ACTUALIZAR MEDIDAS Y PRECIOS
        # --------------------------------

        # Borramos las asociaciones anteriores
        CuadroMedida.query.filter_by(
            id_cuadro=cuadro.id_cuadro
        ).delete()


        # Creamos nuevamente las seleccionadas

        for id_medida in medidas_seleccionadas:

            precio = request.form.get(
                f"precio_{id_medida}"
            )

            if not precio:
                continue

            nueva_medida = CuadroMedida(
                id_cuadro=cuadro.id_cuadro,
                id_medida=id_medida,
                precio=precio
            )

            db.session.add(nueva_medida)


        # --------------------------------
        # IMAGEN PRINCIPAL
        # --------------------------------

        imagen_nueva = request.files.get(
            "imagen_principal"
        )

        if imagen_nueva and imagen_nueva.filename != "":

            nombre_archivo = imagen_nueva.filename

            imagen_nueva.save(
                "static/img/imgCuadros/" + nombre_archivo
            )

            imagen_principal = next(
                (
                    imagen
                    for imagen in cuadro.imagenes
                    if imagen.es_principal
                ),
                None
            )

            if imagen_principal:

                imagen_principal.ruta_imagen = nombre_archivo

            else:

                nueva_imagen = Imagen(
                    id_cuadro=cuadro.id_cuadro,
                    ruta_imagen=nombre_archivo,
                    es_principal=True
                )

                db.session.add(nueva_imagen)


        resultado = editar_cuadro(cuadro)

        if resultado is None:
            return "Error al editar el cuadro", 500

        return redirect("/dashboard")


    return render_template(
        "editarCuadro.html",
        cuadro=cuadro,
        categorias=categorias,
        medidas=medidas,
        luces=luces
    )

@app.route("/eliminar/<int:id_cuadro>")
def eliminar(id_cuadro):

    eliminar_cuadro(id_cuadro)

    return redirect("/dashboard")


@app.route("/agregar-carrito", methods=["POST"])
def agregar_carrito():

    id_cuadro = int(request.form["id_cuadro"])
    id_cuadro_medida = int(request.form["id_cuadro_medida"])

    carrito = session.get("carrito", [])

    encontrado = False

    for item in carrito:

        if (
            item["id_cuadro"] == id_cuadro
            and item["id_cuadro_medida"] == id_cuadro_medida
        ):
            item["cantidad"] += 1
            encontrado = True
            break

    if not encontrado:

        carrito.append({
            "id_cuadro": id_cuadro,
            "id_cuadro_medida": id_cuadro_medida,
            "cantidad": 1
        })

    session["carrito"] = carrito

    cantidad_total = sum(
        item["cantidad"] for item in carrito
    )

    return {
        "ok": True,
        "cantidad": cantidad_total
    }


@app.route("/datos-carrito")
def datos_carrito():

    carrito = session.get("carrito", [])

    productos = []
    subtotal = 0

    for item in carrito:

        cuadro = db.session.get(
            Cuadro,
            item["id_cuadro"]
        )

        opcion = db.session.get(
            CuadroMedida,
            item["id_cuadro_medida"]
        )

        if cuadro is None or opcion is None:
            continue

        imagen_principal = None

        for imagen in cuadro.imagenes:
            if imagen.es_principal:
                imagen_principal = imagen.ruta_imagen
                break

        cantidad = item["cantidad"]

        precio_unitario = float(opcion.precio)

        total_item = precio_unitario * cantidad

        subtotal += total_item

        productos.append({
            "id_cuadro": cuadro.id_cuadro,
            "id_cuadro_medida": opcion.id_cuadro_medida,

            "nombre": cuadro.nombre,

            "medida":
                f"{int(opcion.medida.ancho)} × "
                f"{int(opcion.medida.alto)} cm",

            "imagen": imagen_principal,

            "cantidad": cantidad,

            "precio_unitario": precio_unitario,

            "total": total_item
        })

    return {
        "ok": True,
        "productos": productos,
        "subtotal": subtotal,
        "total": subtotal
    }


@app.route("/cambiar-cantidad-carrito", methods=["POST"])
def cambiar_cantidad_carrito():

    id_cuadro = int(request.form["id_cuadro"])
    id_cuadro_medida = int(request.form["id_cuadro_medida"])
    cambio = int(request.form["cambio"])

    carrito = session.get("carrito", [])

    for item in carrito:

        if (
            item["id_cuadro"] == id_cuadro
            and item["id_cuadro_medida"] == id_cuadro_medida
        ):

            item["cantidad"] += cambio

            if item["cantidad"] <= 0:
                carrito.remove(item)

            break

    session["carrito"] = carrito

    cantidad_total = sum(
        item["cantidad"] for item in carrito
    )

    return {
        "ok": True,
        "cantidad": cantidad_total
    }


@app.route("/eliminar-del-carrito", methods=["POST"])
def eliminar_del_carrito():

    id_cuadro = int(request.form["id_cuadro"])
    id_cuadro_medida = int(request.form["id_cuadro_medida"])

    carrito = session.get("carrito", [])

    carrito = [
        item for item in carrito
        if not (
            item["id_cuadro"] == id_cuadro
            and item["id_cuadro_medida"] == id_cuadro_medida
        )
    ]

    session["carrito"] = carrito

    cantidad_total = sum(
        item["cantidad"] for item in carrito
    )

    return {
        "ok": True,
        "cantidad": cantidad_total
    }


@app.route("/categoria/<int:id_categoria>")
def ver_categoria(id_categoria):

    cuadros = obtener_cuadros_por_categoria(id_categoria)
    destacados = obtener_destacados()
    categorias = Categoria.query.all()

    usuario = None

    if "usuario_id" in session:
        usuario = db.session.get(
            Usuario,
            session["usuario_id"]
        )

    return render_template(
        "index.html",
        cuadros=cuadros,
        destacados=destacados,
        categorias=categorias,
        usuario=usuario
    )

@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        password = request.form["password"]

        usuario_existente = Usuario.query.filter_by(email=email).first()

        if usuario_existente:
            return "Ya existe un usuario registrado con ese email"

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            password=generate_password_hash(password),
            rol="cliente",
            fecha_registro=datetime.now()
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("registro.html")



@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password, password):

            session["usuario_id"] = usuario.id_usuario
            session["usuario_nombre"] = usuario.nombre
            session["usuario_rol"] = usuario.rol

            return redirect(url_for("inicio"))

        return "Email o contraseña incorrectos"

    return render_template("login.html")

@app.route("/mi-cuenta")
def mi_cuenta():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    usuario = db.session.get(
        Usuario,
        session["usuario_id"]
    )

    return render_template(
        "mi_cuenta.html",
        usuario=usuario
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("inicio"))