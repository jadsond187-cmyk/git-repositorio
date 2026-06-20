// Tema escuro

const temaBtn =
document.getElementById("temaBtn");

if(temaBtn){

temaBtn.addEventListener(
"click",
function(){

document.body.classList.toggle("dark");

});

}

// Formulário

const formulario =
document.getElementById("formulario");

if(formulario){

formulario.addEventListener(
"submit",
function(event){

event.preventDefault();

let nome =
document.getElementById("nome").value;

let email =
document.getElementById("email").value;

let mensagem =
document.getElementById("mensagem").value;

if(
nome === "" ||
email === "" ||
mensagem === ""
){

alert(
"Preencha todos os campos."
);

return;

}

let regex =
/^[^\s@]+@[^\s@]+\.[^\s@]+$/;

if(!regex.test(email)){

alert(
"Digite um e-mail válido."
);

return;

}

alert(
"Mensagem enviada com sucesso!"
);

formulario.reset();

});

}