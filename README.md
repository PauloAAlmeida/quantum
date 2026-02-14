# 📐 Álgebra Linear para Computação Quântica: Guia resumido 
(versão inicial by Paulo, em melhoria continua, fique a vontade de mandar PR!)

Este guia consolida os conceitos matemáticos essenciais para entender estados quânticos, operadores e algoritmos, otimizado para visualização no GitHub.

---

## 1. Números Complexos

A computação quântica opera sobre o corpo dos números complexos $\mathbb{C}$.

Um número complexo tem a forma $z = a + bi$, onde $a$ é a parte real, $b$ a parte imaginária e $i = \sqrt{-1}$.

**Operações fundamentais:**

```math
z = a + bi, \quad \bar{z} = a - bi \quad \text{(conjugado)}
```

```math
|z| = \sqrt{a^2 + b^2} \quad \text{(módulo)}
```

```math
|z|^2 = z \cdot \bar{z} = a^2 + b^2 \quad \text{(módulo ao quadrado)}
```

**Forma polar (Euler):**

```math
z = r e^{i\theta} = r(\cos\theta + i\sin\theta)
```

Essa representação é essencial para entender rotações de fase em qubits.

**Propriedades usadas em quântica:**

| Propriedade | Expressão | Uso |
| :--- | :--- | :--- |
| Conjugado do produto | $\overline{zw} = \bar{z}\bar{w}$ | Adjunto de operadores |
| Módulo do produto | $\|zw\| = \|z\|\|w\|$ | Preservação de norma |
| Identidade de Euler | $e^{i\pi} + 1 = 0$ | Porta de fase |
| Raiz da unidade | $e^{2\pi i/N}$ | QFT (Transformada Quântica de Fourier) |

---

## 2. Espaços Vetoriais e Espaço de Hilbert

Um **espaço vetorial** sobre $\mathbb{C}$ é um conjunto de vetores com operações de soma e multiplicação por escalar.

O **Espaço de Hilbert** $\mathcal{H}$ é um espaço vetorial complexo com produto interno, completo em relação à norma induzida. Todo estado quântico vive em um Espaço de Hilbert.

**Para um qubit:** $\mathcal{H} = \mathbb{C}^2$ (espaço de dimensão 2).

**Para $n$ qubits:** $\mathcal{H} = \mathbb{C}^{2^n}$ (dimensão cresce exponencialmente).

**Propriedades do espaço vetorial:**

| Propriedade | Descrição |
| :--- | :--- |
| Fechamento | $\|\psi\rangle + \|\phi\rangle \in \mathcal{H}$ |
| Associatividade | $(\|\psi\rangle + \|\phi\rangle) + \|\chi\rangle = \|\psi\rangle + (\|\phi\rangle + \|\chi\rangle)$ |
| Elemento neutro | Existe $\|0\rangle$ tal que $\|\psi\rangle + \|0\rangle = \|\psi\rangle$ |
| Distributividade | $\alpha(\|\psi\rangle + \|\phi\rangle) = \alpha\|\psi\rangle + \alpha\|\phi\rangle$ |

---

## 3. Notação de Dirac (Bra-Ket)

Na mecânica quântica, os estados são vetores em um Espaço de Hilbert.

* **Ket $|\psi\rangle$**: Representa um **vetor coluna** (estado quântico).
* **Bra $\langle\psi|$**: Representa um **vetor linha** (dual conjugado transposto).

```math
|\psi\rangle = \begin{pmatrix} \alpha \\ \beta \end{pmatrix} \quad \longleftrightarrow \quad \langle\psi| = \begin{pmatrix} \alpha^* & \beta^* \end{pmatrix}
```

A passagem de ket para bra envolve **transpor** e **conjugar** cada componente:

```math
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle \quad \Rightarrow \quad \langle\psi| = \alpha^*\langle 0| + \beta^*\langle 1|
```

---

## 4. Bases Computacionais e Superposição

### Base Computacional (Z)

Os estados básicos formam uma **base ortonormal** para $\mathbb{C}^2$:

```math
|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad |1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}
```

### Base de Hadamard (X)

```math
|+\rangle = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 1 \end{pmatrix} = \frac{|0\rangle + |1\rangle}{\sqrt{2}}, \quad |-\rangle = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ -1 \end{pmatrix} = \frac{|0\rangle - |1\rangle}{\sqrt{2}}
```

### Base Circular (Y)

```math
|R\rangle = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ -i \end{pmatrix} = \frac{|0\rangle - i|1\rangle}{\sqrt{2}}, \quad |L\rangle = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ i \end{pmatrix} = \frac{|0\rangle + i|1\rangle}{\sqrt{2}}
```

