const { Router } = require('express');
//const bd_pacientes = require('../controllers/controlador');
//const bd_recetas = require('../controllers/controlador');
const router = Router();
let cassandra = require('cassandra-driver');
var async = require('async');
let authProvider = new cassandra.auth.PlainTextAuthProvider('cassandra', 'cassandra');
const contactPoints = ['localhost'];
const localDataCenter = 'datacenter1';
let bd_pacientes = new cassandra.Client({
    contactPoints: contactPoints,
    localDataCenter: localDataCenter,
    keyspace: 'pacientes'
});
let bd_recetas = new cassandra.Client({
    contactPoints: contactPoints,
    localDataCenter: localDataCenter,
    keyspace: 'recetas'
});

let query_pacientes = 'SELECT * FROM paciente';
let query_recetas = 'SELECT * from receta';

//bd_pacientes.execute(query_pacientes).then(result => console.log('Paciente : ' + result.rows[0].nombre));
//bd_recetas.execute(query_recetas).then(result => console.log('Doctor : ' + result.rows[0].doctor));

router.get('/test', (req, res) => {
    const data = {
        "Nombre": "Sebastian v2",
        "Apellido": "Garrido v2"
    };
    res.json(data);
});

router.get('/pacientes', (req, res) => {
    //console.table(bd_pacientes.rows);
    //res.json(data_pacientes);
    //console.log(data_pacientes);
    bd_pacientes.execute(query_pacientes, function(error, result) {
        if (error != undefined) {
            console.log('Error ', error);
        } else {
            console.table(result.rows);
        }
    });
});

router.get('/recetas', (req, res) => {
    //console.table(bd_recetas.rows);
    //res.json(data_recetas);
    //console.log(data_recetas);
    bd_recetas.execute(query_recetas).then(result => console.log('Doctor : ' + result.rows[0].doctor));
});

module.exports = router;