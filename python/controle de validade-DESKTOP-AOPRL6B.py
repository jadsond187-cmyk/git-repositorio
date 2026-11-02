# json é a biblioteca padrão que converte dados Python para o formato JSON e vice-versa.
import json
# date representa somente uma data; datetime também consegue interpretar textos de data;
# timedelta representa um intervalo de tempo, usado para calcular os próximos 30 dias.
from datetime import date, datetime, timedelta
# Path ajuda a montar e manipular caminhos de arquivos sem concatenar textos manualmente.
from pathlib import Path
# TypedDict permite descrever o formato de um dicionário para facilitar a leitura do código.
from typing import TypedDict


# TypedDict descreve quais chaves e tipos cada produto deve ter.
# Por exemplo, "id" guarda um inteiro e "nome" guarda um texto.
class Produto(TypedDict):
    id: int  # Número único usado para escolher o produto nos menus.
    nome: str  # Nome do produto, por exemplo, "Leite".
    categoria: str  # Grupo ao qual pertence, como "Laticínios".
    lote: str  # Identificação do lote fornecida pelo fabricante.
    validade: str  # Data no padrão ano-mês-dia, que também será usada no JSON.
    quantidade: int  # Quantas unidades do produto existem no estoque.
    observacoes: str  # Campo livre para informações adicionais.


# Path monta o caminho do arquivo JSON na mesma pasta deste programa,
# mesmo que ele seja executado a partir de outra pasta.
# __file__ contém o caminho deste programa; with_name troca apenas o nome do arquivo.
# Assim, o JSON será criado na mesma pasta do script, independentemente da pasta atual.
ARQUIVO_DADOS = Path(__file__).with_name("produtos_validade.json")
# Produtos que vencem dentro deste prazo recebem um alerta.
DIAS_ALERTA = 30


def carregar_produtos(caminho: Path = ARQUIVO_DADOS) -> list[Produto]:
    """Lê os produtos do JSON e verifica se os dados têm o formato esperado."""
    # caminho é um parâmetro, então podemos escolher outro arquivo ao testar a função.
    # O valor padrão é o arquivo principal configurado acima.
    # Na primeira execução ainda não existe arquivo; nesse caso começamos
    # com uma lista vazia, que será preenchida pelos novos cadastros.
    if not caminho.exists():
        return []  # Devolve uma lista vazia e encerra a função neste caso.

    # with fecha o arquivo automaticamente depois da leitura.
    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)  # Interpreta o JSON e cria objetos Python.

    # O arquivo precisa guardar uma lista, pois cada elemento representa
    # um produto. Um objeto JSON isolado não serve para este formato.
    if not isinstance(dados, list):
        raise ValueError("O arquivo JSON deve conter uma lista de produtos.")

    produtos: list[Produto] = []  # Lista onde serão colocados os produtos validados.
    # Tupla com os nomes dos campos que obrigatoriamente precisam conter textos.
    campos_texto = ("nome", "categoria", "lote", "validade", "observacoes")
    # enumerate também fornece a posição do item, útil para explicar erros.
    for indice, item in enumerate(dados, start=1):
        # Cada elemento da lista JSON deve ser um dicionário de produto.
        if not isinstance(item, dict):
            raise ValueError(f"O produto {indice} no JSON não é um objeto.")
        # get permite conferir se cada campo existe antes de usar seu valor.
        # A condição usa or: basta um teste falhar para os dados serem rejeitados.
        if not isinstance(item.get("id"), int) or not all(
            # all retorna True somente se todos os campos da tupla forem textos.
            isinstance(item.get(campo), str) for campo in campos_texto
        ):
            raise ValueError(f"Os dados do produto {indice} no JSON são inválidos.")
        # A quantidade precisa ser inteira e não pode ser negativa.
        if not isinstance(item.get("quantidade"), int) or item["quantidade"] < 0:
            raise ValueError(f"A quantidade do produto {indice} no JSON é inválida.")
        try:
            # A data no JSON é armazenada no formato ISO: ano-mês-dia.
            datetime.strptime(item["validade"], "%Y-%m-%d")  # Tenta interpretar a data.
        except ValueError as erro:
            # A exceção informa qual produto tem uma data que não pode ser lida.
            raise ValueError(
                f"A data de validade do produto {indice} no JSON é inválida."
            ) from erro

        # Criamos um registro com os campos permitidos e o adicionamos à lista.
        produtos.append(  # Adiciona o produto validado ao final da lista.
            Produto(
                id=item["id"],  # Copia o ID do dicionário lido do arquivo.
                nome=item["nome"],  # Copia o nome do produto.
                categoria=item["categoria"],  # Copia a categoria.
                lote=item["lote"],  # Copia o lote.
                validade=item["validade"],  # Copia a validade no formato ISO.
                quantidade=item["quantidade"],  # Copia a quantidade.
                observacoes=item["observacoes"],  # Copia as observações.
            )
        )
    return produtos  # Entrega ao programa a lista completa que foi carregada.