### Superposição Geral

Qualquer estado de um qubit pode ser escrito como:

```math
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle, \quad |\alpha|^2 + |\beta|^2 = 1
```

Os coeficientes $\alpha$ e $\beta$ são **amplitudes de probabilidade**. A probabilidade de medir $|0\rangle$ é $|\alpha|^2$ e de medir $|1\rangle$ é $|\beta|^2$.

---

## 5. Representação na Esfera de Bloch

Todo estado puro de um qubit pode ser parametrizado por dois ângulos:

```math
|\psi\rangle = \cos\frac{\theta}{2}|0\rangle + e^{i\phi}\sin\frac{\theta}{2}|1\rangle
```

onde $\theta \in [0, \pi]$ é o ângulo polar e $\phi \in [0, 2\pi)$ é o ângulo azimutal.

**Correspondência com a esfera:**

| Estado | $\theta$ | $\phi$ | Posição |
| :--- | :--- | :--- | :--- |
| $\|0\rangle$ | $0$ | — | Polo norte |
| $\|1\rangle$ | $\pi$ | — | Polo sul |
| $\|+\rangle$ | $\pi/2$ | $0$ | Eixo +X |
| $\|-\rangle$ | $\pi/2$ | $\pi$ | Eixo -X |
| $\|R\rangle$ | $\pi/2$ | $3\pi/2$ | Eixo -Y |
| $\|L\rangle$ | $\pi/2$ | $\pi/2$ | Eixo +Y |

---

## 6. Produto Interno e Norma

O **produto interno** entre dois estados é um escalar complexo:

```math
\langle\phi|\psi\rangle = \sum_i \phi_i^* \psi_i
```

**Propriedades:**

| Propriedade | Expressão |
| :--- | :--- |
| Conjugado simétrico | $\langle\phi\|\psi\rangle = \overline{\langle\psi\|\phi\rangle}$ |
| Linearidade à direita | $\langle\phi\|(\alpha\|\psi\rangle + \beta\|\chi\rangle) = \alpha\langle\phi\|\psi\rangle + \beta\langle\phi\|\chi\rangle$ |
| Positividade | $\langle\psi\|\psi\rangle \geq 0$, igual a zero somente se $\|\psi\rangle = 0$ |

**Norma** de um vetor:

```math
\||\psi\rangle\| = \sqrt{\langle\psi|\psi\rangle}
```

Um estado quântico válido tem norma 1 (é **normalizado**).

**Ortogonalidade:** dois estados são ortogonais se $\langle\phi|\psi\rangle = 0$.

---

## 7. Produto Externo

O **produto externo** de dois vetores produz uma **matriz** (operador):

```math
|\psi\rangle\langle\phi| = \begin{pmatrix} \alpha \\ \beta \end{pmatrix} \begin{pmatrix} \gamma^* & \delta^* \end{pmatrix} = \begin{pmatrix} \alpha\gamma^* & \alpha\delta^* \\ \beta\gamma^* & \beta\delta^* \end{pmatrix}
```

**Projetores** são produtos externos de um vetor consigo mesmo:

```math
P_0 = |0\rangle\langle 0| = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}, \quad P_1 = |1\rangle\langle 1| = \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}
```

**Relação de completeza** (resolução da identidade):

```math
|0\rangle\langle 0| + |1\rangle\langle 1| = I
```

Isso generaliza para qualquer base ortonormal: $\sum_i |i\rangle\langle i| = I$.

---

## 8. Produto Tensorial ($\otimes$)

Para sistemas de $n$ qubits, a dimensão do vetor cresce em $2^n$.

**Definição para vetores:**

```math
\begin{pmatrix} a \\ b \end{pmatrix} \otimes \begin{pmatrix} c \\ d \end{pmatrix} = \begin{pmatrix} a \cdot c \\ a \cdot d \\ b \cdot c \\ b \cdot d \end{pmatrix}
```

**Definição para matrizes (produto de Kronecker):**

```math
A \otimes B = \begin{pmatrix} a_{11}B & a_{12}B \\ a_{21}B & a_{22}B \end{pmatrix}
```

**Propriedades:**

| Propriedade | Expressão |
| :--- | :--- |
| Bilinearidade | $\alpha(\|a\rangle \otimes \|b\rangle) = (\alpha\|a\rangle) \otimes \|b\rangle = \|a\rangle \otimes (\alpha\|b\rangle)$ |
| Associatividade | $(\|a\rangle \otimes \|b\rangle) \otimes \|c\rangle = \|a\rangle \otimes (\|b\rangle \otimes \|c\rangle)$ |
| Distributividade | $\|a\rangle \otimes (\|b\rangle + \|c\rangle) = \|a\rangle \otimes \|b\rangle + \|a\rangle \otimes \|c\rangle$ |
| Produto misto | $(A \otimes B)(C \otimes D) = (AC) \otimes (BD)$ |

