from flask import Flask
from app.models import db, Producto

app = Flask(__name__)
app.config["SECRET_KEY"] = "una_contraseña_segura_al_azar"

# configuración de la base de datos (En local  SQLite)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.db"
app.config["SQLALCHEMY_TACK_MODIFICATIONS"] = "false"

# Vinculamos SQLAlchimy con nuestra aplicación de Flask
db.init_app(app)

with app.app_context():
    db.create_all()  # Crea las tablas en la base de datos (si no existieran)

    if not Producto.query.first():
        nuevo_producto = Producto(nombre="Teclado Mecánico RGB", precio=49.99)
        db.session.add(nuevo_producto)
        db.session.commit()
        print(">>> Producto de prueba insertado en la BD. <<<<<<<<<<<<<<<<<<<<<<")


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/test.db")
def test_db():
    productos = Producto.query.all()
    return f"Todos los productos: {productos}"


@app.route("/nuevo-producto/<string:nombre>/<float:precio>")
def nuevoProducto(nombre, precio):
    nuevo_producto = Producto(nombre=nombre, precio=precio)
    db.session.add(nuevo_producto)
    db.session.commit()
    producto = Producto.query.order_by(Producto.id.desc()).first()
    return f"Nuevo producto agregado: {producto}"


if __name__ == "__main__":
    app.run(debug=True)
