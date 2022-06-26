from crypt import methods
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)

def cassandra():
    cluster = Cluster(contact_points=['cassandra_nodo1','cassandra_nodo2','cassandra_nodo3'],
                      port= 9042,
                      auth_provider=PlainTextAuthProvider(username='cassandra', password='tarea3'))
    session1= cluster.connect('pacientes',wait_for_all_pools=False)
    session1.execute('USE pacientes')
    session2= cluster.connect('recetas',wait_for_all_pools=False)
    session2.execute('USE recetas')
    return session1, session2

@app.route("/pacientes")
def pacientes():
    pacientes = cassandra()
    query = "SELECT * FROM pacientes.paciente;"
    rows = pacientes.execute(query)
    return render_template("pacientes.html", pacientes=rows)

@app.route("/recetas")
def recetas():
    recetas = cassandra()
    query = "SELECT * FROM recetas.receta;"
    rows = recetas.execute(query)
    return render_template("recetas.html", recetas=rows)

@app.route('/create',methods = ['GET', 'POST'])
def create_receta():
    pacientes, recetas = cassandra()
    if request.method == 'POST':
        
        #Obtención datos formulario.
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        rut = request.form['rut']
        email = request.form['email']
        fecha_nacimiento = request.form['fecha_nacimiento']
        comentario = request.form['comentario']
        farmacos = request.form['farmacos']
        doctor = request.form['doctor']

        #Obtención de pacientes ya ingresados
        query = "SELECT id, rut FROM pacientes.paciente;"
        rows = pacientes.execute(query)
        lista_ruts = []
        max_id_paciente = 0
        for row in rows:
            lista_ruts.append(row.rut)
            if(max_id_paciente < row.id):
                max_id_paciente = row.id
        

        query = "SELECT id FROM recetas.receta;"
        rows = recetas.execute(query)
        max_id_receta = 0
        for row in rows:
            if(max_id_receta < row.id):
                max_id_receta = row.id

        #Si el paciente no está, se ingresa tanto él/ella como la receta
        if(rut not in lista_ruts):
            query = "INSERT INTO pacientes.paciente(id, nombre, apellido, rut, email, fecha_nacimiento) VALUES(?, ?, ?, ?, ?, ?);"
            preparar = pacientes.prepare(query)
            pacientes.execute(preparar, (max_id_paciente+1, nombre, apellido, rut, email, fecha_nacimiento))

            '''query= "SELECT id FROM pacientes.paciente WHERE rut='"+rut+"' ALLOW FILTERING;"
            result = pacientes.execute(query)
            for row in result:
                id_paciente = row.id'''

            query = "INSERT INTO recetas.receta(id, id_paciente, comentario, farmacos, doctor) VALUES(?,?,?,?,?);"
            preparar = recetas.prepare(query)
            recetas.execute(preparar, (max_id_receta + 1, max_id_paciente + 1, comentario, farmacos, doctor))

            return render_template('create.html', valores= 'Receta y usuario ingresados exitosamente')

        #Paciente ya existente, se crea solo la receta
        else:
            query= "SELECT id FROM pacientes.paciente WHERE rut='"+rut+"' ALLOW FILTERING;"
            result = pacientes.execute(query)
            for row in result:
                id_paciente = row.id

            query = "INSERT INTO recetas.receta(id, id_paciente, comentario, farmacos, doctor) VALUES(?,?,?,?,?);"
            preparar = recetas.prepare(query)
            recetas.execute(preparar, (max_id_receta + 1, id_paciente, comentario, farmacos, doctor))

            return render_template('create.html', valores= 'Receta ingresada exitosamente')

    return render_template('create.html')

@app.route('/delete', methods = ['GET', 'POST'])
def delete_receta():
    pacientes, recetas = cassandra()
    if request.method == 'POST':
        id_receta = request.form['id_receta']
        query = "DELETE FROM recetas.receta WHERE id ="+id_receta+" ;"
        recetas.execute(query)
    return render_template('delete.html', valor= 'Receta eliminada exitosamente')
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
    app.run(host='0.0.0.0', port=3000 , debug=True)



