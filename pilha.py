# Arquivo: pilha.py
# Conteudo: estrutura de dados Pilha (LIFO) implementada com
#           encadeamento de nos. Este arquivo e compartilhado
#           pelo desafio1.py, pelo desafio2.py e pelo main.py,
#           evitando duplicacao de codigo.
# ============================================================
"""Pilha encadeada usada em todo o trabalho.

A pilha guarda os elementos em nos ligados. O topo da pilha e o
primeiro no da corrente; cada no aponta para o no que esta logo
abaixo dele. Assim, empilhar e desempilhar custam sempre o mesmo
tempo (O(1)), pois so mexemos no comeco da corrente.

    topo -> [ c ] -> [ b ] -> [ a ] -> None
             (topo)            (base)
"""


class PilhaVazia(Exception):
    """Levantada ao tentar desempilhar ou ler o topo de uma pilha vazia."""


class No:
    """Elemento da pilha: guarda um valor e o endereco do proximo no."""

    def __init__(self, valor, proximo=None):
        self.valor = valor        # o dado guardado (numero ou operador)
        self.proximo = proximo    # o no de baixo (None se este for a base)


class Pilha:
    """Pilha LIFO (Last In, First Out) encadeada.

    Metodos publicos (o contrato usado pelo resto do programa):
        empilhar(valor) -> None
        desempilhar()   -> valor do topo (e o remove)
        topo()          -> valor do topo (sem remover)
        vazia()         -> True/False
        tamanho()       -> quantidade de elementos
        conteudo()      -> lista da BASE para o TOPO (apenas consulta)
    """

    def __init__(self):
        # Os atributos comecam com "_" para indicar que sao internos:
        # nenhuma outra parte do programa deve mexer neles diretamente.
        self._topo = None
        self._tamanho = 0

    def empilhar(self, valor):
        """Coloca um valor no topo da pilha."""
        # O no novo passa a ser o topo e aponta para o antigo topo.
        self._topo = No(valor, self._topo)
        self._tamanho += 1

    def desempilhar(self):
        """Remove e devolve o valor do topo."""
        if self._topo is None:
            raise PilhaVazia("tentativa de desempilhar de uma pilha vazia")
        no_removido = self._topo
        self._topo = no_removido.proximo   # o topo passa a ser o no de baixo
        self._tamanho -= 1
        return no_removido.valor

    def topo(self):
        """Devolve o valor do topo SEM remove-lo."""
        if self._topo is None:
            raise PilhaVazia("tentativa de ler o topo de uma pilha vazia")
        return self._topo.valor

    def vazia(self):
        """True se a pilha nao tem nenhum elemento."""
        return self._topo is None

    def tamanho(self):
        """Quantidade de elementos guardados na pilha."""
        return self._tamanho

    def conteudo(self):
        """Devolve uma LISTA NOVA com os valores da BASE para o TOPO.

        Serve para imprimir o rastreamento sem destruir a pilha.
        Como o encadeamento vai do topo para a base, percorremos nessa
        ordem e invertemos a lista no final. A pilha nao e alterada e a
        lista devolvida e uma copia: quem recebe pode guarda-la que ela
        nao muda quando a pilha muda.
        """
        valores = []
        atual = self._topo
        while atual is not None:
            valores.append(atual.valor)
            atual = atual.proximo
        valores.reverse()      # agora esta da base para o topo
        return valores


if __name__ == "__main__":
    # Demonstracao rapida da pilha (util para explicar na apresentacao).
    print("Demonstracao da Pilha encadeada")
    p = Pilha()
    print("vazia?", p.vazia())
    for letra in ["a", "b", "c"]:
        p.empilhar(letra)
        print("empilhar", letra, "-> conteudo (base->topo):", p.conteudo())
    print("topo (sem remover):", p.topo())
    print("tamanho:", p.tamanho())
    print("desempilhar ->", p.desempilhar())
    print("conteudo (base->topo):", p.conteudo())
    print("vazia?", p.vazia())
