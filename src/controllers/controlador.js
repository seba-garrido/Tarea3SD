var cassandra = require('cassandra-driver');
var async = require('async');
let authProvider = new cassandra.auth.PlainTextAuthProvider('cassandra', 'cassandra');
let contactPoints = ['127.0.0.1'];
let localDataCenter = 'cassandra-cluster';
var bd_pacientes = new cassandra.Client({ contactPoints: contactPoints, authProvider: authProvider, localDataCenter: localDataCenter, keyspace: 'pacientes' });
var bd_recetas = new cassandra.Client({ contactPoints: contactPoints, authProvider: authProvider, localDataCenter: localDataCenter, keyspace: 'recetas' });

const query_pacientes = 'SELECT * FROM paciente';
const query_recetas = 'SELECT * from receta';

let q1 = bd_pacientes.execute(query_pacientes).then(result => console.log('Paciente : ' + result.rows[0].nombre));
let q2 = bd_recetas.execute(query_recetas).then(result => console.log('Doctor : ' + result.rows[0].doctor));
module.exports = bd_pacientes, bd_recetas;