# Processamento de Expressões Matemáticas

**Disciplina:** Estruturas de Dados

## Integrantes

| Nome | Matrícula |
| ---- | --------- |
|      |           |
|      |           |
|      |           |
|      |           |

---

## 1. Objetivo

O trabalho resolve três etapas encadeadas:

1. **Desafio 1** — avaliar uma expressão **pós-fixa** (notação polonesa reversa), com os tokens separados por espaços. Ex.: `3 4 +` → `7`.
2. **Desafio 2** — converter uma expressão **convencional** (infixa) para pós-fixa. Ex.: `3+4*2` → `3 4 2 * +`.
3. **Programa principal** — ler expressões convencionais, converter, avaliar e mostrar o **rastreamento** das duas etapas.

Operadores aceitos: `+`, `-`, `*`, `/` e `^` (potência). O símbolo `^` é o da entrada; o cálculo em Python usa `**`.

Só é usada a **biblioteca padrão** do Python 3. Não há `eval`, `exec`, nem biblioteca que resolva expressões automaticamente: tudo é feito na mão, com uma pilha encadeada.

---

## 2. Organização dos arquivos

| Arquivo | Conteúdo |
| ------- | -------- |
| `pilha.py` | Classe `Pilha` encadeada (nós) e a classe `No`. Compartilhada pelos demais arquivos. |
| `desafio1.py` | Avaliação pós-fixa: `fmt`, `eh_numero`, `aplicar`, `avaliar` e a exceção `ErroExpressao`. |
| `desafio2.py` | Tokenização e conversão: `tokenizar`, `validar`, `deve_desempilhar`, `converter`. |
| `main.py` | Programa principal: menu, leitura das expressões, impressão dos rastreamentos e a verificação automática. |
| `registro.md` | Este documento. |

**Dependências (sem ciclos):**

```
pilha.py   <-- desafio1.py <-- desafio2.py <-- main.py
```

`pilha.py` não importa ninguém. `desafio2.py` importa de `desafio1.py` apenas `ErroExpressao` e `eh_numero`, para não duplicar a exceção nem a regra do que é um número.

---

## 3. Como executar

Pré-requisito: Python 3 instalado (o projeto foi executado com **Python 3.14.3** no Windows).

Abra o terminal na pasta do projeto e rode:

```bash
python main.py
```

O menu aparece:

```
============================================================
PROCESSAMENTO DE EXPRESSOES MATEMATICAS
============================================================
1 - Desafio 1: avaliar expressao POS-FIXA
2 - Desafios 2 e 3: converter expressao CONVENCIONAL e avaliar
3 - Rodar a verificacao (exemplos do enunciado)
0 - Sair
opcao>
```

- Dentro das opções 1 e 2 é possível digitar **quantas expressões quiser**.
- Uma **linha vazia** volta ao menu; a opção `0` (ou linha vazia no menu) encerra o programa.

Os desafios também rodam isolados, cada um com seu próprio laço de leitura:

```bash
python desafio1.py     # só a avaliação pós-fixa
python desafio2.py     # só a tokenização e a conversão
python pilha.py        # demonstração da pilha
```

---

## 4. A pilha encadeada (`pilha.py`)

A pilha é a estrutura central do trabalho: ela é **LIFO** (*Last In, First Out*), ou seja, o último elemento a entrar é o primeiro a sair — exatamente o comportamento necessário tanto para guardar operandos quanto para guardar operadores.

### Como o encadeamento funciona

Cada elemento é um objeto `No` com dois campos: o `valor` guardado e o `proximo`, que aponta para o nó **de baixo**. A pilha guarda apenas a referência do topo:

```
_topo -> [ c ] -> [ b ] -> [ a ] -> None
          topo             base
```

Empilhar cria um nó novo que aponta para o antigo topo; desempilhar faz o topo passar a ser o nó de baixo. As duas operações mexem só no começo da corrente, por isso custam tempo constante — **O(1)** — e não dependem do tamanho da pilha.

