const port = 8100;

const express = require('express');
const mysql = require('mysql');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);

app.use(express.static(__dirname));

app.get('/', (req, res, next) => {
	res.sendFile(__dirname + '/pageBDD.html');
});

const con = mysql.createConnection({
	host: 'localhost',
	user: 'root',
	password: '',
	database: 'test'
});

io.sockets.on('connection', (socket) => {
	con.query('SELECT * FROM etudiant ORDER BY nom', (err, rows) => {
		socket.emit('data', rows);
	});
});

server.listen(port);
console.log('server started!');