**Notação abreviada:** $|0\rangle \otimes |1\rangle = |0\rangle|1\rangle = |01\rangle$.

**Exemplo com 2 qubits — Base computacional de $\mathbb{C}^4$:**

```math
|00\rangle = \begin{pmatrix} 1\\0\\0\\0 \end{pmatrix}, \quad |01\rangle = \begin{pmatrix} 0\\1\\0\\0 \end{pmatrix}, \quad |10\rangle = \begin{pmatrix} 0\\0\\1\\0 \end{pmatrix}, \quad |11\rangle = \begin{pmatrix} 0\\0\\0\\1 \end{pmatrix}
```

**3 Qubits (Base do Grover):**

```math
|000\rangle = |0\rangle \otimes |0\rangle \otimes |0\rangle = \begin{pmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \end{pmatrix}^T
```

---

## 9. Emaranhamento (Entanglement)

Um estado de dois qubits é **emaranhado** se **não pode** ser escrito como produto tensorial de dois estados individuais.

**Estados de Bell (maximamente emaranhados):**

```math
|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}, \quad |\Phi^-\rangle = \frac{|00\rangle - |11\rangle}{\sqrt{2}}
```

```math
|\Psi^+\rangle = \frac{|01\rangle + |10\rangle}{\sqrt{2}}, \quad |\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}}
```

**Como verificar emaranhamento:** tente fatorar o estado. Se $|\psi\rangle_{AB} \neq |\alpha\rangle_A \otimes |\beta\rangle_B$ para quaisquer $|\alpha\rangle$, $|\beta\rangle$, o estado é emaranhado.

**Exemplo:** $|\Phi^+\rangle = \frac{1}{\sqrt{2}}\begin{pmatrix} 1\\0\\0\\1 \end{pmatrix}$ não pode ser fatorado — é emaranhado.

---

## 10. Matrizes e Operadores Lineares

Um **operador linear** é uma função $A: \mathcal{H} \rightarrow \mathcal{H}$ que satisfaz:

```math
A(\alpha|\psi\rangle + \beta|\phi\rangle) = \alpha A|\psi\rangle + \beta A|\phi\rangle
```

### Tipos de Matrizes Importantes

**Transposta e Conjugada:**

```math
A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}, \quad A^T = \begin{pmatrix} a & c \\ b & d \end{pmatrix}, \quad A^* = \begin{pmatrix} \bar{a} & \bar{b} \\ \bar{c} & \bar{d} \end{pmatrix}
```

**Adjunto (dagger):**

```math
A^\dagger = (A^T)^* = (A^*)^T = \begin{pmatrix} \bar{a} & \bar{c} \\ \bar{b} & \bar{d} \end{pmatrix}
```

| Tipo | Condição | Propriedade | Uso em Quântica |
| :--- | :--- | :--- | :--- |
| Hermitiana | $A = A^\dagger$ | Autovalores reais | Observáveis (medição) |
| Unitária | $UU^\dagger = I$ | Preserva norma | Portas quânticas |
| Normal | $AA^\dagger = A^\dagger A$ | Diagonalizável | Teorema espectral |
| Projetor | $P^2 = P = P^\dagger$ | Idempotente | Medição projetiva |
| Positiva semi-definida | $\langle\psi\|A\|\psi\rangle \geq 0$ | Autovalores $\geq 0$ | Matrizes densidade |

---

## 11. Autovalores e Autovetores

Se $A|v\rangle = \lambda|v\rangle$, então $\lambda$ é um **autovalor** e $|v\rangle$ é um **autovetor** de $A$.

**Exemplo com Pauli-Z:**

```math
Z|0\rangle = (+1)|0\rangle, \quad Z|1\rangle = (-1)|1\rangle
```

Os autovalores de $Z$ são $+1$ e $-1$, com autovetores $|0\rangle$ e $|1\rangle$.

**Exemplo com Pauli-X:**

```math
X|+\rangle = (+1)|+\rangle, \quad X|-\rangle = (-1)|-\rangle
```

**Decomposição espectral** — toda matriz hermitiana pode ser escrita como:

```math
A = \sum_i \lambda_i |v_i\rangle\langle v_i|
```

onde $\lambda_i$ são os autovalores e $|v_i\rangle$ os autovetores ortonormais.

---

## 12. Portas Quânticas (Matrizes Unitárias)