### Contrato público

| Método | O que faz |
| ------ | --------- |
| `empilhar(valor)` | Coloca um valor no topo. |
| `desempilhar()` | Remove e devolve o valor do topo. |
| `topo()` | Devolve o valor do topo **sem** remover. |
| `vazia()` | `True` se não há elementos. |
| `tamanho()` | Quantidade de elementos. |
| `conteudo()` | **Lista nova** com os valores da **base para o topo**, sem alterar a pilha. |

`desempilhar()` e `topo()` em uma pilha vazia levantam `PilhaVazia`. Na prática isso não acontece durante a execução normal, porque `avaliar` e `converter` verificam `tamanho()` e `vazia()` antes de chamar — a exceção é uma proteção.

### O método `conteudo()`

Foi acrescentado à própria classe, como pede o enunciado, para permitir **imprimir o rastreamento sem destruir a pilha**. Ele percorre o encadeamento do topo até a base, monta uma lista e a inverte com `reverse()`, devolvendo os valores na ordem **base → topo**.

Dois detalhes importantes:

- A pilha **não é modificada** — só é lida.
- A lista devolvida é uma **cópia nova** a cada chamada. Por isso os registros antigos do rastreamento continuam mostrando o estado daquele instante mesmo depois de a pilha mudar.

O restante do programa **nunca** acessa `_topo`, `_tamanho` ou os nós: só usa os seis métodos da tabela. O sublinhado no nome dos atributos marca justamente que eles são internos.

### Por que uma implementação própria

A classe usada em aula não foi fornecida junto com o enunciado, então foi implementada uma versão equivalente, com os nomes de método exigidos (`empilhar`, `desempilhar`, `topo`, `vazia`, `tamanho`) em português. Se a classe da aula for disponibilizada, basta substituir o conteúdo de `pilha.py` mantendo esses nomes e acrescentando o `conteudo()`: nenhum outro arquivo precisa ser alterado, porque todos dependem apenas desse contrato.

Listas do Python são usadas só para o que **não é pilha**: a lista de tokens, a lista de saída da conversão e os registros do rastreamento. Nenhuma pilha do trabalho é simulada com `list.append`/`list.pop`.

---

## 5. Desafio 1 — avaliação pós-fixa (`desafio1.py`)

### Algoritmo

Percorrendo os tokens da esquerda para a direita:

1. **Número** → empilha (convertido para `float`).
2. **Operador** → desempilha **dois** operandos, calcula e empilha o resultado.
3. **Fim** → a pilha deve conter **exatamente um** valor: o resultado.

### A ordem dos operandos

Este é o ponto mais fácil de errar. Como a pilha é LIFO, o **primeiro** valor a sair é o que entrou por último, que é o operando da **direita**:

```python
direito  = pilha.desempilhar()   # 1º a sair  -> operando da DIREITA
esquerdo = pilha.desempilhar()   # 2º a sair  -> operando da ESQUERDA
pilha.empilhar(aplicar(token, esquerdo, direito))
```

Para `+` e `*` a ordem não mudaria o resultado, mas para `-`, `/` e `^` ela é decisiva: em `10 3 -`, invertendo a ordem o programa calcularia `3 - 10 = -7` em vez de `10 - 3 = 7`.

### Formato do rastreamento

Largura 5 para o token, alinhado à esquerda, seguido de `|`, e a pilha da base para o topo:

```
token | pilha
3     | 3
4     | 3 4
+     | 7
resultado: 7
```

A linha é montada por `montar_linha_avaliacao`, com `f"{token:<5} | {pilha_texto}"`. Todos os números são formatados pela função exigida:

```python
def fmt(v):
    return f"{v:g}"
```

O `:g` remove o `.0` dos resultados inteiros (`7.0` vira `7`) e mantém as casas necessárias nos decimais (`0.75`).

