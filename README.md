# Tarea N°3 Sistemas Distribuidos 2022

## Integrantes:


Sebastian Garrido

Jorge Fernández

## Comanados:
lo primero es hacer un build del docker-compose:
- docker-compose build
En segunda instancia hay que hacer un docker-compose up:
- docker-compose up --force-recreate
Porsterior a esto se puede revisar a través de la consola que estos contenedores se encuentre arriba, como se aprecia en la imagen:
- Comando: sudo docker ps
![image](https://user-images.githubusercontent.com/70417046/175835041-787cc6da-87ac-4ec4-950f-ac51292f800e.png)


## Preguntas:


1. Explique la arquitectura que Cassandra maneja. Cuando se crea el cluster ¿Como los nodos se conectan? ¿Qué ocurre cuando un cliente realiza una petición a uno de los nodos? ¿Qué ocurre cuando uno de los nodos se desconecta? ¿La red generada entre los nodos siempre es eficiente? ¿Existe balanceo de carga?

La arquitectura que Cassandra emplea es la de un sistema peer to peer (p2p), lo que implica que todos los nodos tienen la misma importancia por lo que el modelo maestro-esclavo no se aplica en este caso, de esta forma ningún nodo tendrá información de más con respecto al resto, lo que permite que cualquiera puede tomar el rol de coordinador de una query, por lo que cassandra efectúa dicha asignación. Todo este sistema (p2p) permite que los nodos puedan comunicarse y compartir entre sí de mejor manera. Además, Cassandra distribuye los datos a lo largo de los nodos dentro del cluster, replicándolos en caso de un eventual fallo. También utiliza estrategias para la replicación de datos, las cuales son NetworkTopologyStrategy y SimpleStrategy.
Al momento de crear un cluster los nodos se conectan entre sí utilizando el protocolo Gossip, el cual efectúa la comunicación de los nodos entre pares, de esta forma se van propagando y comunicando dentro del sistema. Al momento de que un cliente efectúa la petición a uno de los nodos y este emite una solicitud de escritura o lectura, dicho nodo sirve como coordinador para ese cliente en particular para dicha operación. En el caso de desconectarse uno de los nodos, al tener todos los nodos iguales (trabajando con el sistema p2p), Cassandra misma asigna nuevamente a otro nodo como coordinador de dicha operación. En la red pueden generarse fallos entre los nodos pero al usar el protocolo Gossip se pueden detectar dichos fallos, además cuando falla un nodo los pods de Cassandra quedan en estado pendiente (pending) y si se efectúa balanceo de carga entre los servidores del backend en la red, al momento de tener datos y recursos distribuidos en el sistema.


2. Cassandra posee principalmente dos estrategias para mantener redundancia en la replicación de datos. ¿Cuáles son estos? ¿Ćual es la ventaja de uno sobre otro? ¿Cuál utilizaría usted para en el caso actual y por qué? Justifique apropiadamente su respuesta.

Estas estrategias son NetworkTopologyStrategy y SimpleStrategy, donde cada una se caracteriza de la siguiente forma:

NetworkTopologyStrategy:

En esta estrategia podemos almacenar múltiples copias de los datos en diferentes centros de datos cuando sea necesario. Una de las razones importantes para utilizar NetworkTopologyStrategy es cuando se deben colocar varios nodos de réplica en diferentes centros de datos.

SimpleStrategy:

Por otra parte, SimpleStrategy es una estrategia más simple que se recomienda ocupar al tener múltiples nodos en múltiples racks en tan solo un centro de datos.

Para este caso utilizaría SimpleStrategy, ya que al tener un sistema que trabaja de forma distribuida con tan solo un centro de datos, esta estrategia funcionará de mejor manera al tener múltiples nodos trabajando en un mismo centro.

3. Teniendo en cuenta el contexto del problema ¿Usted cree que la solución propuesta es la correcta? ¿Qué ocurre cuando se quiere escalar en la solución? ¿Qué mejoras implementaria? Oriente su respuesta hacia el Sharding (la replicación/distribución de los datos) y comente una estrategia que podría seguir para ordenar los datos.

Sí dado que efectúa el proceso del sistema de autenticación mediante la estructura Cassandra al tener nodos comunicándose entre si con la API REST, ahora bien al querer escalar el sistema, ya sea utilizando alguna de las técnicas (replicación, distribución y caché)  para poder efectuar ello Cassandra funciona con escalabilidad horizontal y vertical. Una de las mejoras que implementaria sería la replicación y distribución de los datos entre nodos, cosa de poder ser tolerante a fallos en el sistema al por ejemplo caerse un nodo, esté en el cluster se reemplaza por otro que sea el coordinador por ejemplo, una estrategia para poder llevar a cabo ello sería utilizar SimpleStrategy, la cual permitiría un mejor funcionamiento y ordenamiento al momento de tener varios nodos trabajando dentro de un cluster. 