As portas transformam vetores preservando a probabilidade total ($U^\dagger U = I$).

### Portas de Um Qubit

**Matrizes de Pauli:**

```math
I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}
```

**Propriedades das matrizes de Pauli:**
- São hermitianas e unitárias: $\sigma_i = \sigma_i^\dagger$, $\sigma_i^2 = I$
- Anticomutam: $\sigma_i\sigma_j = -\sigma_j\sigma_i$ para $i \neq j$
- Relação: $XYZ = iI$

**Hadamard ($H$) — Superposição:**

```math
H = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}
```

```math
H|0\rangle = |+\rangle, \quad H|1\rangle = |-\rangle
```

**Portas de Fase:**

```math
S = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}, \quad T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}, \quad R_\phi = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\phi} \end{pmatrix}
```

Note que $S = T^2$ e $Z = S^2$.

**Portas de Rotação:**

```math
R_x(\theta) = \cos\frac{\theta}{2}I - i\sin\frac{\theta}{2}X = \begin{pmatrix} \cos\frac{\theta}{2} & -i\sin\frac{\theta}{2} \\ -i\sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{pmatrix}
```

```math
R_y(\theta) = \cos\frac{\theta}{2}I - i\sin\frac{\theta}{2}Y = \begin{pmatrix} \cos\frac{\theta}{2} & -\sin\frac{\theta}{2} \\ \sin\frac{\theta}{2} & \cos\frac{\theta}{2} \end{pmatrix}
```

```math
R_z(\theta) = \cos\frac{\theta}{2}I - i\sin\frac{\theta}{2}Z = \begin{pmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{pmatrix}
```

**Decomposição universal:** qualquer porta de 1 qubit pode ser escrita como:

```math
U = e^{i\alpha} R_z(\beta) R_y(\gamma) R_z(\delta)
```

### Portas de Múltiplos Qubits

**CNOT (Controlled-NOT):**

```math
CNOT = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix} = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes X
```

```math
CNOT|00\rangle = |00\rangle, \quad CNOT|01\rangle = |01\rangle, \quad CNOT|10\rangle = |11\rangle, \quad CNOT|11\rangle = |10\rangle
```

**CZ (Controlled-Z):**

```math
CZ = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -1 \end{pmatrix} = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes Z
```

**SWAP:**

```math
SWAP = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}
```

```math
SWAP|ab\rangle = |ba\rangle
```

**Toffoli (CCNOT) — 3 qubits:**

```math
CCNOT|a, b, c\rangle = |a, b, c \oplus (a \cdot b)\rangle
```

É uma porta universal para computação clássica reversível.

### Criação de Estados de Bell

```math
|\Phi^+\rangle = CNOT \cdot (H \otimes I)|00\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}
```

---

## 13. Medição Quântica

### Medição na base computacional

Dado $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$:

| Resultado | Probabilidade | Estado após medição |
| :--- | :--- | :--- |
| 0 | $\|\alpha\|^2$ | $\|0\rangle$ |
| 1 | $\|\beta\|^2$ | $\|1\rangle$ |

### Medição projetiva geral

Operadores de projeção $\{P_m\}$ onde $\sum_m P_m = I$:

```math
\text{Prob}(m) = \langle\psi|P_m|\psi\rangle, \quad |\psi'\rangle = \frac{P_m|\psi\rangle}{\sqrt{\langle\psi|P_m|\psi\rangle}}
```

### Valor esperado de um observável

Para um observável (operador hermitiano) $A$:

```math
\langle A \rangle = \langle\psi|A|\psi\rangle = \sum_i \lambda_i |\langle v_i|\psi\rangle|^2
```

---

## 14. Matriz Densidade

Para estados mistos (incerteza clássica + quântica):

**Estado puro:**

```math
\rho = |\psi\rangle\langle\psi|
```

**Estado misto (ensemble):**

```math
\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|, \quad \sum_i p_i = 1
```

**Propriedades:**

| Propriedade | Expressão |
| :--- | :--- |
| Hermitiana | $\rho = \rho^\dagger$ |
| Traço unitário | $\text{Tr}(\rho) = 1$ |
| Positiva semi-definida | $\langle\phi\|\rho\|\phi\rangle \geq 0$ |
| Pureza | $\text{Tr}(\rho^2) = 1$ (puro), $\text{Tr}(\rho^2) < 1$ (misto) |

**Valor esperado com matriz densidade:**

```math
\langle A \rangle = \text{Tr}(\rho A)
```

**Exemplos:**

```math
\rho_{|0\rangle} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}, \quad \rho_{|+\rangle} = \frac{1}{2}\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}, \quad \rho_{\text{misto}} = \frac{I}{2} = \frac{1}{2}\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}
```

