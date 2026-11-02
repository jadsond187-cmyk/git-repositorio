const express = require("express");
const mysql = require("mysql2");
const path = require("path");
const fs = require("fs");
const app = express();
require("dotenv").config({ path: path.join(__dirname, ".env") });

// Log básico de requisições para diagnóstico
app.use((req, res, next) => {
    console.log(`[request] ${req.method} ${req.url}`);
    next();
});

// Permite receber dados em JSON e formulários
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Pasta do currículo e das páginas dos projetos
const curriculoAlphaDir = path.resolve(__dirname, "..");
app.use("/projetocadastro", (req, res) => {
    res.sendStatus(404);
});
app.use(express.static(curriculoAlphaDir));

// Conexão com o MySQL
const conexao = mysql.createConnection({
    host: process.env.DB_HOST,
    port: Number(process.env.DB_PORT),
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    ssl: {
        ca: fs.readFileSync(path.join(__dirname, "ca.pem"))
    }
});

conexao.connect((erro) => {
    if (erro) {
        console.log("Erro ao conectar:", erro);
        return;
    }

    console.log("Conectado ao MySQL!");
});

// Página inicial
app.get("/", (req, res) => {
    res.sendFile(path.join(curriculoAlphaDir, "index.html"));
});

// Cadastro de segredo
app.post("/cadastro", (req, res) => {
    const { segredo, categoria } = req.body;
    const sql = "INSERT INTO segredos(segredo, categoria) VALUES (?, ?)";

    conexao.query(sql, [segredo, categoria], (erro) => {
        if (erro) {
            console.log(erro);
            return res.send("Erro ao cadastrar o segredo.");
        }

        res.send("Segredo cadastrado com sucesso!");
    });
});

// Lista segredos
app.get("/segredos", (req, res) => {
    console.log("Rota /segredos foi acessada");

    conexao.query("SELECT * FROM segredos", (erro, resultados) => {
        console.log("Entrou no callback");

        if (erro) {
            console.log("Erro:", erro);
            return res.send(erro.message);
        }

        res.json(resultados);
    });
});
// Nota: o `express.static` serve o currículo, sem expor os arquivos do servidor.
const PORT = 3000;

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});
// atualização para novo deploy