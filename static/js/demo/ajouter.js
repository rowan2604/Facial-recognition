var input1 = document.getElementById('photo1'),
    input2 = document.getElementById('photo2'),
    input3 = document.getElementById('photo3'),
    input4 = document.getElementById('photo4'),
    input5 = document.getElementById('photo5'),
    input6 = document.getElementById('photo6'),
    input7 = document.getElementById('photo7'),

	div1 = document.getElementById('taille1'),
    div2 = document.getElementById('taille2'),
    div3 = document.getElementById('taille3'),
    div4 = document.getElementById('taille4'),
    div5 = document.getElementById('taille5'),
    div6 = document.getElementById('taille6'),
    div7 = document.getElementById('taille7');

function analyse(e){
	var file = e.target.files[0];
	console.log("Je suis la ma couille !")
	div1.innerHTML = "Type : "+ file.type +"<br />"+ "Taille : "+ file.size +" octets";
}

// input2.addEventListener("change", analyse, false);
// input3.addEventListener("change", analyse, false);
// input4.addEventListener("change", analyse, false);
// input5.addEventListener("change", analyse, false);
// input6.addEventListener("change", analyse, false);
// input7.addEventListener("change", analyse, false);