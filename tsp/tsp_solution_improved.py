"""
Solução Completa para TSP - Abordagem Clássica vs Quântica (QAOA)
Trabalho: Implementação e Comparação de Algoritmos TSP
"""

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import pickle
import os
import json
from typing import Tuple, List, Dict, Any

# Bibliotecas Quânticas (Qiskit 1.x+)
try:
    from qiskit_algorithms import QAOA, VQE
    from qiskit_algorithms.optimizers import COBYLA, SPSA
    from qiskit.primitives import Sampler, StatevectorSampler
    from qiskit.circuit import QuantumCircuit
    from qiskit.quantum_info import SparsePauliOp
    from qiskit_optimization.applications import Tsp
    from qiskit_optimization.algorithms import MinimumEigenOptimizer
    from qiskit_ibm_runtime import QiskitRuntimeService
    QISKIT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Aviso: Bibliotecas Qiskit não disponíveis ({e})")
    QISKIT_AVAILABLE = False

# ============================================================================
# 1. DEFINIÇÃO DOS GRAFOS E ESTRUTURAS
# ============================================================================

GRAPHS = {
    3: [[0, 10, 15], [10, 0, 20], [15, 20, 0]],
    4: [[0, 1, 50, 50], [1, 0, 2, 50], [50, 2, 0, 3], [50, 50, 3, 0]],
    5: [[0, 2, 9, 10, 7], [1, 0, 6, 4, 3], [15, 7, 0, 8, 3], [6, 3, 12, 0, 11], [9, 7, 5, 6, 0]],
    6: [[0, 3, 6, 7, 8, 9], [3, 0, 5, 6, 7, 8], [6, 5, 0, 4, 5, 6], [7, 6, 4, 0, 3, 4], [8, 7, 5, 3, 0, 2], [9, 8, 6, 4, 2, 0]]
}

OUTPUT_DIR = "/home/claude/tsp_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# 2. FUNÇÕES CLÁSSICAS (BRUTE FORCE TSP)
# ============================================================================

def calculate_route_cost(route: Tuple[int, ...], distance_matrix: List[List[float]]) -> float:
    """Calcula o custo total de uma rota."""
    cost = 0
    for i in range(len(route) - 1):
        cost += distance_matrix[route[i]][route[i + 1]]
    return cost


def solve_tsp_brute_force(distance_matrix: List[List[float]]) -> Tuple[float, Tuple[int, ...], float]:
    """
    Resolve TSP por força bruta (permutações).
    
    Returns:
        (custo_ótimo, rota_ótima, tempo_execução)
    """
    start_time = time.time()
    n = len(distance_matrix)
    vertices = list(range(1, n))  # Começa do vértice 1
    
    min_cost = float('inf')
    best_route = None
    
    for perm in itertools.permutations(vertices):
        route = (0,) + perm + (0,)  # Volta ao início
        cost = calculate_route_cost(route, distance_matrix)
        
        if cost < min_cost:
            min_cost = cost
            best_route = route
    
    elapsed_time = time.time() - start_time
    return min_cost, best_route, elapsed_time


# ============================================================================
# 3. FUNÇÕES QUÂNTICAS (QAOA)
# ============================================================================

def interpret_tsp_solution(x_array: np.ndarray, n_cities: int) -> Tuple[int, ...]:
    """
    Decodifica a solução binária do QAOA em uma rota TSP.
    
    A codificação é: x[i*n + t] representa se a cidade i está na posição t da rota.
    """
    try:
        route = []
        for t in range(n_cities):
            for i in range(n_cities):
                if x_array[i * n_cities + t] >= 0.5:  # Threshold para arredondar
                    route.append(i)
                    break
        
        # Validar se é uma rota válida
        if len(set(route)) == n_cities and len(route) == n_cities:
            return tuple(route) + (route[0],)
        else:
            return None
    except Exception as e:
        print(f"Erro na decodificação: {e}")
        return None


