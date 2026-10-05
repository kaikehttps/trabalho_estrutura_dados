# Arquivo: desafio2.py
# Conteudo: DESAFIO 2 - tokenizacao de expressoes convencionais
#           (infixas) e conversao para a forma POS-FIXA, usando
#           uma pilha de operadores (algoritmo Shunting Yard).
# ============================================================
"""Conversao de expressao convencional (infixa) para pos-fixa.

Resumo do algoritmo (percorrendo os tokens da esquerda para a direita):

    numero    -> vai direto para a SAIDA;
    "("       -> empilha (marca o inicio de um trecho entre parenteses);
    ")"       -> desempilha para a saida ate encontrar "(" e descarta o "(";
    operador  -> antes de empilhar, desempilha para a saida todos os
                 operadores do topo que devem ser aplicados antes dele;
    fim       -> desempilha o que sobrou na pilha para a saida.

Nenhuma funcao deste arquivo imprime nada.
"""

from desafio1 import ErroExpressao, eh_numero
from pilha import Pilha

# Operadores aceitos (tupla, pelo mesmo motivo explicado em desafio1.py).
OPERADORES = ("+", "-", "*", "/", "^")
PARENTESES = ("(", ")")
DIGITOS = "0123456789"

# Tabela de precedencia: numero maior = aplicado primeiro.
PRECEDENCIA = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}

# Tabela de associatividade: define o que fazer quando a precedencia empata.
ASSOCIATIVIDADE = {
    "+": "esquerda",
    "-": "esquerda",
    "*": "esquerda",
    "/": "esquerda",
    "^": "direita",
}

# Larguras fixas exigidas pelo enunciado para o rastreamento.
LARGURA_TOKEN = 5
LARGURA_PILHA = 11


def tokenizar(expressao):
    """Varre a string caractere a caractere e devolve a lista de tokens.

    Reconhece numeros com varios digitos e decimais, operadores e
    parenteses. Espacos sao ignorados, entao "3+42*(7-1)" e
    "3 + 42 * ( 7 - 1 )" produzem exatamente a mesma lista:

        ['3', '+', '42', '*', '(', '7', '-', '1', ')']

    Nao usamos split(), porque na expressao convencional os tokens podem
    estar completamente grudados.
    """
    tokens = []
    i = 0
    total = len(expressao)

    while i < total:
        caractere = expressao[i]

        if caractere.isspace():
            # Espacos apenas separam; nao geram token.
            i += 1

        elif caractere in DIGITOS or caractere == ".":
            # Comeco de um numero: avanca enquanto houver digito ou ponto,
            # juntando tudo em um unico token.
            inicio = i
            while i < total and (expressao[i] in DIGITOS or expressao[i] == "."):
                i += 1
            numero = expressao[inicio:i]
            if not eh_numero(numero):
                # Ex.: "3.5.7" ou um ponto solto.
                raise ErroExpressao("erro: caractere invalido")
            tokens.append(numero)

        elif caractere in OPERADORES or caractere in PARENTESES:
            tokens.append(caractere)
            i += 1

        else:
            # Qualquer outro simbolo (letras, "$", "#", ...) e invalido.
            raise ErroExpressao("erro: caractere invalido")

    return tokens


def validar(tokens):
    """Confere se a sequencia de tokens forma uma expressao bem construida.

    Percorre os tokens com uma "expectativa": em cada posicao sabemos se o
    proximo token deve ser um OPERANDO (numero ou "(") ou um OPERADOR
    (ou ")"). Tambem conta os parenteses abertos.

    Isso rejeita, com mensagem clara e sem quebrar o programa:
        ""          -> expressao vazia
        "3+*4"      -> dois operadores seguidos
        "3+"        -> termina em operador
        "-3", "+5"  -> sinal unario (nao exigido pelo trabalho)
        "2(3+1)"    -> multiplicacao implicita (nao exigida pelo trabalho)
        "3 4"       -> dois numeros seguidos
        "()"        -> parenteses sem conteudo
        "3+4)"      -> parentese fechado sem abertura
        "(3+4"      -> parentese aberto sem fechamento
    """
    if not tokens:
        raise ErroExpressao("erro: expressao malformada")

    espera_operando = True   # a expressao precisa COMECAR com um operando
    abertos = 0              # quantos "(" ainda nao foram fechados

    for token in tokens:
        if eh_numero(token):
            if not espera_operando:
                raise ErroExpressao("erro: expressao malformada")
            espera_operando = False

        elif token == "(":
            if not espera_operando:
                raise ErroExpressao("erro: expressao malformada")
            abertos += 1

        elif token == ")":
            if espera_operando:
                raise ErroExpressao("erro: expressao malformada")
            if abertos == 0:
                raise ErroExpressao("erro: parentese fechado sem abertura")
            abertos -= 1

        else:   # operador
            if espera_operando:
                raise ErroExpressao("erro: expressao malformada")
            espera_operando = True

    if espera_operando:
        # Terminou esperando um operando: a expressao acabou em operador.
        raise ErroExpressao("erro: expressao malformada")
    if abertos > 0:
        raise ErroExpressao("erro: parentese aberto sem fechamento")


