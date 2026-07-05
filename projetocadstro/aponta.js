fetch("https://SEU-SITE.onrender.com/cadastro", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        nome: nome,
        validade: validade
    })
})