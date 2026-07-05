from flask import Flask, render_template, request, redirect
from cadastro import listar, cadastrar, deletar

app = Flask(__name__)

@app.route("/")
def index():
    pessoas = listar()
    return render_template("index.html", pessoas=pessoas)

@app.route("/cadastrar", methods=["POST"])
def rota_cadastrar():
    nome = request.form["nome"]
    idade = request.form["idade"]
    cidade = request.form["cidade"]

    cadastrar(nome, idade, cidade)
    return redirect("/")

@app.route("/deletar/<int:id>")
def rota_deletar(id):
    deletar(id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)