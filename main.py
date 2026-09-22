# ============================================================
# Trabalho: Processamento de Expressoes Matematicas
# Disciplina: Estruturas de Dados
#
# Integrantes:
#   Nome: ______________________________  Matricula: ______________
#   Nome: ______________________________  Matricula: ______________
#   Nome: ______________________________  Matricula: ______________
#   Nome: ______________________________  Matricula: ______________
# ============================================================
#
# Arquivo: main.py
# Conteudo: PROGRAMA PRINCIPAL. Le as expressoes, chama as funcoes
#           dos desafios 1 e 2 e imprime os rastreamentos.
#           Toda a impressao do trabalho esta concentrada aqui.
# ============================================================
"""Programa principal do trabalho.

Menu:
    1 - Desafio 1: avaliar uma expressao POS-FIXA ("3 4 +")
    2 - Desafios 2 e 3: converter uma expressao CONVENCIONAL e avaliar
    3 - Rodar a verificacao com os exemplos do enunciado
    0 - Sair

Regra de organizacao: desafio1.py e desafio2.py apenas calculam e
devolvem valores; quem imprime e este arquivo.
"""

from desafio1 import (
    CABECALHO_AVALIACAO,
    ErroExpressao,
    avaliar,
    fmt,
    formatar_linha_avaliacao,
)
from desafio2 import (
    CABECALHO_CONVERSAO,
    converter,
    formatar_linha_conversao,
    tokenizar,
)


# ------------------------------------------------------------
# Leitura do teclado
# ------------------------------------------------------------

# Caractere invisivel (BOM) que alguns terminais, como o PowerShell,
# colocam no inicio quando a entrada vem de um arquivo redirecionado.
# Se ele nao for removido, a primeira linha lida vem "suja".
MARCA_INVISIVEL = "\ufeff"


def ler_linha(mensagem):
    """Le uma linha do teclado, ja limpa de espacos e da marca invisivel."""
    return input(mensagem).strip().lstrip(MARCA_INVISIVEL).strip()


# ------------------------------------------------------------
# Impressao dos rastreamentos
# ------------------------------------------------------------

def imprimir_avaliacao(posfixa):
    """Imprime o rastreamento da avaliacao pos-fixa e o resultado.

    Devolve o resultado (float) ou None se houve erro.
    """
    registros = []
    erro = None
    resultado = None
    try:
        resultado = avaliar(posfixa, registros)
    except ErroExpressao as problema:
        # A mensagem ja vem pronta ("erro: ...").
        erro = str(problema)

    # O rastreamento e impresso mesmo quando ocorre erro: assim da para ver
    # ate onde o processamento chegou antes do problema.
    print(CABECALHO_AVALIACAO)
    for registro in registros:
        print(formatar_linha_avaliacao(registro))

    if erro is not None:
        print(erro)
        return None
    print("resultado:", fmt(resultado))
    return resultado


def imprimir_conversao(infixa):
    """Imprime o rastreamento da conversao e a expressao pos-fixa.

    Devolve a string pos-fixa ou None se houve erro.
    """
    registros = []
    erro = None
    posfixa = None
    try:
        posfixa = converter(infixa, registros)
    except ErroExpressao as problema:
        erro = str(problema)

    print(CABECALHO_CONVERSAO)
    for registro in registros:
        print(formatar_linha_conversao(registro))

    if erro is not None:
        print(erro)
        return None
    print("posfixa:", posfixa)
    return posfixa


def processar_expressao_convencional(infixa):
    """Etapa 1: converter (com rastreamento). Etapa 2: avaliar (idem)."""
    print("\n--- conversao para pos-fixa ---")
    posfixa = imprimir_conversao(infixa)
    if posfixa is None:
        # Erro na conversao: nao ha o que avaliar.
        return
    print("\n--- avaliacao da pos-fixa ---")
    imprimir_avaliacao(posfixa)


# ------------------------------------------------------------
# Modos de uso (opcoes do menu)
# ------------------------------------------------------------