def deve_desempilhar(topo, operador):
    """Decide se o operador que esta no TOPO sai antes de empilhar o novo.

    Regra:
      - "(" nunca sai aqui: ele so e removido pelo ")" correspondente;
      - sai quem tem precedencia MAIOR que a do operador novo;
      - em caso de EMPATE, so sai se o operador novo for associativo
        a ESQUERDA.

    E o empate que preserva a associatividade a direita de "^":
      * "10-3-2": ao chegar o 2o "-", ha empate e "-" e associativo a
        esquerda -> o "-" do topo SAI -> resultado "10 3 - 2 -" = (10-3)-2.
      * "2^3^2": ao chegar o 2o "^", ha empate e "^" e associativo a
        direita -> o "^" do topo FICA e o novo e empilhado por cima. Como
        a pilha e LIFO, o "^" de cima sai primeiro no final, gerando
        "2 3 2 ^ ^" = 2^(3^2) = 512, e nao (2^3)^2 = 64.
    """
    if topo == "(":
        return False
    if PRECEDENCIA[topo] > PRECEDENCIA[operador]:
        return True
    if PRECEDENCIA[topo] == PRECEDENCIA[operador]:
        return ASSOCIATIVIDADE[operador] == "esquerda"
    return False


def registrar_passo(rastreio, token, pilha, saida):
    """Guarda uma COPIA do estado atual no rastreamento (se ele foi pedido).

    pilha.conteudo() ja devolve uma lista nova (base -> topo) e list(saida)
    copia a saida, entao os registros antigos nao mudam depois.
    """
    if rastreio is None:
        return
    rastreio.append({
        "token": token,
        "pilha": pilha.conteudo(),
        "saida": list(saida),
    })


def converter(expressao, rastreio=None):
    """Recebe a expressao convencional (string) e devolve a pos-fixa (string).

    expressao -- ex.: "3+4*(2-1)"  ou  "3 + 4 * ( 2 - 1 )"
    rastreio  -- lista OPCIONAL que recebe um dicionario por token:
                    {"token": "+", "pilha": ["+"], "saida": ["3"]}
                 O ultimo registro usa o token literal "(fim)" e mostra o
                 esvaziamento final da pilha.

    Retorno: string pos-fixa com os tokens separados por espacos,
             ex.: "3 4 2 1 - * +"
    """
    tokens = tokenizar(expressao)   # pode levantar "erro: caractere invalido"
    validar(tokens)                 # pode levantar os erros de estrutura

    pilha = Pilha()   # pilha SO de operadores e de "("
    saida = []        # lista com os tokens ja definidos da expressao pos-fixa

    for token in tokens:
        if eh_numero(token):
            # Numero nao espera nada: vai direto para a saida.
            saida.append(token)

        elif token == "(":
            pilha.empilhar(token)

        elif token == ")":
            # Fecha o trecho: tudo que estiver acima do "(" sai para a saida.
            while not pilha.vazia() and pilha.topo() != "(":
                saida.append(pilha.desempilhar())
            if pilha.vazia():
                raise ErroExpressao("erro: parentese fechado sem abertura")
            pilha.desempilhar()   # descarta o "(" (parenteses nao vao p/ saida)

        else:   # operador
            while not pilha.vazia() and deve_desempilhar(pilha.topo(), token):
                saida.append(pilha.desempilhar())
            pilha.empilhar(token)

        registrar_passo(rastreio, token, pilha, saida)

    # Fim dos tokens: esvazia a pilha para a saida.
    while not pilha.vazia():
        operador = pilha.desempilhar()
        if operador == "(":
            raise ErroExpressao("erro: parentese aberto sem fechamento")
        saida.append(operador)

    registrar_passo(rastreio, "(fim)", pilha, saida)

    return " ".join(saida)


# ------------------------------------------------------------
# Formatacao do rastreamento (monta strings, NAO imprime)
# ------------------------------------------------------------

def montar_linha_conversao(token, pilha_texto, saida_texto):
    """Monta a linha: token (largura 5) | pilha (largura 11) | saida."""
    return f"{token:<{LARGURA_TOKEN}} | {pilha_texto:<{LARGURA_PILHA}} | {saida_texto}"


# Cabecalho da tabela do Desafio 2: "token | pilha       | saida"
CABECALHO_CONVERSAO = montar_linha_conversao("token", "pilha", "saida")


def formatar_linha_conversao(registro):
    """Transforma um registro do rastreio na linha de texto correspondente."""
    pilha_texto = " ".join(registro["pilha"])
    if pilha_texto == "":
        pilha_texto = "-"
    saida_texto = " ".join(registro["saida"])
    if saida_texto == "":
        saida_texto = "-"
    return montar_linha_conversao(registro["token"], pilha_texto, saida_texto)


if __name__ == "__main__":
    # Execucao isolada do Desafio 2: le expressoes CONVENCIONAIS e mostra
    # a tokenizacao, o rastreamento da conversao e a expressao pos-fixa.
    print("=" * 52)
    print("DESAFIO 2 - conversao de infixa para pos-fixa")
    print("Ex.: 3+4*(2-1)   ou   2^3^2")
    print("Digite uma linha vazia para sair.")
    print("=" * 52)

    while True:
        try:
            entrada = input("\ninfixa> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nencerrando.")
            break
        if entrada == "":
            print("encerrando.")
            break

        registros = []
        erro = None
        posfixa = None
        try:
            print("tokens:", tokenizar(entrada))
            posfixa = converter(entrada, registros)
        except ErroExpressao as problema:
            erro = str(problema)

        print(CABECALHO_CONVERSAO)
        for registro in registros:
            print(formatar_linha_conversao(registro))
        if erro is not None:
            print(erro)
        else:
            print("posfixa:", posfixa)