def solve_tsp_qaoa(distance_matrix: List[List[float]], 
                   p: int = 1,
                   maxiter: int = 100,
                   seed: int = 42) -> Dict[str, Any]:
    """
    Resolve TSP usando QAOA (Quantum Approximate Optimization Algorithm).
    
    Args:
        distance_matrix: Matriz de distâncias
        p: Número de camadas do QAOA (reps)
        maxiter: Iterações máximas do otimizador clássico
        seed: Seed para reprodutibilidade
        
    Returns:
        Dicionário com resultados, circuito, e tempos
    """
    if not QISKIT_AVAILABLE:
        return {"error": "Qiskit não disponível"}
    
    start_time = time.time()
    n_cities = len(distance_matrix)
    
    try:
        # Criar problema TSP
        tsp_problem = Tsp(distance_matrix)
        qubo = tsp_problem.to_quadratic_program()
        
        # Configurar QAOA
        sampler = StatevectorSampler(seed=seed)
        optimizer = COBYLA(maxiter=maxiter, tol=1e-5)
        qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=p)
        
        # Executar otimização
        meo = MinimumEigenOptimizer(qaoa)
        result = meo.solve(qubo)
        
        # Decodificar resultado
        route = interpret_tsp_solution(result.x, n_cities)
        cost = result.fval if route else float('inf')
        
        elapsed_time = time.time() - start_time
        
        return {
            "success": True,
            "route": route,
            "cost": float(cost),
            "time": elapsed_time,
            "iterations": optimizer.settings.get("maxiter", maxiter),
            "fval": float(result.fval),
            "x": result.x
        }
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"❌ Erro QAOA ({n_cities} cidades): {type(e).__name__}: {str(e)[:100]}")
        return {
            "success": False,
            "error": str(e),
            "time": elapsed_time
        }


# ============================================================================
# 4. ANÁLISE E COMPARAÇÃO
# ============================================================================