def salvar_produtos(produtos: list[Produto], caminho: Path = ARQUIVO_DADOS) -> None:
    """Converte a lista de produtos para JSON e grava no disco."""
    # O modo "w" cria o arquivo ou substitui seu conteúdo pelo estado mais recente.
    with caminho.open("w", encoding="utf-8") as arquivo:
        # ensure_ascii=False mantém acentos legíveis; indent organiza o arquivo.
        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)  # Escreve a lista em JSON.
        # A quebra de linha final deixa o arquivo mais fácil de ler em editores.
        arquivo.write("\n")  # Escreve uma quebra de linha no fim do arquivo.


def obter_data_validade(produto: Produto) -> date:
    # Converte o texto salvo no produto para um objeto de data comparável.
    # A chave "validade" acessa o valor correspondente dentro do dicionário.
    texto_data = produto["validade"]
    # strptime interpreta o padrão ISO; date() remove a parte de hora, que não usamos.
    return datetime.strptime(texto_data, "%Y-%m-%d").date()


def obter_status(produto: Produto, hoje: date | None = None) -> str:
    # O parâmetro hoje facilita testar a função com uma data controlada.
    # Se hoje não foi informado, usamos a data verdadeira do computador.
    hoje = hoje or date.today()
    # A subtração entre datas produz um intervalo; days é a quantidade de dias.
    dias = (obter_data_validade(produto) - hoje).days
    # Número negativo significa que a validade ocorreu antes da data de hoje.
    if dias < 0:
        return "vencido"
    # Zero indica que as duas datas são iguais.
    if dias == 0:
        return "vence hoje"
    # Um número positivo até o limite definido gera uma mensagem de alerta.
    if dias <= DIAS_ALERTA:
        return f"vence em {dias} dia(s)"
    # Se nenhuma condição anterior ocorreu, ainda falta mais de 30 dias.
    return "válido"


def formatar_data(produto: Produto) -> str:
    # A data é guardada em ISO, mas exibida no formato comum no Brasil.
    data = obter_data_validade(produto)  # Obtém a data como objeto date.
    return data.strftime("%d/%m/%Y")  # Converte date para dia/mês/ano.


def exibir_produto(produto: Produto) -> None:
    # Cada print mostra uma parte do registro para facilitar a leitura no menu.
    print(
        # As chaves { } dentro da f-string são substituídas pelos valores do produto.
        # O operador or exibe "-" quando o campo do lote está vazio.
        f"ID: {produto['id']} | {produto['nome']} | "
        f"Categoria: {produto['categoria']} | Lote: {produto['lote'] or '-'}"
    )
    print(
        # Chamamos funções para reutilizar a formatação da data e o cálculo do status.
        f"  Validade: {formatar_data(produto)} | "
        f"Quantidade: {produto['quantidade']} | Status: {obter_status(produto)}"
    )
    if produto["observacoes"]:  # Só mostra a linha se houver observação preenchida.
        print(f"  Observações: {produto['observacoes']}")  # Exibe o texto adicional.


def listar_produtos(produtos: list[Produto]) -> None:
    print("\n--- Produtos cadastrados ---")  # \n pula uma linha antes do título.
    if not produtos:
        print("Nenhum produto cadastrado.")
        return  # Não há itens para percorrer, então a função termina aqui.

    # sorted cria uma sequência ordenada sem alterar a lista original.
    # Primeiro compara a validade e depois o nome sem diferenciar maiúsculas.
    for produto in sorted(
        # A chave (validade, nome) ordena primeiro por validade e desempata pelo nome.
        produtos, key=lambda item: (item["validade"], item["nome"].casefold())
    ):
        exibir_produto(produto)  # Mostra cada item na ordem calculada por sorted().


