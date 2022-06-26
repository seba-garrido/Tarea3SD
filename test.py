from crypt import methods
from cassandra.cluster import Cluster
from flask import Flask, render_template, request, redirect, flash
import controlador_productos
cluster = Cluster()

app = Flask(__name__)

@app.route("/agregar_producto")
def formulario_agregar_producto():
    return render_template("agregar_producto.html")

@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = int(request.form["precio"])
    controlador_productos.insertar_producto(nombre, descripcion, precio)
    return redirect("/productos")

@app.route("/")
@app.route("/productos")
def productos():
    productos = controlador_productos.obtener_prodcuto()
    return render_template("productos.html", productos=productos)

@app.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    nombre = request.form["nombre"]
    controlador_productos.eliminar_producto(nombre)
    return redirect("/productos")

#@app.route("/formulario_editar_producto/<text:nombre>")
#def editar_producto(nombre):
 #   producto = controlador_productos.obtener_producto_por_nombre(nombre)
#    return render_template("editar_producto.html", producto=producto)

#@app.route("/actualizar_producto", methods=["POST"])
#def actualizar_producto():
 #   nombre = request.form["nombre"]
  #  descripcion = request.form["descripcion"]
   # precio = int(request.form["precio"])
    #controlador_productos.actualizar_producto(nombre, descripcion, precio)
    #return redirect("/productos")


#session.execute("INSERT INTO productos (nombre, descripcion, precio) VALUES ('jugo test','Este es un jugo creado con test.py', 999)")

#rows = session.execute("SELECT * FROM productos")
#print("Productos")
#print("Nombre | Descripcion | Precio")
#print("-----------------------------")
#for row in rows:
 #   print(row.nombre," | ", row.descripcion," | ", row.precio)
#print("Finished")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000 , debug=True)



