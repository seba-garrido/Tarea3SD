from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

ap = PlainTextAuthProvider(username = 'cassandra', password = 'password123')


cluster = Cluster(['localhost'],auth_provider=ap)




session_pacientes = cluster.connect('pacientes')
#rows = session.execute("SELECT * FROM productos")
#print("Productos")
#print("Nombre | Descripcion | Precio")
#print("-----------------------------")
#for row in rows:
   # print(row.nombre," | ", row.descripcion," | ", row.precio)
#print("Finished")







#create keyspace productos with replication = {'class':'SimpleStrategy', 'replication_factor':2}
#create table productos(nombre text primary key, descripcion text, precio int);

##def insertar_producto(nombre, descripcion, precio):
    ##session.execute("INSERT INTO productos(nombre, descripcion, precio) VALUES (%s,%s,%s)",(nombre, descripcion, precio))
    
def obtener_prodcuto():
    pacientes = session_pacientes.execute("SELECT * FROM paciente")
    return pacientes

#def eliminar_producto(nombre):
    #session.execute("DELETE FROM productos WHERE nombre = '{0}'".format(nombre))
    
#def obtener_producto_por_nombre(nombre):
    #producto = session.execute("SELECT * FROM productos WHERE nombre = %s",(nombre))
    #return producto

#def actualizar_producto(nombre, descripcion, precio):
    #session.execute("UPDATE productos SET descripcion = %s, precio = %s WHERE nombre = %s", (descripcion, precio, nombre))
    
