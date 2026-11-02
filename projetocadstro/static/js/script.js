function mostrarMensagem(texto, tipo) {
    const elem = document.getElementById('mensagem');
    elem.textContent = texto;
    elem.className = `mensagem ${tipo}`;
    setTimeout(() => elem.className = 'mensagem', 5000);
}

function limparFormulario() {
    document.getElementById('id_edicao').value = '';
    document.getElementById('nome').value = '';
    document.getElementById('idade').value = '';
    document.getElementById('cidade').value = '';
}

function cadastrar() {
    const id = document.getElementById('id_edicao').value;
    const nome = document.getElementById('nome').value.trim();
    const idade = document.getElementById('idade').value;
    const cidade = document.getElementById('cidade').value.trim();

    if (!nome || !idade || !cidade) {
        mostrarMensagem('❌ Todos os campos são obrigatórios!', 'erro');
        return;
    }

    const url = id ? '/atualizar' : '/cadastrar';
    const dados = id ? { id, nome, idade, cidade } : { nome, idade, cidade };

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
    })
    .then(r => r.json())
    .then(data => {
        if (data.erro) {
            mostrarMensagem(`❌ ${data.erro}`, 'erro');
        } else {
            mostrarMensagem(data.mensagem, 'sucesso');
            limparFormulario();
            consultar();
        }
    })
    .catch(err => {
        mostrarMensagem('❌ Erro ao salvar', 'erro');
        console.error(err);
    });
}

function consultar() {
    fetch('/consultar', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(r => r.json())
    .then(data => {
        let html = '<h2>📊 Registros no Banco de Dados</h2>';
        
        if (!Array.isArray(data) || data.length === 0) {
            html += '<p style="color: #666; padding: 20px; text-align: center;">Nenhum registro encontrado</p>';
        } else {
            html += `<p style="color: #666; margin-bottom: 10px;">Total: <strong>${data.length}</strong> registro(s)</p>`;
            html += '<table><thead><tr><th>ID</th><th>Nome</th><th>Idade</th><th>Cidade</th><th>Ações</th></tr></thead><tbody>';
            
            data.forEach(pessoa => {
                html += `
                    <tr>
                        <td>#${pessoa.id}</td>
                        <td>${pessoa.nome}</td>
                        <td>${pessoa.idade}</td>
                        <td>${pessoa.cidade}</td>
                        <td class="acoes">
                            <button class="btn-editar" onclick="editar(${pessoa.id}, '${pessoa.nome}', ${pessoa.idade}, '${pessoa.cidade}')">✏️ Editar</button>
                            <button class="btn-deletar" onclick="confirmarDeletar(${pessoa.id}, '${pessoa.nome}')">🗑️ Deletar</button>
                        </td>
                    </tr>
                `;
            });
            html += '</tbody></table>';
        }
        
        document.getElementById('resultado').innerHTML = html;
        document.getElementById('resultado').style.display = 'block';
    })
    .catch(err => {
        mostrarMensagem('❌ Erro ao consultar', 'erro');
        console.error(err);
    });
}

function editar(id, nome, idade, cidade) {
    document.getElementById('id_edicao').value = id;
    document.getElementById('nome').value = nome;
    document.getElementById('idade').value = idade;
    document.getElementById('cidade').value = cidade;
    document.getElementById('nome').focus();
    mostrarMensagem(`✏️ Editando: ${nome}`, 'sucesso');
    window.scrollTo(0, 0);
}

function confirmarDeletar(id, nome) {
    if (confirm(`Tem certeza que deseja deletar "${nome}"?`)) {
        deletar(id);
    }
}

function deletar(id) {
    fetch(`/deletar/${id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(r => r.json())
    .then(data => {
        if (data.erro) {
            mostrarMensagem(`❌ ${data.erro}`, 'erro');
        } else {
            mostrarMensagem(data.mensagem, 'sucesso');
            limparFormulario();
            consultar();
        }
    })
    .catch(err => {
        mostrarMensagem('❌ Erro ao deletar', 'erro');
        console.error(err);
    });
}
