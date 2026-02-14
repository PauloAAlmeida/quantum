# ⚛️ Algoritmo de Grover: Guia resumido (em construção)

Este documento apresenta uma visão detalhada do Algoritmo de Grover, desde a definição do problema até a fundamentação em álgebra linear, utilizando um exemplo prático de busca em uma lista de 8 elementos.

---

## 📋 1. Enunciado do Problema

**Objetivo:** Localizar um índice específico $\omega$ (alvo) em um banco de dados não estruturado de tamanho $N$ de forma mais eficiente que a busca clássica.

* **Tamanho do Banco ($N$):** 8 elementos.
* **Recursos (Qubits):** $n = \log_2(8) = 3$ qubits.
* **A Lista:** `[paulo, dani, pedro, claudio, tiago, maria, marcos, joao]`
* **O Alvo ($\omega$):** `'tiago'`, mapeado para o estado quântico $\vert 100 \rangle$ (5ª posição do vetor).

---

## 🚀 2. Passo a Passo do Algoritmo

### Passo 1: Inicialização
O sistema começa no estado fundamental "zero".
* **Estado:** $\vert \psi_0 \rangle = \vert 000 \rangle$
* **Vetor de Estado:**
$$\begin{pmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \end{pmatrix}^T$$

### Passo 2: Superposição Uniforme (Porta Hadamard)
Aplicamos a porta Hadamard ($H^{\otimes 3}$) em todos os qubits para criar uma mistura igual de todas as possibilidades.
* **Fórmula:** $\vert s \rangle = H^{\otimes 3} \vert 000 \rangle = \frac{1}{\sqrt{8}} \sum_{x=0}^{7} \vert x \rangle$
* **Vetor de Estado (Amplitudes $\approx 0.35$):**
$$\begin{pmatrix} 0.35 & 0.35 & 0.35 & 0.35 & 0.35 & 0.35 & 0.35 & 0.35 \end{pmatrix}^T$$

### Passo 3: O Oráculo (Marcação de Fase)
Inverte o sinal (fase) apenas do estado alvo utilizando a regra: $U_\omega \vert x \rangle = (-1)^{f(x)} \vert x \rangle$.
* **Operação:** Se $x = \text{'tiago'}$, multiplique por $-1$. Caso contrário, multiplique por $1$.
* **Vetor de Estado:**
$$\begin{pmatrix} 0.35 & 0.35 & 0.35 & 0.35 & -0.35 & 0.35 & 0.35 & 0.35 \end{pmatrix}^T$$

### Passo 4: O Difusor (Amplificação de Amplitude)
Realiza a inversão em torno da média para aumentar a probabilidade do estado marcado.
* **Fórmula:** $2 \times \text{Média} - \text{Valor Atual}$
* **Vetor de Estado Final:**
$$\begin{pmatrix} 0.17 & 0.17 & 0.17 & 0.17 & 0.87 & 0.17 & 0.17 & 0.17 \end{pmatrix}^T$$

---

## 📊 3. Tabela de Probabilidades (Medição)

| Nome | Estado Binário | Amplitude | Probabilidade |
| :--- | :--- | :--- | :--- |
| paulo | $\vert 000 \rangle$ | 0.17 | ~3% |
| dani | $\vert 001 \rangle$ | 0.17 | ~3% |
| pedro | $\vert 010 \rangle$ | 0.17 | ~3% |
| claudio | $\vert 011 \rangle$ | 0.17 | ~3% |
| **tiago** | $\mathbf{\vert 100 \rangle}$ | **0.87** | **~78%** |
| maria | $\vert 101 \rangle$ | 0.17 | ~3% |
| marcos | $\vert 110 \rangle$ | 0.17 | ~3% |
| joao | $\vert 111 \rangle$ | 0.17 | ~3% |

---
> **Dica:** A aceleração de Grover é quadrática, ou seja, para uma lista de $N$ itens, precisamos de aproximadamente $\sqrt{N}$ iterações.