def analyze_results(n_cities: int, 
                   classical_cost: float, 
                   classical_time: float,
                   quantum_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analisa comparativamente os resultados clássicos vs quânticos.
    """
    analysis = {
        "n_cities": n_cities,
        "classical_cost": classical_cost,
        "classical_time": classical_time,
        "quantum_success": quantum_result.get("success", False),
    }
    
    if quantum_result.get("success"):
        quantum_cost = quantum_result["cost"]
        quantum_time = quantum_result["time"]
        
        # Métrica de erro relativo
        relative_error = abs(quantum_cost - classical_cost) / classical_cost * 100
        speedup = classical_time / quantum_time if quantum_time > 0 else 0
        
        analysis.update({
            "quantum_cost": quantum_cost,
            "quantum_time": quantum_time,
            "relative_error_percent": relative_error,
            "speedup": speedup,
            "quantum_route": quantum_result.get("route"),
        })
    else:
        analysis.update({
            "quantum_cost": "N/A",
            "quantum_time": quantum_result.get("time", "N/A"),
            "relative_error_percent": "N/A",
            "speedup": "N/A",
            "quantum_route": None,
            "error_msg": quantum_result.get("error", "Unknown error")
        })
    
    return analysis


def create_comparison_visualizations(results_list: List[Dict[str, Any]]):
    """
    Cria gráficos comparativos dos resultados.
    """
    df = pd.DataFrame(results_list)
    
    # Filtrar apenas resultados bem-sucedidos do QAOA
    df_success = df[df["quantum_success"] == True].copy()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Tempo de Execução
    ax = axes[0, 0]
    x = range(len(df))
    ax.bar([i - 0.2 for i in x], df["classical_time"], width=0.4, label="Clássico", alpha=0.8)
    if not df_success.empty:
        quantum_times = [df[df["n_cities"] == n]["quantum_time"].values[0] 
                        for n in df["n_cities"] if not pd.isna(df[df["n_cities"] == n]["quantum_time"].values[0])]
        cities_q = [n for n in df["n_cities"] if not pd.isna(df[df["n_cities"] == n]["quantum_time"].values[0])]
        x_q = [df["n_cities"].tolist().index(n) for n in cities_q]
        ax.bar([i + 0.2 for i in x_q], quantum_times, width=0.4, label="QAOA", alpha=0.8)
    ax.set_xlabel("Número de Cidades")
    ax.set_ylabel("Tempo (s)")
    ax.set_title("Tempo de Execução: Clássico vs QAOA")
    ax.set_xticks(x)
    ax.set_xticklabels(df["n_cities"])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # 2. Custo da Rota
    ax = axes[0, 1]
    ax.bar([i - 0.2 for i in x], df["classical_cost"], width=0.4, label="Clássico", alpha=0.8)
    if not df_success.empty:
        quantum_costs = [df[df["n_cities"] == n]["quantum_cost"].values[0] 
                        for n in df["n_cities"] if df[df["n_cities"] == n]["quantum_success"].values[0]]
        cities_q = [n for n in df["n_cities"] if df[df["n_cities"] == n]["quantum_success"].values[0]]
        x_q = [df["n_cities"].tolist().index(n) for n in cities_q]
        ax.bar([i + 0.2 for i in x_q], quantum_costs, width=0.4, label="QAOA", alpha=0.8)
    ax.set_xlabel("Número de Cidades")
    ax.set_ylabel("Custo da Rota")
    ax.set_title("Custo Ótimo: Clássico vs QAOA")
    ax.set_xticks(x)
    ax.set_xticklabels(df["n_cities"])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # 3. Erro Relativo
    if not df_success.empty:
        ax = axes[1, 0]
        errors = [df[df["n_cities"] == n]["relative_error_percent"].values[0] 
                 for n in df_success["n_cities"]]
        cities = df_success["n_cities"].tolist()
        colors = ['green' if e < 5 else 'orange' if e < 20 else 'red' for e in errors]
        ax.bar(cities, errors, color=colors, alpha=0.8)
        ax.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
        ax.set_xlabel("Número de Cidades")
        ax.set_ylabel("Erro Relativo (%)")
        ax.set_title("Distância ao Ótimo (QAOA)")
        ax.grid(axis='y', alpha=0.3)
    else:
        axes[1, 0].text(0.5, 0.5, "Sem dados QAOA", ha='center', va='center', 
                       transform=axes[1, 0].transAxes)
    
    # 4. Speedup
    if not df_success.empty:
        ax = axes[1, 1]
        speedups = [df[df["n_cities"] == n]["speedup"].values[0] 
                   for n in df_success["n_cities"]]
        cities = df_success["n_cities"].tolist()
        colors = ['green' if s > 1 else 'red' for s in speedups]
        ax.bar(cities, speedups, color=colors, alpha=0.8)
        ax.axhline(y=1, color='black', linestyle='--', linewidth=1, label="Baseline (1x)")
        ax.set_xlabel("Número de Cidades")
        ax.set_ylabel("Speedup")
        ax.set_title("Speedup: Tempo Clássico / Tempo QAOA")
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
    else:
        axes[1, 1].text(0.5, 0.5, "Sem dados QAOA", ha='center', va='center',
                       transform=axes[1, 1].transAxes)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/tsp_comparison.png", dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {OUTPUT_DIR}/tsp_comparison.png")
    plt.close()


# ============================================================================
# 5. EXECUÇÃO PRINCIPAL
# ============================================================================

def main():
    print("=" * 80)
    print("SOLUÇÃO COMPLETA: TSP CLÁSSICO vs QAOA")
    print("=" * 80)
    
    results = []
    all_routes = {}
    
    # Processar cada tamanho de problema
    for n_cities in sorted(GRAPHS.keys()):
        print(f"\n{'='*80}")
        print(f"PROCESSANDO: {n_cities} CIDADES")
        print(f"{'='*80}")
        
        distance_matrix = GRAPHS[n_cities]
        
        # --- SOLUÇÃO CLÁSSICA ---
        print("\n[1/2] Executando Brute Force Clássico...")
        classical_cost, classical_route, classical_time = solve_tsp_brute_force(distance_matrix)
        print(f"     ✓ Rota ótima: {classical_route}")
        print(f"     ✓ Custo: {classical_cost:.4f}")
        print(f"     ✓ Tempo: {classical_time:.6f}s")
        
        # --- SOLUÇÃO QUÂNTICA ---
        print("\n[2/2] Executando QAOA...")
        quantum_result = solve_tsp_qaoa(distance_matrix, p=1, maxiter=50)
        
        if quantum_result.get("success"):
            print(f"     ✓ Rota: {quantum_result['route']}")
            print(f"     ✓ Custo: {quantum_result['cost']:.4f}")
            print(f"     ✓ Tempo: {quantum_result['time']:.6f}s")
        else:
            print(f"     ✗ Erro: {quantum_result.get('error', 'Unknown')}")
        
        # --- ANÁLISE ---
        analysis = analyze_results(n_cities, classical_cost, classical_time, quantum_result)
        results.append(analysis)
        
        # Armazenar rotas
        all_routes[n_cities] = {
            "classical": classical_route,
            "quantum": quantum_result.get("route")
        }
        
        # Exibir resumo
        print(f"\n📊 RESUMO:")
        print(f"   Custo Clássico: {classical_cost:.4f}")
        print(f"   Custo QAOA:     {analysis.get('quantum_cost', 'N/A')}")
        if analysis.get('quantum_success'):
            print(f"   Erro Relativo:  {analysis['relative_error_percent']:.2f}%")
            print(f"   Speedup:        {analysis['speedup']:.2f}x")
    
    # --- GERAR TABELA FINAL ---
    print(f"\n{'='*80}")
    print("TABELA COMPARATIVA FINAL")
    print(f"{'='*80}\n")
    
    df_results = pd.DataFrame(results)
    
    # Formatar para exibição
    display_df = df_results.copy()
    display_df["classical_time"] = display_df["classical_time"].apply(lambda x: f"{x:.6f}s")
    display_df["quantum_time"] = display_df["quantum_time"].apply(
        lambda x: f"{x:.6f}s" if isinstance(x, float) else "N/A"
    )
    display_df["classical_cost"] = display_df["classical_cost"].apply(lambda x: f"{x:.4f}")
    display_df["quantum_cost"] = display_df["quantum_cost"].apply(
        lambda x: f"{x:.4f}" if isinstance(x, float) else "N/A"
    )
    display_df["relative_error_percent"] = display_df["relative_error_percent"].apply(
        lambda x: f"{x:.2f}%" if isinstance(x, float) else "N/A"
    )
    display_df["speedup"] = display_df["speedup"].apply(
        lambda x: f"{x:.2f}x" if isinstance(x, float) else "N/A"
    )
    
    print(display_df.to_string(index=False))
    
    # --- SALVAR RESULTADOS ---
    print(f"\n{'='*80}")
    print("SALVANDO RESULTADOS")
    print(f"{'='*80}\n")
    
    # CSV
    csv_path = f"{OUTPUT_DIR}/tsp_results.csv"
    df_results.to_csv(csv_path, index=False)
    print(f"✓ Resultados (CSV): {csv_path}")
    
    # JSON
    json_path = f"{OUTPUT_DIR}/tsp_results.json"
    results_for_json = []
    for r in results:
        r_copy = r.copy()
        r_copy["quantum_route"] = str(r_copy.get("quantum_route"))
        results_for_json.append(r_copy)
    
    with open(json_path, 'w') as f:
        json.dump(results_for_json, f, indent=2)
    print(f"✓ Resultados (JSON): {json_path}")
    
    # Rotas
    routes_path = f"{OUTPUT_DIR}/tsp_routes.pkl"
    with open(routes_path, 'wb') as f:
        pickle.dump(all_routes, f)
    print(f"✓ Rotas (Pickle): {routes_path}")
    
    # Gerar visualizações
    print("\nGerando visualizações...")
    create_comparison_visualizations(results)
    
    print(f"\n{'='*80}")
    print(f"✓ EXECUÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"  Resultados salvos em: {OUTPUT_DIR}/")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
