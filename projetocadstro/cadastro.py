def conectar():
    return mysql.connector.connect(
        host="mysql-7f4508f-jadsond187-7af5.l.aivencloud.com",
        port=17207,
        user="avnadmin",
        password="SUA_SENHA_AQUI",
        database="defaultdb",
        ssl_ca="ca.pem"
    )

# -------------------------
# LISTAR
# -------------------------
def listar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pessoas")
    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados

# -------------------------
# CADASTRAR
# -------------------------
def cadastrar(nome, idade, cidade):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO pessoas (nome, idade, cidade) VALUES (%s, %s, %s)",
            (nome, idade, cidade)
        )
        conn.commit()

    except Exception as erro:
        print("ERRO AO INSERIR:", erro)

    finally:
        cursor.close()
        conn.close()

# -------------------------
# DELETAR
# -------------------------
def deletar(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM pessoas WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()