// Tema escuro

const temaBtn = document.getElementById("temaBtn");

function aplicarTemaSalvo() {
  const temaSalvo = localStorage.getItem("curriculoTema");

  if (temaSalvo === "dark") {
    document.body.classList.add("dark");
  } else {
    document.body.classList.remove("dark");
  }
}

aplicarTemaSalvo();

if (temaBtn) {
  temaBtn.addEventListener("click", function () {
    const estaEscuro = document.body.classList.toggle("dark");
    localStorage.setItem("curriculoTema", estaEscuro ? "dark" : "light");
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

let nome = document.getElementById("nome").value.trim();
let email = document.getElementById("email").value.trim();
let mensagem = document.getElementById("mensagem").value.trim();

if(nome === "" || email === "" || mensagem === ""){
  alert("Preencha todos os campos.");
  return;
}

let regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

if(!regex.test(email)){
  alert("Digite um e-mail válido.");
  return;
}

const dados = new FormData(formulario);

fetch("../../php/enviar_contato.php", {
  method: "POST",
  body: dados
})
.then(function(resposta){
  return resposta.json();
})
.then(function(resultado){
  if(resultado.success){
    alert("Mensagem enviada com sucesso!");
    formulario.reset();
  } else {
    alert(resultado.message || "Não foi possível enviar a mensagem.");
  }
})
.catch(function(){
  alert("Erro ao conectar com o servidor. Certifique-se de que o PHP está rodando.");
});

});

}