### Erros tratados

| Situação | Mensagem | Exemplo |
| -------- | -------- | ------- |
| Menos de dois operandos na pilha ao encontrar um operador | `erro: operandos insuficientes` | `3 + * 4` |
| Sobra mais de um operando no final | `erro: expressao malformada` | `3 4 5 +` |
| Divisor igual a zero | `erro: divisao por zero` | `8 0 /` |
| Token que não é número nem operador | `erro: caractere invalido` | `3 4 a +` |
| Expressão vazia | `erro: expressao malformada` | `` |

---

## 6. Desafio 2 — tokenização e conversão (`desafio2.py`)

### Tokenização

`tokenizar` faz uma **varredura caractere a caractere** (não usa `split()`), porque na expressão convencional os tokens podem estar grudados:

- **espaço** → ignorado (serve só como separador);
- **dígito ou `.`** → começo de um número: o laço interno avança enquanto houver dígito ou ponto, juntando tudo em **um único token** (é assim que `42` e `2.5` não viram `4`,`2`);
- **operador ou parêntese** → token de um caractere;
- **qualquer outra coisa** → `erro: caractere invalido`.

Por isso `3+42*(7-1)` e `3 + 42 * ( 7 - 1 )` produzem exatamente a mesma lista:

```python
['3', '+', '42', '*', '(', '7', '-', '1', ')']
```

### Validação da estrutura

`validar` percorre os tokens guardando uma **expectativa**: em cada posição o programa sabe se o próximo token deveria ser um *operando* (número ou `(`) ou um *operador* (ou `)`). Também conta quantos parênteses estão abertos. Isso rejeita, com mensagem clara e sem quebrar o programa:

| Entrada | Motivo | Mensagem |
| ------- | ------ | -------- |
| *(vazia)* | nada a processar | `erro: expressao malformada` |
| `3+*4` | dois operadores seguidos | `erro: expressao malformada` |
| `3+` | termina em operador | `erro: expressao malformada` |
| `-3+4` | sinal unário (não exigido) | `erro: expressao malformada` |
| `2(3+1)` | multiplicação implícita (não exigida) | `erro: expressao malformada` |
| `3 4` | dois números seguidos | `erro: expressao malformada` |
| `()` | parênteses sem conteúdo | `erro: expressao malformada` |
| `3+4)` | fecha sem ter aberto | `erro: parentese fechado sem abertura` |
| `(3+4` | abre e não fecha | `erro: parentese aberto sem fechamento` |
| `3$4` | símbolo desconhecido (pego na tokenização) | `erro: caractere invalido` |

### Conversão (algoritmo *Shunting Yard*)

A pilha aqui guarda **operadores e `(`** — nunca números. A lista `saida` vai recebendo os tokens já posicionados da expressão pós-fixa.

| Token | Ação |
| ----- | ---- |
| número | vai direto para a **saída** |
| `(` | empilha (marca o início de um trecho) |
| `)` | desempilha para a saída até achar `(` e **descarta** o `(` |
| operador | desempilha para a saída todos os operadores do topo que devem ser aplicados antes; depois empilha o novo |
| fim | esvazia a pilha para a saída |

Parênteses **não aparecem** na pós-fixa: a ordem dos tokens já expressa o agrupamento.

### Precedência e associatividade

| Operadores | Precedência | Associatividade |
| ---------- | ----------: | --------------- |
| `+` e `-`  | 1 | Esquerda |
| `*` e `/`  | 2 | Esquerda |
| `^`        | 3 | Direita |

A decisão fica isolada na função `deve_desempilhar(topo, operador)`:

```python
if topo == "(":
    return False
if PRECEDENCIA[topo] > PRECEDENCIA[operador]:
    return True
if PRECEDENCIA[topo] == PRECEDENCIA[operador]:
    return ASSOCIATIVIDADE[operador] == "esquerda"
return False
```

Lendo em português:

1. O `(` **nunca** sai nesse momento — ele só é removido pelo `)` correspondente. É isso que faz o parêntese "proteger" o que está dentro dele.
2. Sai quem tem precedência **maior** que a do operador novo (o `*` sai antes do `+` chegar).
3. **No empate**, só sai se o operador novo for associativo à **esquerda**.

#### Por que a regra do empate preserva a associatividade à direita de `^`

O empate é exatamente o caso em que a associatividade decide, e a condição `ASSOCIATIVIDADE[operador] == "esquerda"` trata os dois casos:

- **`10-3-2`** — quando o segundo `-` chega, o topo é `-`: precedências iguais e `-` é associativo à **esquerda**, então o `-` do topo **sai** antes. Resultado: `10 3 - 2 -`, que é `(10-3)-2 = 5`. Se ele não saísse, a conta viraria `10-(3-2) = 9`.
- **`2^3^2`** — quando o segundo `^` chega, o topo é `^`: precedências iguais, mas `^` é associativo à **direita**, então o `^` do topo **fica** e o novo é empilhado por cima. Como a pilha é LIFO, no esvaziamento final o `^` de cima (o da direita) sai primeiro. Resultado: `2 3 2 ^ ^`, que é `2^(3^2) = 512` — e não `(2^3)^2 = 64`.

Em uma frase: **empate com associatividade à esquerda desempilha; empate com associatividade à direita empilha.** Empilhar por cima adia o operador da esquerda, e adiar na pilha significa aplicar depois.

### Formato do rastreamento

Largura 5 para o token, 11 para a pilha, `-` quando pilha ou saída estiverem vazias, e o token literal `(fim)` no esvaziamento final:

```
token | pilha       | saida
3     | -           | 3
+     | +           | 3
4     | +           | 3 4
(fim) | -           | 3 4 +
posfixa: 3 4 +
```

---

## 7. Como o rastreamento é passado para o programa principal

O enunciado exige que `converter` receba uma string e devolva uma string, e que as funções **não imprimam**. Para expor o rastreamento sem mudar o retorno, `avaliar` e `converter` recebem um **parâmetro opcional** `rastreio`:

```python
registros = []
posfixa = converter("3+4", registros)   # retorno continua sendo a string
```

- Se `rastreio` for `None` (o padrão), nada é registrado e a função funciona normalmente — é assim que a verificação automática a usa.
- Se for uma lista, ela recebe um dicionário por token:
  - avaliação: `{"token": "+", "pilha": ["7"]}`
  - conversão: `{"token": "+", "pilha": ["+"], "saida": ["3"]}`

**Os estados são cópias.** `pilha.conteudo()` devolve uma lista nova e a saída é copiada com `list(saida)`. Sem isso, todos os registros apontariam para a mesma lista e, no final, todas as linhas do rastreamento mostrariam o **estado final** repetido.

Como a lista é preenchida durante a execução, se ocorrer um erro no meio do caminho ela **já contém os passos que deram certo**. Por isso o `main.py` imprime o rastreamento parcial e só então a mensagem de erro — dá para ver exatamente onde o processamento parou.

---

## 8. Exemplos de uso (saídas reais do programa)

### 8.1 Expressão com parênteses

```
infixa> 3+4*(2-1)
tokens: ['3', '+', '4', '*', '(', '2', '-', '1', ')']

--- conversao para pos-fixa ---
token | pilha       | saida
3     | -           | 3
+     | +           | 3
4     | +           | 3 4
*     | + *         | 3 4
(     | + * (       | 3 4
2     | + * (       | 3 4 2
-     | + * ( -     | 3 4 2
1     | + * ( -     | 3 4 2 1
)     | + *         | 3 4 2 1 -
(fim) | -           | 3 4 2 1 - * +
posfixa: 3 4 2 1 - * +

--- avaliacao da pos-fixa ---
token | pilha
3     | 3
4     | 3 4
2     | 3 4 2
1     | 3 4 2 1
-     | 3 4 1
*     | 3 4
+     | 7
resultado: 7
```