---

## 15. Operadores de Grover

Conceitos específicos para o algoritmo de busca:

**Oráculo ($U_\omega$):** Marca o estado alvo invertendo sua fase.

```math
U_\omega = I - 2|\omega\rangle\langle\omega|
```

**Difusor ($D$):** Realiza a inversão sobre a média.

```math
D = 2|s\rangle\langle s| - I, \quad \text{onde} \quad |s\rangle = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle
```

**Iteração de Grover:**

```math
G = D \cdot U_\omega
```

**Número ótimo de iterações:**

```math
k \approx \frac{\pi}{4}\sqrt{N}
```

onde $N = 2^n$ é o tamanho do espaço de busca.

---

## 16. Transformada Quântica de Fourier (QFT)

A QFT mapeia a base computacional para a base de Fourier:

```math
QFT|j\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} e^{2\pi ijk/N}|k\rangle
```

**Matriz para 2 qubits ($N=4$):**

```math
QFT_4 = \frac{1}{2} \begin{pmatrix} 1 & 1 & 1 & 1 \\ 1 & i & -1 & -i \\ 1 & -1 & 1 & -1 \\ 1 & -i & -1 & i \end{pmatrix}
```

A QFT é essencial nos algoritmos de Shor (fatoração) e estimativa de fase.

---

## 17. Identidades e Propriedades Úteis

### Relações fundamentais

| Propriedade | Expressão |
| :--- | :--- |
| Normalização | $\langle\psi\|\psi\rangle = 1$ |
| Ortogonalidade | $\langle 0\|1\rangle = 0$ |
| Completeza | $\|0\rangle\langle 0\| + \|1\rangle\langle 1\| = I$ |
| Unitariedade | $UU^\dagger = U^\dagger U = I$ |
| Adjunto de produto | $(AB)^\dagger = B^\dagger A^\dagger$ |
| Adjunto de tensor | $(A \otimes B)^\dagger = A^\dagger \otimes B^\dagger$ |
| Traço cíclico | $\text{Tr}(ABC) = \text{Tr}(CAB) = \text{Tr}(BCA)$ |

### Identidades com Hadamard

```math
HXH = Z, \quad HZH = X, \quad HYH = -Y
```

```math
H = \frac{X + Z}{\sqrt{2}}
```

### Identidades com CNOT

```math
CNOT \cdot (I \otimes H) \cdot CNOT = \text{SWAP parcial (troca na base X)}
```

### Comutadores e Anticomutadores

```math
[A, B] = AB - BA \quad \text{(comutador)}
```

```math
\{A, B\} = AB + BA \quad \text{(anticomutador)}
```

Para as matrizes de Pauli: $[\sigma_i, \sigma_j] = 2i\epsilon_{ijk}\sigma_k$.

---

## 18. Complexidade e Dimensões — Referência Rápida

| Qubits ($n$) | Dimensão ($2^n$) | Nº de amplitudes | Tamanho da matriz unitária |
| :--- | :--- | :--- | :--- |
| 1 | 2 | 2 | $2 \times 2$ |
| 2 | 4 | 4 | $4 \times 4$ |
| 3 | 8 | 8 | $8 \times 8$ |
| 5 | 32 | 32 | $32 \times 32$ |
| 10 | 1.024 | 1.024 | $1024 \times 1024$ |
| 20 | ~1M | ~1M | ~$10^6 \times 10^6$ |
| 50 | ~$10^{15}$ | ~$10^{15}$ | Intratável classicamente |

---

## 19. Mapa de Conceitos

```
Números Complexos
    └── Espaço de Hilbert (ℂ^2ⁿ)
          ├── Notação de Dirac (Bra-Ket)
          │     ├── Produto Interno → Probabilidade
          │     ├── Produto Externo → Operadores
          │     └── Produto Tensorial → Múltiplos Qubits
          ├── Estados
          │     ├── Bases (Z, X, Y)
          │     ├── Superposição
          │     ├── Emaranhamento (Bell)
          │     └── Esfera de Bloch
          ├── Operadores
          │     ├── Matrizes de Pauli (X, Y, Z)
          │     ├── Hadamard, S, T
          │     ├── Rotações (Rx, Ry, Rz)
          │     ├── CNOT, CZ, SWAP, Toffoli
          │     └── Autovalores / Decomposição Espectral
          ├── Medição
          │     ├── Projetiva
          │     ├── Valor Esperado
          │     └── Matriz Densidade
          └── Algoritmos
                ├── Grover (Oráculo + Difusor)
                └── QFT (Transformada de Fourier)
```
