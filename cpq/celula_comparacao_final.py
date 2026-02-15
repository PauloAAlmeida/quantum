# =============================================================================
# CÉLULA PARA ADICIONAR NO FINAL DO NOTEBOOK
# Comparação Sistemática: Brute Force vs QAOA
# =============================================================================

import pandas as pd
import time

# Matrizes de distâncias para teste
graphs = {
    3: np.array([
        [0, 10, 15],
        [10, 0, 20],
        [15, 20, 0]
    ], dtype=float),
    
    4: np.array([
        [0, 1, 50, 50],
        [1, 0, 2, 50],
        [50, 2, 0, 3],
        [50, 50, 3, 0]
    ], dtype=float),
    
    5: np.array([
        [0, 2, 9, 10, 7],
        [1, 0, 6, 4, 3],
        [15, 7, 0, 8, 3],
        [6, 3, 12, 0, 11],
        [9, 7, 5, 6, 0]
    ], dtype=float),
    
    6: np.array([
        [0, 3, 6, 7, 8, 9],
        [3, 0, 5, 6, 7, 8],
        [6, 5, 0, 4, 5, 6],
        [7, 6, 4, 0, 3, 4],
        [8, 7, 5, 3, 0, 2],
        [9, 8, 6, 4, 2, 0]
    ], dtype=float)
}

# =============================================================================
# FUNÇÃO DE EXECUÇÃO COMPLETA
# =============================================================================

def executar_comparacao_completa(graphs, p_qaoa=2, shots=4096):
    """
    Executa comparação sistemática entre Brute Force e QAOA.
    
    Retorna DataFrame com métricas conforme solicitado:
    - Número de cidades
    - Tempo clássico vs quântico
    - Custo da rota clássica ótima
    - Custo da melhor rota via QAOA
    - Distância relativa ao ótimo
    """
    
    resultados = []
    
    for n_cidades, D in graphs.items():
        print(f"\n{'='*70}")
        print(f"📍 PROCESSANDO: {n_cidades} CIDADES ({n_cidades**2} qubits)")
        print(f"{'='*70}")
        
        # =================================================================
        # BRUTE FORCE CLÁSSICO
        # =================================================================
        print(f"\n[1/2] 🔍 Executando Brute Force Clássico...")
        
        inicio_bf = time.time()
        rota_bf, custo_bf = brute_force_tsp(D)
        tempo_bf = time.time() - inicio_bf
        
        print(f"      ✅ Rota ótima: {rota_bf}")
        print(f"      ✅ Custo: {custo_bf}")
        print(f"      ✅ Tempo: {tempo_bf:.6f}s")
        
        # =================================================================
        # QAOA
        # =================================================================
        print(f"\n[2/2] ⚛️  Executando QAOA (p={p_qaoa})...")
        
        # Construir Hamiltoniano
        n = len(D)
        A = np.max(D) * n + 1
        h, J = construir_hamiltoniano_tsp(D, A)
        num_qubits = n ** 2
        
        # Medir tempo total do QAOA (construção + otimização + execução)
        inicio_qaoa = time.time()
        
        # Otimização
        init_params = [0.5] * (2 * p_qaoa)
        res = minimize(
            objective,
            init_params,
            args=(h, J, D, num_qubits, p_qaoa),
            method="COBYLA",
            options={'maxiter': 200}
        )
        
        # Circuito final
        gammas = res.x[:p_qaoa]
        betas = res.x[p_qaoa:]
        qc_final = qaoa_circuit(h, J, num_qubits, gammas, betas)
        qc_final.measure_all()
        
        # Execução final
        tqc = transpile(qc_final, sim)
        result = sim.run(tqc, shots=shots).result()
        counts = result.get_counts()
        
        tempo_qaoa = time.time() - inicio_qaoa
        
        # Extrair melhor resultado
        exp_cost, frac_validas, (melhor_rota_qaoa, melhor_custo_qaoa) = expected_cost(counts, D)
        
        # Tratar caso de não encontrar solução válida
        if melhor_rota_qaoa is None:
            melhor_custo_qaoa = float('inf')
            gap_relativo = float('inf')
            melhor_rota_qaoa = "N/A"
        else:
            gap_relativo = ((melhor_custo_qaoa - custo_bf) / custo_bf) * 100
        
        print(f"      ✅ Melhor rota: {melhor_rota_qaoa}")
        print(f"      ✅ Custo QAOA: {melhor_custo_qaoa}")
        print(f"      ✅ Tempo: {tempo_qaoa:.4f}s")
        print(f"      ✅ Soluções válidas: {100*frac_validas:.1f}%")
        print(f"      ✅ Gap relativo: {gap_relativo:.2f}%")
        
        # Armazenar resultado
        resultados.append({
            'Cidades (n)': n_cidades,
            'Qubits (n²)': n_cidades ** 2,
            'Rota Clássica': str(rota_bf),
            'Custo Clássico': custo_bf,
            'Tempo Clássico (s)': tempo_bf,
            'Rota QAOA': str(melhor_rota_qaoa),
            'Custo QAOA': melhor_custo_qaoa,
            'Tempo QAOA (s)': tempo_qaoa,
            'Gap Relativo (%)': gap_relativo,
            'Soluções Válidas (%)': frac_validas * 100,
            'Ótimo Encontrado': 'Sim' if melhor_custo_qaoa == custo_bf else 'Não'
        })
    
    # Criar DataFrame
    df = pd.DataFrame(resultados)
    
    return df