### 8.2 Associatividade à direita

```
infixa> 2^3^2
tokens: ['2', '^', '3', '^', '2']

--- conversao para pos-fixa ---
token | pilha       | saida
2     | -           | 2
^     | ^           | 2
3     | ^           | 2 3
^     | ^ ^         | 2 3
2     | ^ ^         | 2 3 2
(fim) | -           | 2 3 2 ^ ^
posfixa: 2 3 2 ^ ^

--- avaliacao da pos-fixa ---
token | pilha
2     | 2
3     | 2 3
2     | 2 3 2
^     | 2 9
^     | 512
resultado: 512
```

Repare nas duas últimas linhas da avaliação: primeiro sai `3^2 = 9` e só depois `2^9 = 512`.

### 8.3 Decimais e números com vários dígitos

```
infixa> 2.5*(10-4)
tokens: ['2.5', '*', '(', '10', '-', '4', ')']
...
posfixa: 2.5 10 4 - *
resultado: 15
```

### 8.4 Erros

```
posfixa> 3 + * 4
token | pilha
3     | 3
erro: operandos insuficientes

posfixa> 8 0 /
token | pilha
8     | 8
0     | 8 0
erro: divisao por zero

infixa> 3+4)
tokens: ['3', '+', '4', ')']
erro: parentese fechado sem abertura

infixa> 3$4
tokens: erro: caractere invalido
erro: caractere invalido
```

Em todos os casos o programa continua rodando e pede a próxima expressão.

Observação: os erros de estrutura (parênteses, sinal unário, expressão vazia) são detectados por `validar` **antes** do laço de conversão, então o rastreamento aparece vazio — só o cabeçalho. Os erros da avaliação acontecem no meio do laço, então o rastreamento mostra os passos já executados.

---

## 9. Verificação executada

A opção **3** do menu roda a bateria de testes. Os casos ficam nas listas `TESTES_POSFIXA`, `TESTES_INFIXA` e `TESTES_ERRO`, no `main.py`, e incluem todos os exemplos do enunciado mais decimais, números com vários dígitos e todas as mensagens de erro.

Resultado da execução (Python 3.14.3, Windows):

```
Total: 37 casos | falhas: 0
```

Casos verificados:

**Avaliação pós-fixa**

| Entrada | Resultado |
| ------- | --------: |
| `3 4 +` | 7 |
| `3 4 2 * +` | 11 |
| `3 4 + 2 *` | 14 |
| `10 3 -` | 7 |
| `20 4 /` | 5 |
| `5 1 2 + 4 * + 3 -` | 14 |
| `2.5 1.5 +` | 4 |
| `100 25 /` | 4 |
| `2 3 2 ^ ^` | 512 |
| `2 3 ^ 2 ^` | 64 |

**Conversão e avaliação**

| Entrada | Pós-fixa | Resultado |
| ------- | -------- | --------: |
| `3+4*2` | `3 4 2 * +` | 11 |
| `(3+4)*2` | `3 4 + 2 *` | 14 |
| `1+2*3-4/2` | `1 2 3 * + 4 2 / -` | 5 |
| `3+4*(2-1)` | `3 4 2 1 - * +` | 7 |
| `10-3-2` | `10 3 - 2 -` | 5 |
| `2^3^2` | `2 3 2 ^ ^` | 512 |
| `(2^3)^2` | `2 3 ^ 2 ^` | 64 |
| `3+42*(7-1)` | `3 42 7 1 - * +` | 255 |
| `2.5*4` | `2.5 4 *` | 10 |
| `0.5+0.25` | `0.5 0.25 +` | 0.75 |
| `3 + 4 * 2` | `3 4 2 * +` | 11 |

