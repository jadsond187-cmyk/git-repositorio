cadastros = []

def cadastrar():
    nome = input("Nome: ")
    idade = int(input("Idade: "))
    cidade = input("Cidade: ")

    pessoa = {
        "nome": nome,
        "idade": idade,
        "cidade": cidade
    }

    cadastros.append(pessoa)
    print("\nCadastro realizado com sucesso!\n")


def listar():
    if len(cadastros) == 0:
        print("\nNenhum cadastro encontrado.\n")
        return

    print("\n--- CADASTROS ---")
    for i, pessoa in enumerate(cadastros, start=1):
        print(f"\nCadastro {i}")
        print(f"Nome: {pessoa['nome']}")
        print(f"Idade: {pessoa['idade']}")
        print(f"Cidade: {pessoa['cidade']}")
    print()


while True:
    print("=== SISTEMA DE CADASTRO ===")
    print("1 - Cadastrar pessoa")
    print("2 - Listar cadastros")
    print("3 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar()

    elif opcao == "2":
        listar()

    elif opcao == "3":
        print("Sistema encerrado.")
        break

    else:
        print("Opção inválida.\n")