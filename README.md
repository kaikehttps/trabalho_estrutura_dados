<h1 align="center">🧮 Processamento de Expressões Matemáticas</h1>

<p align="center">
  <em>Avaliação de expressões pós-fixas e conversão de expressões convencionais usando <strong>pilha encadeada</strong>.</em>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Disciplina" src="https://img.shields.io/badge/Estruturas_de_Dados-Trabalho_Acadêmico-4B32C3?style=for-the-badge">
  <img alt="Dependências" src="https://img.shields.io/badge/Dependências-Zero-2ea44f?style=for-the-badge">
</p>

---

## 👥 Integrantes

| # | Nome | Matrícula |
|:-:|------|-----------|
| 1 | *Kaike Ferreira Alves - * | 202305010538 |
| 2 | *Gustavo Wendell de Lima Oliveira - * | 2025010420 |
| 3 | *Nome do participante 3* | — |

---

## 🎯 Sobre o trabalho

O projeto resolve **três etapas encadeadas**, todas apoiadas em uma pilha implementada do zero:

| Etapa | O que faz | Exemplo |
|:-----:|-----------|---------|
| **Desafio 1** | Avalia uma expressão **pós-fixa** (notação polonesa reversa) | `3 4 2 * +` → `11` |
| **Desafio 2** | Converte uma expressão **convencional** (infixa) para pós-fixa | `3+4*2` → `3 4 2 * +` |
| **Desafio 3** | Programa principal: lê, converte, avalia e mostra o **rastreamento** | `3+4*2` → `11` |

**Operadores suportados:** `+` `-` `*` `/` `^` (potência) · parênteses · números decimais.

> 🚫 Sem `eval`, sem `exec`, sem bibliotecas externas — apenas a biblioteca padrão do Python e uma pilha encadeada feita à mão.

---

## 📁 Estrutura

```
trabalho_estrutura_dados/
├── pilha.py      → Classe Pilha (LIFO) encadeada com nós — base de tudo
├── desafio1.py   → Avaliação pós-fixa
├── desafio2.py   → Tokenização + conversão (Shunting Yard)
└── main.py       → Menu, entrada do usuário e impressão dos rastreamentos
```

**Dependências entre módulos (sem ciclos):**

```
pilha.py ← desafio1.py ← desafio2.py ← main.py
```

Os módulos de cálculo **não imprimem nada** — toda a saída fica concentrada no [main.py](main.py).

---

## 🚀 Como executar

```bash
python main.py
```

```
============================================================
PROCESSAMENTO DE EXPRESSOES MATEMATICAS
============================================================
1 - Desafio 1: avaliar expressao POS-FIXA
2 - Desafios 2 e 3: converter expressao CONVENCIONAL e avaliar
3 - Rodar a verificacao (exemplos do enunciado)
0 - Sair
```

Cada módulo também roda isolado:

```bash
python desafio1.py    # só a avaliação pós-fixa
python desafio2.py    # só a tokenização e a conversão
python pilha.py       # demonstração da pilha
```

---

## 💡 Exemplo de uso

Entrada: `3+4*2`

```
--- conversao para pos-fixa ---
token | pilha       | saida
3     | -           | 3
+     | +           | 3
4     | +           | 3 4
*     | + *         | 3 4
2     | + *         | 3 4 2
(fim) | -           | 3 4 2 * +
posfixa: 3 4 2 * +

--- avaliacao da pos-fixa ---
token | pilha
3     | 3
4     | 3 4
2     | 3 4 2
*     | 3 8
+     | 11
resultado: 11
```

---

## 🧱 A estrutura de dados

`Pilha` encadeada — cada `No` guarda um valor e aponta para o nó **de baixo**:

```
_topo → [ c ] → [ b ] → [ a ] → None
         topo            base
```

| Método | Ação | Custo |
|--------|------|:-----:|
| `empilhar(valor)` | Insere no topo | `O(1)` |
| `desempilhar()` | Remove e devolve o topo | `O(1)` |
| `topo()` | Lê o topo sem remover | `O(1)` |
| `vazia()` / `tamanho()` | Consulta de estado | `O(1)` |
| `conteudo()` | Cópia dos valores (base → topo), sem destruir a pilha | `O(n)` |

---

## ⚖️ Precedência dos operadores

| Operador | Precedência | Associatividade |
|:--------:|:-----------:|:---------------:|
| `^` | 3 | à direita |
| `*` `/` | 2 | à esquerda |
| `+` `-` | 1 | à esquerda |

Por isso `2^3^2` = **512** (`2^(3^2)`) e `(2^3)^2` = **64**.

---

## 🛡️ Tratamento de erros

Toda entrada inválida gera uma mensagem clara em vez de quebrar o programa:

| Situação | Mensagem |
|----------|----------|
| `3 + * 4` | `erro: operandos insuficientes` |
| `3 4 5 +` | `erro: expressao malformada` |
| `8 0 /` | `erro: divisao por zero` |
| `3+4)` | `erro: parentese fechado sem abertura` |
| `(3+4` | `erro: parentese aberto sem fechamento` |
| `3$4` | `erro: caractere invalido` |

---

## ✅ Verificação automática

A **opção 3** do menu roda todos os exemplos do enunciado — avaliação, conversão e mensagens de erro — marcando cada caso com `OK` ou `FALHOU` e exibindo o total ao final.

---

<p align="center">
  <sub>Trabalho acadêmico · Estruturas de Dados · Python 3</sub>
</p>
