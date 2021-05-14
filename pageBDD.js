(function(){
	const socket = io.connect('http://localhost:8100');

	printTab();

	function printTab(){
		let tab = document.getElementById("Etudiants");

		socket.on('data', (rows) => {
			console.log(rows);
			rows.forEach((row) => {
				let ligne = document.createElement("tr");
				let cell = document.createElement("td");
				cell.appendChild(document.createTextNode(row.Nom));
				ligne.appendChild(cell);
				cell = document.createElement("td");
				cell.appendChild(document.createTextNode(row.Prenom));
				ligne.appendChild(cell);
				cell = document.createElement("td");
				cell.appendChild(document.createTextNode(row.Classe));
				ligne.appendChild(cell);
				cell = document.createElement("td");
				row.Presence == 1 ? cell.style.backgroundColor = "green" : cell.style.backgroundColor = "red";
				ligne.appendChild(cell);
				tab.appendChild(ligne);
			}
		)});	
	}
})()