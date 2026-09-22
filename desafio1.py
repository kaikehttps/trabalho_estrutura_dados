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
# Arquivo: desafio1.py
# Conteudo: DESAFIO 1 - avaliacao de expressoes POS-FIXAS
#           (notacao polonesa reversa) usando pilha encadeada.
# ============================================================
"""Avaliacao de expressoes pos-fixas com tokens separados por espacos.

Ideia do algoritmo:
    - numero   -> empilha;
    - operador -> desempilha DOIS operandos, calcula e empilha o resultado;
    - no final, a pilha deve ter exatamente UM valor: o resultado.

Cuidado essencial: o primeiro valor desempilhado e o operando da DIREITA
e o segundo e o da ESQUERDA. Se a ordem for trocada, "-", "/" e "^" dao
resultados errados (10 3 - viraria 3 - 10).

Nenhuma funcao deste arquivo imprime nada. A impressao fica no programa
principal (main.py) ou no bloco __main__ do final deste arquivo.
"""

from pilha import Pilha

# Operadores aceitos. Usamos uma TUPLA (e nao a string "+-*/^") porque em
# uma string o teste "in" acharia tambem pedacos: "+-" in "+-*/^" seria True.
OPERADORES = ("+", "-", "*", "/", "^")

DIGITOS = "0123456789"

# Larguras fixas exigidas pelo enunciado para o rastreamento.
LARGURA_TOKEN = 5


class ErroExpressao(Exception):
    """Erro previsto de expressao (mensagem ja pronta para o usuario).

    A mensagem guardada e exatamente a que deve ser impressa, por exemplo
    "erro: divisao por zero". O programa principal captura esse erro e
    imprime a mensagem no lugar do resultado, continuando a execucao.
    """


def fmt(v):
    """Formata um numero para impressao (funcao exigida pelo enunciado)."""
    return f"{v:g}"


def eh_numero(token):
    """True se o token for um numero valido: digitos e, no maximo, um ponto.

    Aceita: "3", "42", "3.5", "0.25"
    Rejeita: "", ".", "3.5.7", "-8" (sinal unario nao e aceito), "a"
    """
    if token == "" or token == ".":
        return False
    if token.count(".") > 1:
        return False
    for caractere in token:
        if caractere not in DIGITOS and caractere != ".":
            return False
    return True


def aplicar(operador, esquerdo, direito):
    """Calcula "esquerdo operador direito" e devolve o resultado."""
    if operador == "+":
        return esquerdo + direito
    if operador == "-":
        return esquerdo - direito
    if operador == "*":
        return esquerdo * direito
    if operador == "/":
        if direito == 0:
            raise ErroExpressao("erro: divisao por zero")
        return esquerdo / direito
    if operador == "^":
        # O simbolo "^" e a potencia; em Python o calculo usa "**".
        if esquerdo == 0 and direito < 0:
            # 0 ^ -1 equivale a 1/0.
            raise ErroExpressao("erro: divisao por zero")
        try:
            resultado = esquerdo ** direito
        except (OverflowError, ValueError):
            # Numero grande demais para um float: tratado como expressao
            # invalida para o programa nao quebrar com excecao nao tratada.
            raise ErroExpressao("erro: expressao malformada")
        if isinstance(resultado, complex):
            # Ex.: (-3) ^ 0.5 daria um numero complexo; fora do escopo.
            raise ErroExpressao("erro: expressao malformada")
        return resultado
    # Nunca deve acontecer: avaliar() so chama aplicar() com operador valido.
    raise ErroExpressao("erro: caractere invalido")


def avaliar(posfixa, rastreio=None):
    """Avalia a expressao pos-fixa e devolve o resultado (float).

    posfixa  -- string com os tokens separados por espacos, ex.: "3 4 +"
    rastreio -- lista OPCIONAL. Se for informada, recebe um dicionario por
                token processado, no formato:
                    {"token": "+", "pilha": ["7"]}
                A lista da pilha ja e uma COPIA formatada do estado daquele
                instante, entao os registros antigos nao mudam quando a
                pilha muda depois.

    Levanta ErroExpressao com as mensagens exigidas pelo enunciado.
    """
    # Aqui o split() por espacos e permitido: a entrada do Desafio 1 JA vem
    # com os tokens separados por espacos.
    tokens = posfixa.split()
    if not tokens:
        raise ErroExpressao("erro: expressao malformada")

    pilha = Pilha()
    for token in tokens:
        if eh_numero(token):
            pilha.empilhar(float(token))
        elif token in OPERADORES:
            # Sao necessarios dois operandos para qualquer operador binario.
            if pilha.tamanho() < 2:
                raise ErroExpressao("erro: operandos insuficientes")
            direito = pilha.desempilhar()     # 1o a sair = operando da DIREITA
            esquerdo = pilha.desempilhar()    # 2o a sair = operando da ESQUERDA
            pilha.empilhar(aplicar(token, esquerdo, direito))
        else:
            raise ErroExpressao("erro: caractere invalido")

        # Registra o estado da pilha DEPOIS de processar este token.
        if rastreio is not None:
            rastreio.append({
                "token": token,
                "pilha": [fmt(valor) for valor in pilha.conteudo()],
            })

    if pilha.tamanho() != 1:
        # Sobrou mais de um operando (ex.: "3 4 5 +").
        raise ErroExpressao("erro: expressao malformada")
    return pilha.desempilhar()


# ------------------------------------------------------------
# Formatacao do rastreamento (monta strings, NAO imprime)
# ------------------------------------------------------------

def montar_linha_avaliacao(token, pilha_texto):
    """Monta uma linha no formato: token (largura 5) | pilha."""
    return f"{token:<{LARGURA_TOKEN}} | {pilha_texto}"


# Cabecalho da tabela do Desafio 1: "token | pilha"
CABECALHO_AVALIACAO = montar_linha_avaliacao("token", "pilha")


def formatar_linha_avaliacao(registro):
    """Transforma um registro do rastreio na linha de texto correspondente."""
    pilha_texto = " ".join(registro["pilha"])
    if pilha_texto == "":
        pilha_texto = "-"
    return montar_linha_avaliacao(registro["token"], pilha_texto)


if __name__ == "__main__":
    # Execucao isolada do Desafio 1: le expressoes POS-FIXAS do teclado.
    print("=" * 52)
    print("DESAFIO 1 - avaliacao de expressoes pos-fixas")
    print("Tokens separados por espacos. Ex.: 3 4 2 * +")
    print("Digite uma linha vazia para sair.")
    print("=" * 52)

    while True:
        try:
            entrada = input("\nposfixa> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nencerrando.")
            break
        if entrada == "":
            print("encerrando.")
            break

        registros = []
        erro = None
        resultado = None
        try:
            resultado = avaliar(entrada, registros)
        except ErroExpressao as problema:
            erro = str(problema)

        print(CABECALHO_AVALIACAO)
        for registro in registros:
            print(formatar_linha_avaliacao(registro))
        if erro is not None:
            print(erro)
        else:
            print("resultado:", fmt(resultado))
