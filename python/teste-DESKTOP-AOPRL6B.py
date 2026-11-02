def listar_produtos(produtos):
    """Mostra na tela todos os produtos que estão na lista recebida.

    Cada produto é um dicionário com quatro informações: identificador (id),
    nome, preço e quantidade disponível em estoque. A função apenas exibe os
    dados; ela não altera a lista.
    """
    # Uma lista vazia é considerada falsa em uma condição. Por isso, "not
    # produtos" verifica se ainda não há nenhum produto para exibir.
    if not produtos:
        print("\nNenhum produto cadastrado.")
        # Encerra esta função aqui. Sem o return, o programa também tentaria
        # percorrer a lista vazia mais abaixo.
        return

    print("\n--- Produtos cadastrados ---")
    # O for visita um produto de cada vez. Em cada repetição, "produto"
    # representa um dos dicionários guardados na lista.
    for produto in produtos:
        print(
            # As chaves entre colchetes acessam os valores do dicionário.
            # :.2f formata o preço com exatamente duas casas decimais.
            f"ID: {produto['id']} | {produto['nome']} | "
            f"R$ {produto['preco']:.2f} | Estoque: {produto['estoque']}"
        )


def cadastrar_produto(produtos, proximo_id):
    """Pede os dados de um produto, valida-os e adiciona o produto à lista.

    Recebe a lista compartilhada de produtos e o próximo identificador
    disponível. Devolve o próximo identificador para que a função principal
    possa usá-lo no cadastro seguinte.
    """
    # strip() remove espaços extras no início e no fim do texto digitado.
    nome = input("Nome do produto: ").strip()
    if not nome:
        print("O nome do produto não pode ficar vazio.")
        # Como nada foi cadastrado, o identificador continua o mesmo.
        return proximo_id

    try:
        # float converte o preço para número decimal. replace permite digitar
        # o separador decimal brasileiro (vírgula) ou o ponto.
        preco = float(input("Preço: R$ ").replace(",", "."))
        # O estoque é um número inteiro, então usamos int para converter.
        estoque = int(input("Quantidade em estoque: "))
    except ValueError:
        # float ou int geram ValueError se o texto digitado não for numérico.
        # O except evita que esse erro interrompa todo o programa.
        print("Preço ou quantidade inválidos.")
        return proximo_id

    # Um preço deve ser positivo; a quantidade pode ser zero, mas não negativa.
    if preco <= 0 or estoque < 0:
        print("O preço deve ser maior que zero e o estoque não pode ser negativo.")
        return proximo_id

    # append adiciona um novo elemento ao final da lista. O produto é guardado
    # como um dicionário, associando cada informação a uma chave.
    produtos.append(
        {
            "id": proximo_id,
            "nome": nome,
            "preco": preco,
            "estoque": estoque,
        }
    )
    print(f"Produto '{nome}' cadastrado com sucesso (ID {proximo_id}).")
    # O cadastro deu certo: o próximo produto receberá o identificador seguinte.
    return proximo_id + 1


def comprar_produto(produtos):
    """Registra uma compra e reduz o estoque, se houver unidades suficientes."""
    # Exibe os IDs disponíveis para ajudar a pessoa a escolher o produto.
    listar_produtos(produtos)
    if not produtos:
        return

    try:
        # O usuário seleciona o produto por seu ID e informa quantas unidades
        # quer comprar. Ambos devem ser números inteiros.
        produto_id = int(input("\nID do produto que deseja comprar: "))
        quantidade = int(input("Quantidade: "))
    except ValueError:
        print("ID ou quantidade inválidos.")
        return

    # next procura o primeiro item que atende à condição. A expressão
    # "item['id'] == produto_id" compara o ID do item com o digitado.
    # Se nenhum item corresponder, o valor padrão None será devolvido.
    produto = next((item for item in produtos if item["id"] == produto_id), None)
    if produto is None:
        print("Produto não encontrado.")
        return

    # Bloqueia compras de zero ou de quantidades negativas.
    if quantidade <= 0:
        print("A quantidade deve ser maior que zero.")
        return

    # Não permite vender mais unidades do que as disponíveis.
    if quantidade > produto["estoque"]:
        print(f"Estoque insuficiente. Disponível: {produto['estoque']}.")
        return

    # A compra é válida. Atualizamos o próprio dicionário do produto; como ele
    # está dentro da lista, a alteração também fica refletida na lista.
    produto["estoque"] -= quantidade
    # Calcula o valor total multiplicando o preço pela quantidade comprada.
    total = produto["preco"] * quantidade
    print(f"Compra realizada: {quantidade} x {produto['nome']} = R$ {total:.2f}")


def deletar_produto(produtos):
    """Remove da lista o produto selecionado pelo seu identificador."""
    listar_produtos(produtos)
    if not produtos:
        return

    try:
        # O ID é inteiro, por isso o texto digitado precisa ser convertido.
        produto_id = int(input("\nID do produto que deseja deletar: "))
    except ValueError:
        print("ID inválido.")
        return

    # Procura na lista um produto com o ID solicitado.
    produto = next((item for item in produtos if item["id"] == produto_id), None)
    if produto is None:
        print("Produto não encontrado.")
        return

    # remove exclui da lista exatamente o dicionário encontrado.
    produtos.remove(produto)
    print(f"Produto '{produto['nome']}' deletado com sucesso.")


def main():
    """Prepara os dados e mantém o menu funcionando até a opção de saída."""
    # A lista começa vazia. Ela guarda os produtos enquanto o programa está
    # aberto; ao encerrar, os dados não são gravados em arquivo.
    produtos = []
    # O primeiro produto receberá ID 1. Cada cadastro válido aumenta esse valor.
    proximo_id = 1

    # while True repete o menu indefinidamente. A opção "0" encerra o laço
    # com break.
    while True:
        print(
            "\n=== Sistema de Produtos ==="
            "\n1. Listar produtos"
            "\n2. Cadastrar produto"
            "\n3. Comprar produto"
            "\n4. Deletar produto"
            "\n0. Sair"
        )
        # strip remove espaços extras antes de comparar com as opções do menu.
        opcao = input("Escolha uma opção: ").strip()

        # Cada opção chama a função responsável por aquela tarefa.
        if opcao == "1":
            listar_produtos(produtos)
        elif opcao == "2":
            # A função devolve o ID atualizado; guardamos o resultado para o
            # próximo cadastro não repetir o identificador.
            proximo_id = cadastrar_produto(produtos, proximo_id)
        elif opcao == "3":
            comprar_produto(produtos)
        elif opcao == "4":
            deletar_produto(produtos)
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Escolha uma opção do menu.")


# Esta condição é verdadeira quando este arquivo é executado diretamente.
# Ela permite que main() inicie o sistema sem iniciá-lo automaticamente caso
# este arquivo seja importado por outro programa.
if __name__ == "__main__":
    main()