**Mensagens de erro** — 16 casos, cobrindo as seis mensagens exigidas (`3 + * 4`, `3 4 5 +`, `8 0 /`, `+`, vazia, `3 4 a +`, `3+4)`, `(3+4`, `3$4`, `3+*4`, `3+`, `-3+4`, `2(3+1)`, `()`, `8/0`).

---

## 10. Decisões e limitações

1. **Pilha própria, contrato preservado.** A classe da aula não foi fornecida; foi implementada uma equivalente com os métodos pedidos. Trocá-la exige alterar só `pilha.py`.
2. **Uma única exceção, `ErroExpressao`, com a mensagem pronta.** Ela é definida em `desafio1.py` e reutilizada por `desafio2.py`. As funções levantam o erro; quem imprime é o `main.py`. Isso mantém a regra de que as funções não imprimem e evita `print` espalhado.
3. **Números viram `float`.** Simplifica o código (um único tipo) e a função `fmt` com `:g` esconde o `.0` na impressão. Consequência conhecida: divisões podem trazer dízimas de ponto flutuante (`10/3`), e o `:g` arredonda a exibição para 6 dígitos significativos.
4. **Sinal unário não é aceito.** `-3+4` e `+5` são recusados com `erro: expressao malformada`. Para negativos, use a forma `(0-3)`. Em pós-fixa, `-8` também é recusado (`erro: caractere invalido`), para manter a mesma regra do que é um número nos dois desafios.
5. **Multiplicação implícita não é aceita.** `2(3+1)` e `(1+2)(3+4)` são recusados; é preciso escrever o `*`.
6. **Operadores são sempre binários** e só existem os cinco do enunciado. Não há funções (`sen`, `raiz`), variáveis nem constantes.
7. **Casos numéricos extremos** (potência que estoura o `float`, ou base negativa com expoente fracionário, que daria número complexo) são reportados como `erro: expressao malformada`, para não deixar escapar exceção não tratada. Mensagens novas não foram inventadas: são usadas apenas as do enunciado.
8. **`split()` só na entrada pós-fixa.** Ali os tokens já vêm separados por espaços, como manda o enunciado. Na expressão convencional a tokenização é feita caractere a caractere.
9. **Entrada e saída pós-fixas sempre com espaços**, mesmo que algumas tabelas do PDF mostrem os tokens visualmente juntos.
10. **Leitura resistente ao BOM.** `ler_linha` remove um caractere invisível (`﻿`, chamado BOM) que alguns terminais — o PowerShell, por exemplo — inserem quando a entrada vem de um arquivo redirecionado. Sem isso, a primeira linha lida viria "suja".
11. **Ambiguidade visual do `-` no rastreamento.** O enunciado pede `-` para indicar pilha ou saída vazias, e `-` também é o operador de subtração. Em `10-3-2`, a linha `-     | -           | 10` significa "token `-`, pilha contendo o operador `-`". A ambiguidade é apenas visual, no formato exigido; internamente os dois casos são distintos.
12. **A impressão fica no programa principal.** Os blocos `if __name__ == "__main__":` de `desafio1.py` e `desafio2.py` também imprimem, mas eles *são* programas principais — servem para rodar cada desafio isolado durante a apresentação.

---

## 11. Declaração de uso de IA

Na elaboração deste trabalho foi utilizada a ferramenta **Claude (Anthropic)**, por meio do Claude Code, com as seguintes finalidades:

- escrita do código-fonte dos arquivos `pilha.py`, `desafio1.py`, `desafio2.py` e `main.py`, a partir das exigências do enunciado;
- organização do código em funções, redação dos comentários e das explicações didáticas;
- montagem da bateria de casos de verificação e execução desses casos no ambiente local (Python 3.14.3, Windows), com correção dos problemas encontrados;
- redação deste `registro.md`.

Nenhuma outra ferramenta de IA foi utilizada. As saídas reproduzidas na seção 8 e o resultado da seção 9 foram obtidos executando os arquivos entregues.