def modo_posfixa():
    """Le e avalia varias expressoes pos-fixas."""
    print("\n[Desafio 1] Digite expressoes POS-FIXAS (tokens separados por espacos).")
    print("Exemplo: 5 1 2 + 4 * + 3 -")
    print("Linha vazia volta ao menu.")
    while True:
        try:
            entrada = ler_linha("\nposfixa> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if entrada == "":
            return
        imprimir_avaliacao(entrada)


def modo_convencional():
    """Le varias expressoes convencionais, converte e avalia."""
    print("\n[Desafios 2 e 3] Digite expressoes CONVENCIONAIS (com ou sem espacos).")
    print("Exemplo: 3+42*(7-1)")
    print("Linha vazia volta ao menu.")
    while True:
        try:
            entrada = ler_linha("\ninfixa> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if entrada == "":
            return
        print("tokens:", tokenizar_seguro(entrada))
        processar_expressao_convencional(entrada)


def tokenizar_seguro(expressao):
    """Mostra os tokens; se houver caractere invalido, devolve a mensagem.

    A tokenizacao tambem e feita dentro de converter(); aqui ela aparece
    separada so para a apresentacao, mostrando o resultado do Desafio 2.
    """
    try:
        return tokenizar(expressao)
    except ErroExpressao as problema:
        return str(problema)


# ------------------------------------------------------------
# Verificacao com os exemplos do enunciado
# ------------------------------------------------------------

# (expressao pos-fixa, resultado esperado)
TESTES_POSFIXA = [
    ("3 4 +", 7),
    ("3 4 2 * +", 11),
    ("3 4 + 2 *", 14),
    ("10 3 -", 7),
    ("20 4 /", 5),
    ("5 1 2 + 4 * + 3 -", 14),
    ("2.5 1.5 +", 4),
    ("100 25 /", 4),
    ("2 3 2 ^ ^", 512),
    ("2 3 ^ 2 ^", 64),
]

# (expressao convencional, pos-fixa esperada, resultado esperado)
TESTES_INFIXA = [
    ("3+4*2", "3 4 2 * +", 11),
    ("(3+4)*2", "3 4 + 2 *", 14),
    ("1+2*3-4/2", "1 2 3 * + 4 2 / -", 5),
    ("3+4*(2-1)", "3 4 2 1 - * +", 7),
    ("10-3-2", "10 3 - 2 -", 5),
    ("2^3^2", "2 3 2 ^ ^", 512),
    ("(2^3)^2", "2 3 ^ 2 ^", 64),
    ("3+42*(7-1)", "3 42 7 1 - * +", 255),
    ("2.5*4", "2.5 4 *", 10),
    ("0.5+0.25", "0.5 0.25 +", 0.75),
    ("3 + 4 * 2", "3 4 2 * +", 11),
]

# (expressao, tipo, mensagem esperada)
TESTES_ERRO = [
    ("3 + * 4", "posfixa", "erro: operandos insuficientes"),
    ("3 4 5 +", "posfixa", "erro: expressao malformada"),
    ("8 0 /", "posfixa", "erro: divisao por zero"),
    ("+", "posfixa", "erro: operandos insuficientes"),
    ("", "posfixa", "erro: expressao malformada"),
    ("3 4 a +", "posfixa", "erro: caractere invalido"),
    ("3+4)", "infixa", "erro: parentese fechado sem abertura"),
    ("(3+4", "infixa", "erro: parentese aberto sem fechamento"),
    ("3$4", "infixa", "erro: caractere invalido"),
    ("", "infixa", "erro: expressao malformada"),
    ("3+*4", "infixa", "erro: expressao malformada"),
    ("3+", "infixa", "erro: expressao malformada"),
    ("-3+4", "infixa", "erro: expressao malformada"),
    ("2(3+1)", "infixa", "erro: expressao malformada"),
    ("()", "infixa", "erro: expressao malformada"),
    ("8/0", "infixa", "erro: divisao por zero"),
]


def executar_verificacao():
    """Roda os exemplos do enunciado e imprime OK ou FALHOU em cada um."""
    total = 0
    falhas = 0

    print("\n=== Verificacao 1: avaliacao pos-fixa ===")
    for posfixa, esperado in TESTES_POSFIXA:
        total += 1
        try:
            obtido = fmt(avaliar(posfixa))
        except ErroExpressao as problema:
            obtido = str(problema)
        situacao = "OK" if obtido == fmt(esperado) else "FALHOU"
        if situacao == "FALHOU":
            falhas += 1
        print(f"[{situacao:6}] {posfixa:22} -> {obtido:24} (esperado {fmt(esperado)})")

    print("\n=== Verificacao 2: conversao e avaliacao ===")
    for infixa, posfixa_esperada, esperado in TESTES_INFIXA:
        total += 1
        try:
            posfixa_obtida = converter(infixa)
            resultado = fmt(avaliar(posfixa_obtida))
        except ErroExpressao as problema:
            posfixa_obtida = str(problema)
            resultado = "-"
        certo = (posfixa_obtida == posfixa_esperada and resultado == fmt(esperado))
        situacao = "OK" if certo else "FALHOU"
        if not certo:
            falhas += 1
        print(f"[{situacao:6}] {infixa:14} -> {posfixa_obtida:24} = {resultado:8}"
              f" (esperado {posfixa_esperada} = {fmt(esperado)})")

    print("\n=== Verificacao 3: mensagens de erro ===")
    for expressao, tipo, mensagem in TESTES_ERRO:
        total += 1
        try:
            if tipo == "posfixa":
                obtido = "resultado: " + fmt(avaliar(expressao))
            else:
                obtido = "resultado: " + fmt(avaliar(converter(expressao)))
        except ErroExpressao as problema:
            obtido = str(problema)
        situacao = "OK" if obtido == mensagem else "FALHOU"
        if situacao == "FALHOU":
            falhas += 1
        rotulo = f"({tipo}) {expressao!r}"
        print(f"[{situacao:6}] {rotulo:24} -> {obtido:38} (esperado {mensagem})")

    print(f"\nTotal: {total} casos | falhas: {falhas}")


# ------------------------------------------------------------
# Menu principal
# ------------------------------------------------------------

def mostrar_menu():
    print("\n" + "=" * 60)
    print("PROCESSAMENTO DE EXPRESSOES MATEMATICAS")
    print("=" * 60)
    print("1 - Desafio 1: avaliar expressao POS-FIXA")
    print("2 - Desafios 2 e 3: converter expressao CONVENCIONAL e avaliar")
    print("3 - Rodar a verificacao (exemplos do enunciado)")
    print("0 - Sair")


def main():
    while True:
        mostrar_menu()
        try:
            opcao = ler_linha("opcao> ")
        except (EOFError, KeyboardInterrupt):
            print("\nate logo!")
            return

        if opcao == "1":
            modo_posfixa()
        elif opcao == "2":
            modo_convencional()
        elif opcao == "3":
            executar_verificacao()
        elif opcao == "0" or opcao == "":
            print("ate logo!")
            return
        else:
            print("opcao invalida.")


if __name__ == "__main__":
    main()
