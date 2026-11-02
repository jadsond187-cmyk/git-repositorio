// ====================================
// BANCO DE DADOS LOCAL
// ====================================

const BASE_URL = "http://localhost:5000";

// ====== FUNÇÕES AUXILIARES ======
function mostrarMensagem(texto, tipo = 'info') {
    console.log(`[${tipo.toUpperCase()}] ${texto}`);
    const elem = document.getElementById('mensagem');
    if (elem) {
        elem.textContent = texto;
        elem.className = `mensagem ${tipo}`;
        setTimeout(() => elem.className = 'mensagem', 5000);
    }
}

function limparFormulario() {
    document.getElementById('id_edicao').value = '';
    document.getElementById('nome').value = '';
    document.getElementById('idade').value = '';
    document.getElementById('cidade').value = '';
}

// ====== CADASTRAR ======
function cadastrar(nome, idade, cidade) {
    if (!nome || !idade || !cidade) {
        mostrarMensagem('❌ Todos os campos são obrigatórios!', 'erro');
        return;
    }

    fetch(`${BASE_URL}/cadastrar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, idade, cidade })
    })
    .then(r => r.json())
    .then(data => {
        mostrarMensagem(data.mensagem || data.erro, data.erro ? 'erro' : 'sucesso');
        if (!data.erro) {
            limparFormulario();
            consultar();
        }
    })
    .catch(err => {
        mostrarMensagem('❌ Erro ao cadastrar', 'erro');
        console.error(err);
    });
}

// ====== CONSULTAR ======
function consultar() {
    fetch(`${BASE_URL}/consultar`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(r => r.json())
    .then(data => {
        let html = '<h2>📊 Registros no Banco de Dados</h2>';
        
        if (!Array.isArray(data) || data.length === 0) {
            html += '<p style="color: #666;">Nenhum registro encontrado</p>';
        } else {
            html += `<p style="color: #666;">Total: <strong>${data.length}</strong> registro(s)</p>`;
            html += '<table><tr><th>ID</th><th>Nome</th><th>Idade</th><th>Cidade</th><th>Ações</th></tr>';
            
            data.forEach(pessoa => {
                html += `<tr>
                    <td>#${pessoa.id}</td>
                    <td>${pessoa.nome}</td>
                    <td>${pessoa.idade}</td>
                    <td>${pessoa.cidade}</td>
                    <td>
                        <button onclick="editar(${pessoa.id}, '${pessoa.nome}', ${pessoa.idade}, '${pessoa.cidade}')">Editar</button>
                        <button onclick="deletar(${pessoa.id})">Deletar</button>
                    </td>
                </tr>`;
            });
            html += '</table>';
        }
        
        document.getElementById('resultado').innerHTML = html;
    })
    .catch(err => {
        mostrarMensagem('❌ Erro ao consultar', 'erro');
        console.error(err);
    });
}

// ====== ATUALIZAR ======
function atualizar(id, nome, idade, cidade) {
    if (!id || !nome || !idade || !cidade) {
        mostrarMensagem('❌ Todos os campos são obrigatórios!', 'erro');
        return;
    }

    fetch(`${BASE_URL}/atualizar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, nome, idade, cidade })
    })
    .then(r => r.json())
    .then(data => {
        mostrarMensagem(data.mensagem || data.erro, data.erro ? 'erro' : 'sucesso');
        if (!data.erro) {
            limparFormulario();
            consultar();
        }
    })
    .catch(err => {
        mostrarMensagem('❌ Erro ao atualizar', 'erro');
        console.error(err);
    });
}

// ====== DELETAR ======
function deletar(id) {
    if (!confirm('Tem certeza que deseja deletar este registro?')) {
        return;
    }

    fetch(`${BASE_URL}/deletar/${id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(r => r.json())
    .then(data => {
        mostrarMensagem(data.mensagem || data.erro, data.erro ? 'erro' : 'sucesso');
        if (!data.erro) {
            limparFormulario();
            consultar();
        }
    })
    .catch(err => {
        mostrarMensagem('❌ Erro ao deletar', 'erro');
        console.error(err);
    });
}

// ====== EDITAR ======
function editar(id, nome, idade, cidade) {
    document.getElementById('id_edicao').value = id;
    document.getElementById('nome').value = nome;
    document.getElementById('idade').value = idade;
    document.getElementById('cidade').value = cidade;
    mostrarMensagem(`✏️ Editando: ${nome}`, 'info');
    document.getElementById('nome').focus();
}