# =============================================================================
# EXECUTAR COMPARAÇÃO
# =============================================================================

print("=" * 70)
print("🚀 COMPARAÇÃO SISTEMÁTICA: BRUTE FORCE vs QAOA")
print("=" * 70)

# Executar (ajuste p_qaoa conforme necessário)
df_resultados = executar_comparacao_completa(graphs, p_qaoa=2, shots=4096)

# =============================================================================
# EXIBIR RESULTADOS
# =============================================================================

print("\n")
print("=" * 70)
print("📊 TABELA DE RESULTADOS")
print("=" * 70)

# Exibir DataFrame completo
print("\n")
display(df_resultados)

# =============================================================================
# TABELA RESUMIDA (formato do enunciado)
# =============================================================================

print("\n")
print("=" * 70)
print("📋 RESUMO CONFORME ENUNCIADO")
print("=" * 70)

df_resumo = df_resultados[[
    'Cidades (n)', 
    'Tempo Clássico (s)', 
    'Tempo QAOA (s)',
    'Custo Clássico', 
    'Custo QAOA', 
    'Gap Relativo (%)'
]].copy()

df_resumo.columns = [
    'Cidades',
    'Tempo Clássico (s)',
    'Tempo Quântico (s)',
    'Custo Ótimo',
    'Custo QAOA',
    'Distância Relativa (%)'
]

print("\n")
display(df_resumo)

# =============================================================================
# ANÁLISE DE DESEMPENHO
# =============================================================================

print("\n")
print("=" * 70)
print("📈 ANÁLISE DE DESEMPENHO E LIMITAÇÕES")
print("=" * 70)

print("\n🔹 DESEMPENHO DO BRUTE FORCE (Clássico):")
print("-" * 50)
print(f"   • Sempre encontra a solução ÓTIMA")
print(f"   • Complexidade: O(n!) - cresce fatorialmente")
print(f"   • Tempo para n=3: {df_resultados[df_resultados['Cidades (n)']==3]['Tempo Clássico (s)'].values[0]:.6f}s")
print(f"   • Tempo para n=6: {df_resultados[df_resultados['Cidades (n)']==6]['Tempo Clássico (s)'].values[0]:.6f}s")

