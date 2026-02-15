# Criptografia Pós-Quântica: Fundamentos e Implementações

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-green)
![NIST](https://img.shields.io/badge/Padrão-FIPS%20203%20%7C%20FIPS%20204-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)

## Sobre o Projeto

Este repositório explora a **Criptografia Pós-Quântica (PQC)**, um campo essencial para garantir a segurança da informação na era dos computadores quânticos. O projeto inclui implementações educacionais, benchmarks comparativos e análises de segurança dos novos padrões NIST.

---

## A Ameaça Quântica

### Por que precisamos de nova criptografia?

Os algoritmos criptográficos clássicos que protegem a internet hoje (RSA, ECDSA, Diffie-Hellman) baseiam-se em dois problemas matemáticos considerados computacionalmente difíceis: a **fatoração de inteiros** e o **logaritmo discreto**. 

Em 1994, Peter Shor demonstrou que um computador quântico suficientemente poderoso poderia resolver ambos os problemas em tempo polinomial, quebrando efetivamente toda a criptografia de chave pública atual.

### Algoritmo de Shor

O algoritmo de Shor utiliza a **Transformada Quântica de Fourier** para encontrar o período de funções modulares, permitindo:

| Problema | Complexidade Clássica | Complexidade Quântica (Shor) |
|----------|----------------------|------------------------------|
| Fatoração de $n$ bits | $O(\exp(n^{1/3}))$ | $O(n^3)$ |
| Logaritmo Discreto | $O(\exp(n^{1/2}))$ | $O(n^3)$ |

**Implicação prática:** Uma chave RSA-2048 que levaria bilhões de anos para ser quebrada classicamente poderia ser comprometida em horas por um computador quântico com ~4.000 qubits lógicos estáveis.

### Linha do Tempo da Ameaça

```
2024 ─────── Computadores quânticos com ~1.000 qubits (NISQ)
     │
2030 ─────── Previsão: Primeiros sistemas com correção de erro útil
     │
2035 ─────── Previsão: "Q-Day" - Quebra de RSA-2048 possível
     │
Hoje ─────── "Harvest Now, Decrypt Later" - Dados interceptados
             hoje podem ser descriptografados no futuro
```

---

## Padrões NIST de Criptografia Pós-Quântica

Em agosto de 2024, o NIST publicou os primeiros padrões de criptografia pós-quântica após 8 anos de competição e análise:

### FIPS 203: ML-KEM (Module-Lattice-Based Key-Encapsulation Mechanism)

Anteriormente conhecido como CRYSTALS-Kyber, o ML-KEM é o padrão para **encapsulamento de chaves** (substituindo troca de chaves Diffie-Hellman e RSA-KEM).

**Base matemática:** Problema Module Learning With Errors (MLWE)

$$\mathbf{A} \cdot \mathbf{s} + \mathbf{e} = \mathbf{t} \pmod{q}$$

onde $\mathbf{A}$ é uma matriz pública, $\mathbf{s}$ é o segredo, e $\mathbf{e}$ é um pequeno vetor de erro.

| Variante | Nível de Segurança | Chave Pública | Chave Privada | Ciphertext |
|----------|-------------------|---------------|---------------|------------|
| ML-KEM-512 | NIST Nível 1 (AES-128) | 800 bytes | 1.632 bytes | 768 bytes |
| ML-KEM-768 | NIST Nível 3 (AES-192) | 1.184 bytes | 2.400 bytes | 1.088 bytes |
| ML-KEM-1024 | NIST Nível 5 (AES-256) | 1.568 bytes | 3.168 bytes | 1.568 bytes |

### FIPS 204: ML-DSA (Module-Lattice-Based Digital Signature Algorithm)

Anteriormente CRYSTALS-Dilithium, o ML-DSA é o padrão principal para **assinaturas digitais**.

**Base matemática:** Problema Module Short Integer Solution (MSIS) combinado com MLWE

| Variante | Nível de Segurança | Chave Pública | Chave Privada | Assinatura |
|----------|-------------------|---------------|---------------|------------|
| ML-DSA-44 | NIST Nível 2 | 1.312 bytes | 2.528 bytes | 2.420 bytes |
| ML-DSA-65 | NIST Nível 3 | 1.952 bytes | 4.000 bytes | 3.309 bytes |
| ML-DSA-87 | NIST Nível 5 | 2.592 bytes | 4.896 bytes | 4.627 bytes |

### FIPS 205: SLH-DSA (Stateless Hash-Based Digital Signature Algorithm)

Anteriormente SPHINCS+, oferece assinaturas baseadas apenas em funções hash (segurança mais conservadora).

---

## Problemas Matemáticos Subjacentes

### Reticulados (Lattices)

Um reticulado $\mathcal{L}$ em $\mathbb{R}^n$ é o conjunto de todas as combinações lineares inteiras de vetores base $\mathbf{b}_1, \ldots, \mathbf{b}_n$:

$$\mathcal{L} = \left\{ \sum_{i=1}^{n} z_i \mathbf{b}_i : z_i \in \mathbb{Z} \right\}$$

**Problemas difíceis em reticulados:**

1. **Shortest Vector Problem (SVP):** Encontrar o vetor não-nulo mais curto no reticulado.

2. **Closest Vector Problem (CVP):** Dado um ponto alvo, encontrar o vetor do reticulado mais próximo.

3. **Learning With Errors (LWE):** Distinguir amostras $(\mathbf{a}_i, \langle \mathbf{a}_i, \mathbf{s} \rangle + e_i)$ de amostras uniformemente aleatórias.

Estes problemas são considerados difíceis mesmo para computadores quânticos, com os melhores algoritmos conhecidos tendo complexidade exponencial.

### Por que reticulados são seguros contra computadores quânticos?

O algoritmo de Grover oferece apenas speedup quadrático para buscas não estruturadas, insuficiente para quebrar a segurança dos reticulados se os parâmetros forem escolhidos adequadamente. Não se conhece nenhum algoritmo quântico que ofereça vantagem significativa contra problemas de reticulados.

---

## Estrutura do Repositório

```
pos-quantica/
├── README.md
├── requirements.txt
├── mlkem_side_channel_test.py    # Testes de resistência a side-channel
├── benchmark_classico_vs_pq.py   # Benchmark comparativo de performance
├── comparar_tamanhos.py          # Análise de tamanhos de chaves/assinaturas
├── examples/
│   ├── basic_mlkem.py            # Exemplo básico de uso do ML-KEM
│   ├── basic_mldsa.py            # Exemplo básico de uso do ML-DSA
│   └── hybrid_tls.py             # Exemplo de implementação híbrida
└── output/
    ├── timing_analysis.png
    ├── dashboard_performance.png
    └── reports/
```

---

## Scripts Disponíveis

### 1. Teste de Resistência a Side-Channel (`mlkem_side_channel_test.py`)

Implementação educacional do ML-KEM com contramedidas contra ataques de canal lateral.

**Funcionalidades:**
- Operações em tempo constante (constant-time)
- Masking algébrico contra DPA/CPA
- Randomização de execução
- Análise estatística de timing

**Execução:**
```bash
# Instalação de dependências
pip install numpy scipy matplotlib

# Execução padrão
python mlkem_side_channel_test.py

# Para maior precisão de timing (Linux)
sudo nice -n -20 python mlkem_side_channel_test.py
```

**Saída esperada:**
- Gráficos de distribuição de timing em `output/`
- Relatórios detalhados com análise estatística
- Comparação entre implementação segura e vulnerável

### 2. Benchmark Comparativo (`benchmark_classico_vs_pq.py`)

Compara performance entre algoritmos clássicos (RSA, ECDSA) e pós-quânticos (ML-DSA).

**Métricas avaliadas:**
- Tempo de geração de chaves
- Tempo de assinatura
- Tempo de verificação
- Coeficiente de variação (consistência)

**Execução:**
```bash
pip install pandas seaborn matplotlib cryptography

python benchmark_classico_vs_pq.py
```

### 3. Análise de Tamanhos (`comparar_tamanhos.py`)

Analisa e visualiza o impacto dos tamanhos maiores de chaves e assinaturas pós-quânticas.

**Análises incluídas:**
- Comparação visual de tamanhos
- Impacto em bandwidth de rede
- Projeções para cenários reais (TLS handshakes, assinaturas em massa)

**Execução:**
```bash
pip install matplotlib cryptography

# Opcional: para algoritmos pós-quânticos reais
pip install liboqs

python comparar_tamanhos.py
```

---

## Comparativo: Clássico vs Pós-Quântico

### Tamanhos de Chaves Públicas

| Algoritmo | Tipo | Tamanho | Comparação com ECDSA P-256 |
|-----------|------|---------|---------------------------|
| ECDSA P-256 | Clássico | 91 bytes | 1x (baseline) |
| RSA-2048 | Clássico | 294 bytes | 3,2x |
| ML-KEM-512 | Pós-Quântico | 800 bytes | 8,8x |
| ML-KEM-768 | Pós-Quântico | 1.184 bytes | 13x |
| ML-DSA-44 | Pós-Quântico | 1.312 bytes | 14,4x |
| ML-DSA-65 | Pós-Quântico | 1.952 bytes | 21,5x |

### Tamanhos de Assinaturas

| Algoritmo | Tamanho | Comparação com ECDSA |
|-----------|---------|---------------------|
| ECDSA P-256 | ~64 bytes | 1x (baseline) |
| RSA-2048 | 256 bytes | 4x |
| ML-DSA-44 | 2.420 bytes | 38x |
| ML-DSA-65 | 3.309 bytes | 52x |
| ML-DSA-87 | 4.627 bytes | 72x |

### Performance Típica

| Operação | RSA-2048 | ECDSA P-256 | ML-DSA-44 | ML-KEM-768 |
|----------|----------|-------------|-----------|------------|
| Geração de Chaves | ~50ms | ~0,5ms | ~0,1ms | ~0,05ms |
| Assinatura/Encaps | ~1ms | ~0,3ms | ~0,5ms | ~0,05ms |
| Verificação/Decaps | ~0,05ms | ~0,5ms | ~0,3ms | ~0,05ms |

---

## Ataques de Canal Lateral (Side-Channel)

### Tipos de Ataques

1. **Timing Attacks:** Exploram variações no tempo de execução dependentes dos dados secretos.

2. **Power Analysis (SPA/DPA):** Analisam consumo de energia durante operações criptográficas.

3. **Electromagnetic Analysis:** Capturam emanações eletromagnéticas do dispositivo.

4. **Cache Attacks:** Exploram padrões de acesso à cache do processador.

### Contramedidas Implementadas

**Operações em Tempo Constante:**
```python
def constant_time_select(condition: int, a: int, b: int) -> int:
    """Retorna a se condition != 0, senão b, sem branches"""
    mask = -(condition & 1)  # 0 ou 0xFFFFFFFF
    return (mask & a) | (~mask & b)
```

**Comparação em Tempo Constante:**
```python
def constant_time_compare(a: bytes, b: bytes) -> bool:
    """Compara sem vazamento de timing"""
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0
```

**Masking Algébrico:**
```python
# Valor real: v
# Valor mascarado: v_masked = (v + r) mod q
# Máscara: r (valor aleatório)
# Operações são realizadas em valores mascarados
```

---

## Estratégias de Migração

### Abordagem Híbrida (Recomendada para Transição)

Combina algoritmos clássicos e pós-quânticos para garantir segurança mesmo se um deles for comprometido:

```
Chave_Híbrida = KDF(Chave_ECDH || Chave_ML-KEM)
```

**Vantagens:**
- Segurança garantida pelo algoritmo mais forte
- Compatibilidade com sistemas legados
- Proteção contra descobertas criptanalíticas futuras

### Cronograma Sugerido de Migração

| Fase | Período | Ações |
|------|---------|-------|
| Inventário | 2024-2025 | Mapear todos os usos de criptografia assimétrica |
| Planejamento | 2025-2026 | Definir estratégia híbrida, atualizar bibliotecas |
| Implementação | 2026-2028 | Deploy gradual começando por sistemas críticos |
| Transição | 2028-2030 | Migração completa para PQC puro |
| Deprecação | 2030+ | Remoção de algoritmos clássicos vulneráveis |

---

## Instalação e Configuração

### Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Básica

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/pos-quantica.git
cd pos-quantica

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### Instalação com liboqs (Algoritmos Reais)

```bash
# Ubuntu/Debian
sudo apt-get install cmake ninja-build libssl-dev

# Instalar liboqs
git clone https://github.com/open-quantum-safe/liboqs.git
cd liboqs && mkdir build && cd build
cmake -GNinja ..
ninja && sudo ninja install

# Instalar wrapper Python
pip install liboqs-python
```

### Arquivo requirements.txt

```
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
seaborn>=0.11.0
pandas>=1.3.0
cryptography>=3.4.0
# liboqs  # Opcional, requer compilação nativa
```

---

## Casos de Uso Práticos

### Comunicações Seguras (TLS 1.3 Híbrido)

O TLS 1.3 já suporta extensões para algoritmos pós-quânticos. Navegadores como Chrome e Firefox estão experimentando com ML-KEM híbrido.

### Assinaturas de Software

Atualizações de firmware e software precisam de assinaturas que permaneçam seguras por décadas. ML-DSA-65 é recomendado para este caso.

### Infraestrutura de Chaves Públicas (PKI)

Certificados X.509 com chaves pós-quânticas estão em desenvolvimento. O tamanho maior das chaves impacta o design de cadeias de certificados.

### IoT e Sistemas Embarcados

Para dispositivos com recursos limitados, ML-KEM-512 e ML-DSA-44 oferecem o melhor balanço entre segurança e eficiência.

---

## Referências

### Padrões NIST

- [FIPS 203: ML-KEM](https://csrc.nist.gov/publications/detail/fips/203/final)
- [FIPS 204: ML-DSA](https://csrc.nist.gov/publications/detail/fips/204/final)
- [FIPS 205: SLH-DSA](https://csrc.nist.gov/publications/detail/fips/205/final)

### Artigos Fundamentais

- Shor, P. "Algorithms for Quantum Computation: Discrete Logarithms and Factoring." FOCS 1994.
- Regev, O. "On Lattices, Learning with Errors, and Cryptography." STOC 2005.
- Ajtai, M. "Generating Hard Instances of Lattice Problems." STOC 1996.

### Implementações de Referência

- [liboqs (Open Quantum Safe)](https://github.com/open-quantum-safe/liboqs)
- [PQClean](https://github.com/PQClean/PQClean)
- [CRYSTALS-Kyber](https://pq-crystals.org/kyber/)
- [CRYSTALS-Dilithium](https://pq-crystals.org/dilithium/)

---

## Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue para discussão antes de enviar um pull request.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Aviso:** Este repositório contém implementações educacionais. Para uso em produção, utilize bibliotecas certificadas e auditadas como liboqs ou implementações de fornecedores confiáveis.
