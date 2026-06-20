from datetime import datetime

produtos = []
print("===== sistema de controle de validade de dados =====")

while True:
    print("\n1 - cadastrar produto")
    print("2 - sair")
    print("3 - ver produtos cadastrados")

    opcao = input("Digite a opção desejada: ")

    if opcao == "2":
        print("Saindo do sistema...")
        break

    if opcao == "3":
        print("\nProdutos cadastrados:")
        if produtos:
            for produto in produtos:
                print(f"Nome: {produto['produto']}, Validade: {produto['validade']}, Status: {produto['status']}")
        else:
            print("Nenhum produto cadastrado.")
        continue

    if opcao == "1":
        produto = input("Nome do produto: ")
        validade = input("Data de validade (dd/mm/aaaa): ")

        try:
            data_validade = datetime.strptime(validade, "%d/%m/%Y")
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa.")
            continue

        hoje = datetime.now()

        if data_validade >= hoje:
            status = "válido"
        else:
            status = "vencido"

        produtos.append({
            "produto": produto,
            "validade": validade,
            "status": status
        })

        print("\nProduto cadastrado com sucesso!")
        print(f"Nome: {produto}")
        print(f"Data de validade: {validade}")
        print(f"Status: {status}")
        continue

    print("Opção inválida. Tente novamente.")
