printTab();

function printTab(){
	let etudiants = [["Bouville", "Jean-Charles", "CIR3", "1"], ["Crespel", "Rémy", "CIR3", "1"],
					 ["Hadjaz", "Rowan", "CIR3", "1"], ["Kaddouri", "Abderzak", "CIR3", "1"]];
	let tab = document.getElementById("Etudiants");
	
	for(let line of etudiants){
		let row = document.createElement("tr");
		for(let str in line){
			let cell = document.createElement("td");
			if(str == 3){
				line[str] == 1 ? cell.style.backgroundColor = "green" : cell.style.backgroundColor = "red";
			}
			else{
				cell.appendChild(document.createTextNode(line[str]));
			}
			row.appendChild(cell);
		}
		tab.appendChild(row);
	}
}