def ler_data(prompt: str, data_atual: str | None = None) -> str:
    # prompt é a pergunta mostrada; data_atual é opcional e usada na edição.
    # O while repete a pergunta até receber uma data válida.
    while True:
        entrada = input(prompt).strip()  # input lê texto; strip remove espaços externos.
        # Na edição, Enter significa conservar a data que já estava cadastrada.
        if not entrada and data_atual is not None:
            return data_atual  # Devolve o valor antigo sem pedir outra data.
        try:
            # strptime valida o calendário (por exemplo, rejeita 31/02).
            # isoformat converte para o formato usado para salvar no JSON.
            return datetime.strptime(entrada, "%d/%m/%Y").date().isoformat()
        except ValueError:
            # Um texto inválido ou uma data impossível causa ValueError.
            # Em vez de fechar o programa, mostramos a mensagem e repetimos o while.
            print("Data inválida. Informe uma data existente no formato dd/mm/aaaa.")


def ler_quantidade(prompt: str, quantidade_atual: int | None = None) -> int:
    # O retorno int garante que a quantidade será armazenada como número inteiro.
    while True:
        entrada = input(prompt).strip()  # Lê a resposta e remove espaços extras.
        # Durante a edição, uma entrada vazia mantém a quantidade existente.
        if not entrada and quantidade_atual is not None:
            return quantidade_atual  # Sai sem alterar a quantidade antiga.
        try:
            quantidade = int(entrada)  # Tenta converter, por exemplo, "12" em 12.
            # Quantidade negativa não faz sentido para o estoque.
            if quantidade >= 0:
                return quantidade  # A quantidade válida é devolvida ao chamador.
        except ValueError:
            # int falha se a pessoa digitar letras ou um número decimal.
            pass
        # Também chegamos aqui se a conversão falhar ou o número for negativo.
        print("Informe um número inteiro igual ou maior que zero.")


def proximo_id(produtos: list[Produto]) -> int:
    # max encontra o maior ID atual; default=0 cobre uma lista ainda vazia.
    maior_id = max((produto["id"] for produto in produtos), default=0)
    # O próximo identificador é sempre um número acima do maior identificador atual.
    return maior_id + 1


def cadastrar_produto(produtos: list[Produto]) -> None:
    print("\n--- Cadastro de produto ---")  # Separa visualmente esta etapa no terminal.
    nome = input("Nome: ").strip()  # Lê o nome e remove espaços no começo e no fim.
    if not nome:
        print("O nome do produto não pode ficar vazio.")
        return  # Interrompe o cadastro para não criar produto sem nome.

    categoria = input("Categoria: ").strip()  # Categoria é texto e pode ficar vazia.
    lote = input("Lote (opcional): ").strip()  # O lote também pode não ser informado.
    # As funções de leitura verificam os formatos antes de devolver os valores.
    validade = ler_data("Data de validade (dd/mm/aaaa): ")
    quantidade = ler_quantidade("Quantidade em estoque: ")
    observacoes = input("Observações (opcional): ").strip()  # Texto livre opcional.
    # O dicionário guarda todos os campos do novo produto em um único registro.
    produtos.append(
        # Produto(...) cria um dicionário com as chaves descritas na classe TypedDict.
        Produto(
            id=proximo_id(produtos),  # Calcula um identificador que ainda não foi usado.
            nome=nome,
            categoria=categoria,
            lote=lote,
            validade=validade,
            quantidade=quantidade,
            observacoes=observacoes,
        )
    )
    print("Produto cadastrado.")  # Confirma que o novo item entrou na lista.


def localizar_por_id(produtos: list[Produto], produto_id: int) -> Produto | None:
    # next devolve o primeiro produto com esse ID; None significa "não achou".
    # A expressão entre parênteses percorre a lista e compara o ID de cada produto.
    return next((produto for produto in produtos if produto["id"] == produto_id), None)


def solicitar_id() -> int | None:
    try:
        # input sempre retorna texto; int transforma o ID em número.
        texto_id = input("ID do produto: ").strip()
        return int(texto_id)  # Se o texto não for um inteiro, o except trata o erro.
    except ValueError:
        print("ID inválido. Informe um número.")
        return None  # None informa ao chamador que não foi possível ler um ID.


