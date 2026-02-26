graph TD
    %% ============ PROBLEMA ============
    TSP["🏙️ <b>PROBLEMA: TSP</b><br/>Encontrar rota de menor custo<br/>que visita N cidades uma vez<br/><i>NP-difícil, cresce com N!</i>"]

    %% ============ PASSO 1 ============
    subgraph P1["PASSO 1 — Formulação"]
        FB["<b>Força Bruta</b><br/>Enumera todas N! rotas<br/>Custo ótimo = referência"]
        VARS["<b>Variáveis Binárias</b><br/>x_{i,t} ∈ {0,1}<br/>cidade i no passo t"]
    end

    %% ============ PASSO 2 ============
    subgraph P2["PASSO 2 — Hamiltoniano"]
        QUBO["<b>Formulação QUBO</b><br/>H_QUBO = H_custo + H_p1 + H_p2"]
        HC["<b>H_custo</b><br/>Σ d_{ij} · x_{i,t} · x_{j,t+1}<br/><i>distâncias da rota</i>"]
        HP1["<b>H_p1</b><br/>A·Σ(Σ x_{i,t} - 1)²<br/><i>cada cidade 1 vez</i>"]
        HP2["<b>H_p2</b><br/>A·Σ(Σ x_{i,t} - 1)²<br/><i>cada passo 1 cidade</i>"]
        ISING["<b>Hamiltoniano Ising</b><br/>x_i → (I - σ_z)/2<br/>Matriz 2^(n²) × 2^(n²)"]
    end

    %% ============ PASSO 3 ============
    subgraph P3["PASSO 3 — Evolução Adiabática"]
        H0["<b>H₀ (inicial)</b><br/>-Σ σ_x^(i)<br/>Estado fundamental: |+⟩^⊗n"]
        HF["<b>H_f (final)</b><br/>= H_QUBO (Ising)<br/>Estado fundamental: rota ótima"]
        INTERP["<b>Interpolação</b><br/>H(s) = (1-s)·H₀ + s·H_f<br/>s = t/T ∈ [0,1]"]
        ESPECTRO["<b>Espectro E_k(s)</b><br/>Diagonalização de H(s)<br/>para cada valor de s"]
        GAP["<b>Lacuna Espectral</b><br/>Δ(s) = E₁(s) - E₀(s)<br/>Δ_min determina dificuldade"]
        TEOREMA["<b>Teorema Adiabático</b><br/>T >> 1/Δ_min²<br/>garante permanência<br/>no fundamental"]
    end

    %% ============ PASSO 4 ============
    subgraph P4["PASSO 4 — Simulação"]
        SCHROD["<b>Eq. Schrödinger</b><br/>i·d|ψ⟩/dt = H(t)|ψ⟩<br/>solve_ivp (RK45)"]
        PSIT["<b>|ψ(t)⟩</b><br/>Estado quântico<br/>ao longo do tempo"]
        P0T["<b>P₀(t)</b><br/>|⟨fundamental(s)|ψ(t)⟩|²<br/>prob. no estado fundamental"]
        DWAVE["<b>D-Wave Ocean SDK</b><br/>ExactSolver: solução exata<br/>SimulatedAnnealing: amostragem"]
        PFINAL["<b>P_final</b><br/>Prob. de sucesso<br/>no final da evolução"]
    end

    %% ============ PASSO 5 ============
    subgraph P5["PASSO 5 — Processamento de Sinais"]
        FFT["<b>FFT de P₀(t)</b><br/>Frequências dominantes ω<br/>Parseval: energia conservada"]
        RELACAO["<b>Relação ΔE = ℏω</b><br/>Picos da FFT ↔ lacunas<br/>de energia de H_f"]
        STFT["<b>Espectrograma (STFT)</b><br/>Como as frequências<br/>mudam com s(t)"]
        QSP["<b>QSP (código professor)</b><br/>Processamento quântico<br/>de sinais via rotações<br/>unitárias SU(2)"]
        NORMA["<b>Conservação da Norma</b><br/>||ψ'||² = ||ψ||² = 1<br/>↔ Teorema de Parseval"]
    end

    %% ============ PASSO 6 ============
    subgraph P6["PASSO 6 — Avaliação"]
        COMP["<b>Comparação</b><br/>Clássico vs Adiabático<br/>vs D-Wave"]
        LIMIT["<b>Limitações</b><br/>Escalabilidade, Δ_min,<br/>ruído, parâmetro A"]
        PERSP["<b>Perspectivas</b><br/>Correção de erros,<br/>schedules não-lineares"]
    end

    %% ============ CONEXÕES ============
    
    %% Fluxo principal
    TSP --> P1
    TSP --> VARS
    VARS --> QUBO
    FB -.->|"referência<br/>para validação"| COMP

    %% Passo 2 interno
    HC --> QUBO
    HP1 --> QUBO
    HP2 --> QUBO
    QUBO --> ISING

    %% Passo 2 → 3
    ISING --> HF
    H0 --> INTERP
    HF --> INTERP
    INTERP --> ESPECTRO
    ESPECTRO --> GAP
    GAP --> TEOREMA

    %% Passo 3 → 4
    INTERP --> SCHROD
    TEOREMA -.->|"define T mínimo"| SCHROD
    SCHROD --> PSIT
    PSIT --> P0T
    P0T --> PFINAL
    QUBO -->|"BQM"| DWAVE

    %% Passo 4 → 5
    P0T -->|"sinal temporal"| FFT
    P0T --> STFT
    FFT --> RELACAO
    GAP -.->|"validação:<br/>ω = ΔE/ℏ?"| RELACAO
    NORMA -.->|"fundamenta"| FFT
    NORMA -.->|"fundamenta"| QSP

    %% Passo 5 → 6
    RELACAO --> COMP
    PFINAL --> COMP
    DWAVE --> COMP
    GAP --> LIMIT
    COMP --> PERSP

    %% ============ ESTILO ============
    classDef problema fill:#ff6b6b,stroke:#c0392b,color:#fff,font-weight:bold
    classDef passo1 fill:#74b9ff,stroke:#2980b9,color:#000
    classDef passo2 fill:#a29bfe,stroke:#6c5ce7,color:#000
    classDef passo3 fill:#55efc4,stroke:#00b894,color:#000
    classDef passo4 fill:#ffeaa7,stroke:#fdcb6e,color:#000
    classDef passo5 fill:#fd79a8,stroke:#e84393,color:#fff
    classDef passo6 fill:#dfe6e9,stroke:#636e72,color:#000

    class TSP problema
    class FB,VARS passo1
    class QUBO,HC,HP1,HP2,ISING passo2
    class H0,HF,INTERP,ESPECTRO,GAP,TEOREMA passo3
    class SCHROD,PSIT,P0T,DWAVE,PFINAL passo4
    class FFT,RELACAO,STFT,QSP,NORMA passo5
    class COMP,LIMIT,PERSP passo6
