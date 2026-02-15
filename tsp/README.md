# O Problema do Caixeiro Viajante (TSP) e a Computação Quântica

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-green)
![Tópico](https://img.shields.io/badge/Tópico-Otimização%20Combinatória-blue)
![Tópico](https://img.shields.io/badge/Tópico-Computação%20Quântica-purple)

## Sobre o Projeto

Este repositório é dedicado ao estudo do **Problema do Caixeiro Viajante (TSP)**, explorando desde as resoluções clássicas tradicionais até as novas fronteiras oferecidas pela **Computação Quântica**. O objetivo central é entender as limitações da computação clássica em problemas de otimização combinatória e investigar como algoritmos quânticos podem oferecer vantagens no futuro.

---

## O Problema: O que é o TSP?

O Problema do Caixeiro Viajante pode ser formulado da seguinte maneira:

> *"Dada uma lista de cidades e as distâncias entre cada par delas, qual é a rota mais curta possível que visita cada cidade exatamente uma vez e retorna à cidade de origem?"*

Matematicamente, o TSP é modelado como a busca pelo **ciclo hamiltoniano de menor custo** em um grafo ponderado e completo. Apesar de sua premissa simples, encontrar a solução ótima se torna computacionalmente inviável à medida que o número de cidades cresce.

### Formulação Matemática

Dado um grafo completo $G = (V, E)$ com $n$ vértices (cidades) e uma matriz de distâncias $d_{ij}$ representando o custo de ir da cidade $i$ para a cidade $j$, o objetivo é minimizar:

$$\min \sum_{i=1}^{n} \sum_{j=1}^{n} d_{ij} \cdot x_{ij}$$

Sujeito às restrições:
- Cada cidade é visitada exatamente uma vez
- Cada cidade é deixada exatamente uma vez  
- Não há subciclos (restrições de eliminação de subtour)

---

## Abordagens Clássicas

A computação clássica ataca o TSP de duas maneiras principais: buscando a solução ótima garantida (métodos exatos) ou buscando eficiência computacional (heurísticas e metaheurísticas).

### 1. Métodos Exatos

Estes algoritmos garantem encontrar a rota absolutamente mais curta, mas sofrem com tempo de execução exponencial.

#### Força Bruta (Enumeração Completa)

O método mais simples e intuitivo: gerar todas as permutações possíveis de rotas, calcular o custo de cada uma e selecionar a menor.

| Característica | Valor |
|----------------|-------|
| **Complexidade de Tempo** | $O(n!)$ |
| **Complexidade de Espaço** | $O(n)$ |
| **Garantia de Otimalidade** | Sim |
| **Viabilidade Prática** | Apenas para $n \leq 10$ |

**Pseudocódigo:**
```
função força_bruta(cidades, distâncias):
    melhor_rota = nula
    menor_custo = infinito
    
    para cada permutação P de cidades:
        custo = calcular_custo(P, distâncias)
        se custo < menor_custo:
            menor_custo = custo
            melhor_rota = P
    
    retornar melhor_rota, menor_custo
```

#### Programação Dinâmica (Algoritmo de Held-Karp)

Proposto independentemente por Bellman e por Held & Karp em 1962, este algoritmo usa o princípio da otimalidade de Bellman para evitar recálculos redundantes através de memoização.

A ideia central é: para cada subconjunto $S$ de cidades e cada cidade final $j \in S$, armazenamos o custo mínimo de um caminho que parte da cidade inicial, visita todas as cidades em $S$ e termina em $j$.

| Característica | Valor |
|----------------|-------|
| **Complexidade de Tempo** | $O(n^2 \cdot 2^n)$ |
| **Complexidade de Espaço** | $O(n \cdot 2^n)$ |
| **Garantia de Otimalidade** | Sim |
| **Viabilidade Prática** | Até $n \approx 25$ |

**Recorrência:**

$$C(S, j) = \min_{i \in S, i \neq j} \left[ C(S \setminus \{j\}, i) + d_{ij} \right]$$

onde $C(S, j)$ é o custo mínimo para visitar todas as cidades em $S$ terminando em $j$.

#### Branch and Bound (Ramificar e Limitar)

Este método explora sistematicamente a árvore de soluções, usando limites inferiores para "podar" ramos que não podem conter a solução ótima.

**Componentes principais:**
- **Ramificação (Branching):** Divide o problema em subproblemas menores
- **Limitação (Bounding):** Calcula limites inferiores para cada subproblema
- **Poda (Pruning):** Descarta subproblemas cujo limite inferior excede a melhor solução conhecida

| Característica | Valor |
|----------------|-------|
| **Complexidade de Tempo** | $O(n!)$ no pior caso, mas muito melhor na prática |
| **Complexidade de Espaço** | $O(n^2)$ a $O(2^n)$ dependendo da implementação |
| **Garantia de Otimalidade** | Sim |
| **Viabilidade Prática** | Até $n \approx 40-60$ com boas heurísticas |

**Técnicas de cálculo de limite inferior:**
- Relaxação da Árvore Geradora Mínima (MST)
- Relaxação de Programação Linear
- 1-tree relaxation

#### Programação Linear Inteira (ILP)

O TSP pode ser formulado como um problema de programação linear inteira, permitindo o uso de solvers comerciais poderosos como CPLEX, Gurobi ou SCIP.

**Formulação de Dantzig-Fulkerson-Johnson (DFJ):**

$$\min \sum_{i < j} d_{ij} \cdot x_{ij}$$

Sujeito a:
- $\sum_{j \neq i} x_{ij} = 2$ para todo $i$ (cada cidade tem grau 2)
- $\sum_{i,j \in S} x_{ij} \leq |S| - 1$ para todo $S \subset V$ (eliminação de subtours)
- $x_{ij} \in \{0, 1\}$

---

### 2. Métodos Heurísticos (Algoritmos Construtivos)

Quando a solução exata é inviável, heurísticas constroem rapidamente soluções "boas o suficiente".

#### Vizinho Mais Próximo (Nearest Neighbor)

O algoritmo guloso mais simples: sempre ir para a cidade não visitada mais próxima.

| Característica | Valor |
|----------------|-------|
| **Complexidade de Tempo** | $O(n^2)$ |
| **Qualidade da Solução** | Tipicamente 20-25% acima do ótimo |
| **Garantia de Aproximação** | $O(\log n)$ do ótimo |

```
função vizinho_mais_proximo(cidade_inicial, distâncias):
    rota = [cidade_inicial]
    não_visitadas = todas_cidades - {cidade_inicial}
    
    enquanto não_visitadas não vazio:
        atual = último elemento de rota
        próxima = cidade em não_visitadas mais próxima de atual
        adicionar próxima a rota
        remover próxima de não_visitadas
    
    retornar rota
```

#### Inserção Mais Barata (Cheapest Insertion)

Constrói a rota incrementalmente, sempre inserindo a próxima cidade na posição que causa o menor aumento no custo total.

| Característica | Valor |
|----------------|-------|
| **Complexidade de Tempo** | $O(n^2)$ a $O(n^3)$ |
| **Qualidade da Solução** | Geralmente melhor que Vizinho Mais Próximo |

#### Algoritmo de Christofides (1976)

O melhor algoritmo de aproximação conhecido para TSP métrico, com garantia de estar no máximo 50% acima do ótimo.

**Passos:**
1. Construir a Árvore Geradora Mínima (MST)
2. Encontrar vértices de grau ímpar na MST
3. Encontrar o matching perfeito de peso mínimo entre vértices ímpares
4. Combinar MST e matching para formar um grafo Euleriano
5. Encontrar o circuito Euleriano
6. Converter em circuito Hamiltoniano (atalhos)

| Característica | Valor |
|----------------|-------|
| **Complexidade de Tempo** | $O(n^3)$ |
| **Garantia de Aproximação** | $\frac{3}{2}$ do ótimo (para TSP métrico) |

---

### 3. Metaheurísticas (Busca Local e Otimização Global)

Algoritmos que escapam de ótimos locais através de estratégias inteligentes de exploração.

#### 2-opt e 3-opt

Melhorias iterativas que removem e reconectam arestas da rota.

**2-opt:** Remove 2 arestas e reconecta de forma cruzada. Se a nova rota é melhor, mantém a mudança.

| Característica | Valor |
|----------------|-------|
| **Complexidade por iteração** | $O(n^2)$ |
| **Complexidade até convergência** | $O(n^2)$ a $O(n^3)$ iterações |

#### Lin-Kernighan

Uma das heurísticas mais eficazes para o TSP, generalizando k-opt com k variável.

| Característica | Valor |
|----------------|-------|
| **Qualidade** | Frequentemente encontra soluções ótimas ou muito próximas |
| **Implementação de Referência** | LKH (Lin-Kernighan-Helsgaun) |

#### Simulated Annealing (Recozimento Simulado)

Inspirado no processo metalúrgico de recozimento, aceita movimentos que pioram a solução com probabilidade decrescente.

$$P(\text{aceitar}) = \exp\left(-\frac{\Delta E}{T}\right)$$

onde $\Delta E$ é a diferença de custo e $T$ é a "temperatura" que decresce ao longo do tempo.

#### Algoritmos Genéticos

Mantém uma população de soluções que evolui através de:
- **Seleção:** Soluções melhores têm maior chance de reprodução
- **Crossover:** Combina partes de duas rotas "pais"
- **Mutação:** Pequenas alterações aleatórias (ex: trocar duas cidades)

#### Otimização por Colônia de Formigas (ACO)

Formigas artificiais constroem rotas depositando "feromônio" em arestas boas, guiando futuras formigas.

---

## Limitações da Computação Clássica

O principal gargalo das abordagens clássicas é a **Complexidade Computacional**. O TSP é classificado como um problema **NP-Difícil**.

### Crescimento Fatorial

Para $n$ cidades, o número de rotas possíveis em uma abordagem de força bruta é:

$$\frac{(n-1)!}{2}$$

| Cidades | Rotas Possíveis | Tempo (1 bilhão de rotas/seg) |
|---------|-----------------|-------------------------------|
| 10 | 181.440 | < 1 ms |
| 15 | 43.589.145.600 | ~44 segundos |
| 20 | 6,08 × 10¹⁶ | ~1.930 anos |
| 25 | 3,10 × 10²³ | ~9,8 bilhões de anos |

Mesmo usando Programação Dinâmica com complexidade $O(n^2 \cdot 2^n)$, computadores clássicos eventualmente atingem limites intransponíveis. É aqui que precisamos de um novo paradigma.

---

## Abordagem Quântica

A Computação Quântica não calcula todas as rotas simultaneamente de forma "mágica", mas usa princípios como **Superposição** e **Emaranhamento Quântico** para explorar o espaço de soluções de maneira fundamentalmente diferente.

### Quantum Approximate Optimization Algorithm (QAOA)

Algoritmo híbrido clássico-quântico que utiliza portas quânticas parametrizadas para encontrar soluções aproximadas. Especialmente adequado para computadores NISQ (Noisy Intermediate-Scale Quantum).

### Variational Quantum Eigensolver (VQE)

Formula o TSP como um problema de encontrar o estado fundamental de um Hamiltoniano, usando circuitos quânticos variacionais otimizados classicamente.

### Quantum Annealing

Disponível em processadores como os da D-Wave. O TSP é formulado como um problema QUBO (Quadratic Unconstrained Binary Optimization), e o sistema físico naturalmente evolui para estados de menor energia.

### Algoritmo de Grover

Oferece speedup quadrático ($O(\sqrt{N})$ vs $O(N)$) para buscas não estruturadas, potencialmente aplicável a verificação de soluções.

---

## Comparativo: Clássico vs Quântico

| Aspecto | Clássico | Quântico |
|---------|----------|----------|
| **Estado Atual** | Maduro, prático | Em desenvolvimento |
| **Melhor Exato** | $O(n^2 \cdot 2^n)$ | Potencial para melhorias |
| **Hardware** | Amplamente disponível | Limitado (NISQ) |
| **Instâncias Resolvidas** | Até ~90.000 cidades | ~20 cidades (demonstrações) |
| **Vantagem Esperada** | - | Speedup polinomial ou exponencial |

---

## Ferramentas e Bibliotecas

**Computação Clássica:**
- [NetworkX](https://networkx.org/) - Modelagem de grafos em Python
- [OR-Tools](https://developers.google.com/optimization) - Solver de otimização do Google
- [Concorde TSP Solver](http://www.math.uwaterloo.ca/tsp/concorde.html) - Solver exato estado-da-arte

**Computação Quântica:**
- [Qiskit](https://qiskit.org/) - Framework quântico da IBM
- [D-Wave Ocean](https://docs.ocean.dwavesys.com/) - SDK para quantum annealing
- [PennyLane](https://pennylane.ai/) - Diferenciação automática para circuitos quânticos

---

## Como Executar

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/tsp-quantum.git
cd tsp-quantum

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar exemplos
python examples/classical_tsp.py
python examples/qaoa_tsp.py
```

---

## Referências

- Applegate, D. L., et al. *The Traveling Salesman Problem: A Computational Study*. Princeton University Press, 2006.
- Held, M., & Karp, R. M. "A dynamic programming approach to sequencing problems." *Journal of SIAM*, 1962.
- Christofides, N. "Worst-case analysis of a new heuristic for the travelling salesman problem." Technical Report, 1976.
- Farhi, E., et al. "A Quantum Approximate Optimization Algorithm." *arXiv:1411.4028*, 2014.

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