def editar_produto(produtos: list[Produto]) -> None:
    produto_id = solicitar_id()  # Pede o ID e recebe um inteiro ou None.
    # Só procuramos o produto quando a conversão do ID foi bem-sucedida.
    produto = localizar_por_id(produtos, produto_id) if produto_id is not None else None
    if produto is None:
        print("Produto não encontrado.")
        return

    print("Pressione Enter para manter o valor atual.")
    # Os valores atuais entre colchetes ajudam a pessoa a saber o que está editando.
    # Enter deixa estes campos de texto inalterados, pois só atualizamos se não vazios.
    nome = input(f"Nome [{produto['nome']}]: ").strip()
    categoria = input(f"Categoria [{produto['categoria']}]: ").strip()
    lote = input(f"Lote [{produto['lote']}]: ").strip()
    # Para data e quantidade, as funções recebem o valor atual e retornam esse valor
    # quando a resposta é vazia.
    validade = ler_data(
        f"Validade [{formatar_data(produto)}] (dd/mm/aaaa): ", produto["validade"]
    )
    quantidade = ler_quantidade(
        f"Quantidade [{produto['quantidade']}]: ", produto["quantidade"]
    )
    observacoes = input(f"Observações [{produto['observacoes']}]: ").strip()

    # Em cada if, só substituímos o texto antigo quando um texto novo foi digitado.
    if nome:
        produto["nome"] = nome
    if categoria:
        produto["categoria"] = categoria
    if lote:
        produto["lote"] = lote
    if observacoes:
        produto["observacoes"] = observacoes
    # Estes campos usam funções próprias que já preservam o valor anterior
    # quando a pessoa apenas pressiona Enter.
    produto["validade"] = validade  # Atualiza para a data nova ou mantém a existente.
    produto["quantidade"] = quantidade  # Atualiza para a quantidade nova ou mantém.
    print("Produto atualizado.")  # Confirma a edição na tela.


def excluir_produto(produtos: list[Produto]) -> None:
    produto_id = solicitar_id()  # Recebe o ID como número ou None se não for válido.
    produto = localizar_por_id(produtos, produto_id) if produto_id is not None else None
    if produto is None:
        print("Produto não encontrado.")
        return

    # casefold converte a resposta para minúsculas para aceitar "S" e "s".
    confirmacao = input(f"Excluir '{produto['nome']}'? (s/n): ").strip().casefold()
    if confirmacao == "s":
        # remove tira da lista exatamente o dicionário selecionado.
        produtos.remove(produto)
        print("Produto excluído.")
    else:
        print("Exclusão cancelada.")


def buscar_produtos(produtos: list[Produto]) -> None:
    # Normalizamos o termo para facilitar a busca sem diferenciar maiúsculas.
    termo = input("Buscar por nome, categoria ou lote: ").strip().casefold()
    # A compreensão de lista filtra os produtos que contêm o termo digitado.
    # casefold permite encontrar "CAFÉ" ao buscar "café", sem diferenciar
    # letras maiúsculas e minúsculas.
    encontrados = [
        produto  # Cada produto encontrado será incluído na nova lista.
        for produto in produtos
        # Junta os três campos pesquisáveis em uma única frase.
        if termo
        in " ".join(
            (produto["nome"], produto["categoria"], produto["lote"])
        ).casefold()
    ]
    if not encontrados:
        print("Nenhum produto encontrado.")
        return
    for produto in encontrados:  # Percorre todos os resultados encontrados.
        exibir_produto(produto)  # Reutiliza a função que formata cada produto.


def filtrar_por_validade(produtos: list[Produto]) -> None:
    # Estas opções serão comparadas com a escolha digitada pela pessoa.
    print("\n1. Vencidos")
    print(f"2. Vencendo nos próximos {DIAS_ALERTA} dias")
    print("3. Dentro da validade (mais de 30 dias)")
    opcao = input("Escolha o filtro: ").strip()  # A opção é lida como texto.
    hoje = date.today()  # Guarda uma única data de referência para todo o filtro.
    # timedelta representa um intervalo de tempo; aqui calculamos o limite
    # dos próximos DIAS_ALERTA dias.
    limite = hoje + timedelta(days=DIAS_ALERTA)  # Data final do período de alerta.

    # Cada opção usa uma condição diferente para selecionar as datas.
    if opcao == "1":
        # A validade já passou quando sua data é menor que hoje.
        filtrados = [p for p in produtos if obter_data_validade(p) < hoje]
    elif opcao == "2":
        # Inclui a data de hoje e também o último dia do prazo de alerta.
        filtrados = [
            p for p in produtos if hoje <= obter_data_validade(p) <= limite
        ]
    elif opcao == "3":
        # O produto só entra aqui se vencer depois do limite de alerta.
        filtrados = [p for p in produtos if obter_data_validade(p) > limite]
    else:
        print("Opção inválida.")
        return

    listar_produtos(filtrados)  # Usa a listagem existente para exibir o resultado.