print("\n🔹 DESEMPENHO DO QAOA (Quântico simulado):")
print("-" * 50)
n_otimos = df_resultados[df_resultados['Ótimo Encontrado'] == 'Sim'].shape[0]
print(f"   • Soluções ótimas encontradas: {n_otimos}/{len(graphs)}")
print(f"   • Gap médio: {df_resultados['Gap Relativo (%)'].mean():.2f}%")
print(f"   • Média de soluções válidas: {df_resultados['Soluções Válidas (%)'].mean():.1f}%")

print("\n🔹 LIMITAÇÕES OBSERVADAS:")
print("-" * 50)
print("   • QAOA é um algoritmo APROXIMADO (não garante ótimo)")
print("   • Número de qubits cresce com n² (escalabilidade limitada)")
print("   • Simulação clássica de qubits é exponencialmente custosa")
print("   • Muitas soluções medidas violam as restrições do TSP")
print("   • Qualidade depende do número de camadas (p) e otimização")

print("\n🔹 COMPARAÇÃO DE ESCALABILIDADE:")
print("-" * 50)
print("   • Brute Force: O(n!) - inviável para n > 12")
print("   • QAOA (simulado): O(2^{n²}) - inviável para n > 5")
print("   • QAOA (hardware real): potencial vantagem para n grande")

# =============================================================================
# GRÁFICOS DE ANÁLISE
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Gráfico 1: Comparação de Tempos
ax1 = axes[0, 0]
x = df_resultados['Cidades (n)']
width = 0.35
ax1.bar(x - width/2, df_resultados['Tempo Clássico (s)'], width, label='Brute Force', color='steelblue')
ax1.bar(x + width/2, df_resultados['Tempo QAOA (s)'], width, label='QAOA', color='purple', alpha=0.8)
ax1.set_xlabel('Número de Cidades')
ax1.set_ylabel('Tempo (s)')
ax1.set_title('Tempo de Execução: Clássico vs QAOA')
ax1.legend()
ax1.set_xticks(x)

# Gráfico 2: Comparação de Custos
ax2 = axes[0, 1]
ax2.bar(x - width/2, df_resultados['Custo Clássico'], width, label='Ótimo (BF)', color='steelblue')
ax2.bar(x + width/2, df_resultados['Custo QAOA'], width, label='QAOA', color='purple', alpha=0.8)
ax2.set_xlabel('Número de Cidades')
ax2.set_ylabel('Custo da Rota')
ax2.set_title('Custo da Rota: Ótimo vs QAOA')
ax2.legend()
ax2.set_xticks(x)

# Gráfico 3: Gap Relativo
ax3 = axes[1, 0]
colors = ['green' if g == 0 else 'orange' if g < 50 else 'red' for g in df_resultados['Gap Relativo (%)']]
ax3.bar(x, df_resultados['Gap Relativo (%)'], color=colors)
ax3.set_xlabel('Número de Cidades')
ax3.set_ylabel('Gap Relativo (%)')
ax3.set_title('Distância Relativa ao Ótimo')
ax3.axhline(y=0, color='green', linestyle='--', alpha=0.5, label='Ótimo')
ax3.set_xticks(x)

# Gráfico 4: Porcentagem de Soluções Válidas
ax4 = axes[1, 1]
ax4.bar(x, df_resultados['Soluções Válidas (%)'], color='teal')
ax4.set_xlabel('Número de Cidades')
ax4.set_ylabel('Soluções Válidas (%)')
ax4.set_title('Porcentagem de Soluções Válidas (QAOA)')
ax4.set_xticks(x)
ax4.set_ylim(0, 100)

plt.tight_layout()
plt.savefig('comparacao_bf_qaoa.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n📁 Gráfico salvo como 'comparacao_bf_qaoa.png'")

# =============================================================================
# EXPORTAR PARA CSV (opcional)
# =============================================================================

df_resultados.to_csv('resultados_tsp_qaoa.csv', index=False)
print("📁 Resultados salvos em 'resultados_tsp_qaoa.csv'")
