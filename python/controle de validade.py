from datetime import datetime #uma importação de biblioteca que permite trabalhar com datas e horas em Python, fornecendo classes para manipulação de datas, horas e intervalos de tempo.

produtos = []
print("===== sistema de controle de validade de dados =====")
#esse programa nao tem funçoes, ele é um programa simples que permite cadastrar produtos e verificar se eles estão vencidos ou não, usando a data de validade informada pelo usuario. O programa utiliza uma lista para armazenar os produtos cadastrados, e cada produto é representado por um dicionario com as chaves "produto", "validade" e "status". O status é calculado automaticamente com base na data de validade informada pelo usuario.
while True:#menu de opçoes para o usuario escolher
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