def mostrar_resumo(produtos: list[Produto]) -> None:
    hoje = date.today()  # Data usada para separar produtos por situação.
    limite = hoje + timedelta(days=DIAS_ALERTA)  # Último dia considerado "próximo".
    # sum conta quantas condições são verdadeiras (True vale como 1).
    # Cada expressão gera True para um produto que pertence a essa categoria.
    vencidos = sum(obter_data_validade(p) < hoje for p in produtos)
    vencendo = sum(hoje <= obter_data_validade(p) <= limite for p in produtos)
    validos = sum(obter_data_validade(p) > limite for p in produtos)
    # Soma o campo quantidade de todos os produtos, não apenas a quantidade de cadastros.
    unidades = sum(produto["quantidade"] for produto in produtos)

    # As próximas linhas imprimem o resultado calculado acima.
    print("\n--- Resumo do estoque ---")
    print(f"Produtos cadastrados: {len(produtos)}")  # len conta os registros da lista.
    print(f"Unidades em estoque: {unidades}")
    print(f"Vencidos: {vencidos}")
    print(f"Vencendo em até {DIAS_ALERTA} dias: {vencendo}")
    print(f"Com validade acima de {DIAS_ALERTA} dias: {validos}")


def main() -> None:
    # Se o arquivo não puder ser lido ou estiver malformado, mostramos o
    # erro para não iniciar com uma lista vazia e sobrescrever dados existentes.
    try:
        produtos = carregar_produtos()  # Recupera os dados salvos antes de abrir o menu.
    except (OSError, json.JSONDecodeError, ValueError) as erro:
        # OSError é erro de arquivo; JSONDecodeError indica JSON malformado;
        # ValueError é levantado pelas validações feitas em carregar_produtos().
        print(f"Não foi possível carregar os produtos: {erro}")
        return  # Evita prosseguir se não foi possível carregar os dados corretamente.

    # O menu continua aparecendo até a pessoa selecionar "0".
    while True:
        # Uma string entre parênteses pode ser dividida em várias linhas de código.
        # As strings que começam com \n inserem quebras de linha na tela.
        print(
            "\n===== Controle de validade ====="
            "\n1. Listar produtos"
            "\n2. Cadastrar produto"
            "\n3. Buscar produto"
            "\n4. Editar produto"
            "\n5. Excluir produto"
            "\n6. Filtrar por validade"
            "\n7. Ver resumo do estoque"
            "\n0. Salvar e sair"
        )
        opcao = input("Escolha uma opção: ").strip()  # Lê a opção e remove espaços.

        try:
            # Cada opção chama a função responsável por uma tarefa.
            if opcao == "1":
                listar_produtos(produtos)  # Opção 1: exibe todos os produtos.
            elif opcao == "2":
                cadastrar_produto(produtos)  # Opção 2: inclui um novo produto.
                # Salvamos logo após uma alteração para não depender somente
                # do encerramento normal do programa.
                salvar_produtos(produtos)  # Persiste a lista atual no JSON.
            elif opcao == "3":
                buscar_produtos(produtos)  # Opção 3: procura por nome, categoria ou lote.
            elif opcao == "4":
                editar_produto(produtos)  # Opção 4: altera os campos de um cadastro.
                salvar_produtos(produtos)  # Grava a alteração no arquivo.
            elif opcao == "5":
                excluir_produto(produtos)  # Opção 5: pede confirmação e remove o item.
                salvar_produtos(produtos)  # Grava a lista já sem o item removido.
            elif opcao == "6":
                filtrar_por_validade(produtos)  # Opção 6: separa por data de validade.
            elif opcao == "7":
                mostrar_resumo(produtos)  # Opção 7: mostra contagens e unidades.
            elif opcao == "0":
                salvar_produtos(produtos)  # Faz uma última gravação antes de sair.
                print("Dados salvos. Até logo!")  # Mensagem de encerramento.
                break  # Sai do while e termina o menu.
            else:
                # Qualquer texto que não seja uma opção conhecida chega aqui.
                print("Opção inválida. Escolha uma opção do menu.")
        except OSError as erro:
            # OSError pode ocorrer se o arquivo não puder ser escrito
            # (por exemplo, por falta de permissão ou espaço em disco).
            print(f"Erro ao salvar os dados em '{ARQUIVO_DADOS}': {erro}")
            return  # Interrompe o programa para não continuar após falha de gravação.


# Esta condição inicia o menu apenas quando o arquivo é executado diretamente.
# Assim, outras partes do programa podem importar as funções sem abrir o menu.
if __name__ == "__main__":
    main()
