#!/usr/bin/env python3
"""
Atividade Hands-ON 2: Benchmark Criptografia Clássica vs Pós-Quântica
Objetivo: Medir e comparar tempos de geração, assinatura e verificação

Autor: SENAI CIMATEC
Data: 2025
"""

import time
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Importações para criptografia clássica
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

# Simulação de algoritmos pós-quânticos (representando ML-DSA)
# Em ambiente real, usaria bibliotecas como liboqs-python
import hashlib
import random
import os

class PostQuantumSimulator:
    """Simulador de algoritmos pós-quânticos para fins didáticos"""
    
    def __init__(self, security_level="44"):
        self.security_level = security_level
        if security_level == "44":
            self.key_size = 1312 + 2400  # ML-DSA-44
            self.signature_size = 2420
        elif security_level == "65":
            self.key_size = 1952 + 4000  # ML-DSA-65
            self.signature_size = 3309
        else:
            self.key_size = 2592 + 4896  # ML-DSA-87
            self.signature_size = 4627
    
    def generate_keypair(self):
        """Simula geração de chaves pós-quânticas"""
        # Simula complexidade computacional
        start_time = time.perf_counter()
        
        # Operações simuladas baseadas na complexidade real
        for _ in range(100):
            _ = hashlib.sha256(os.urandom(32)).hexdigest()
        
        private_key = os.urandom(self.key_size // 8)
        public_key = hashlib.sha256(private_key).digest()
        
        elapsed = time.perf_counter() - start_time
        return (private_key, public_key), elapsed
    
    def sign(self, message, private_key):
        """Simula assinatura pós-quântica"""
        start_time = time.perf_counter()
        
        # Simula operações de assinatura
        for _ in range(50):
            _ = hashlib.sha256(message + private_key).hexdigest()
        
        signature = os.urandom(self.signature_size)
        
        elapsed = time.perf_counter() - start_time
        return signature, elapsed
    
    def verify(self, message, signature, public_key):
        """Simula verificação pós-quântica"""
        start_time = time.perf_counter()
        
        # Simula operações de verificação
        for _ in range(30):
            _ = hashlib.sha256(message + signature + public_key).hexdigest()
        
        # Simula sucesso na verificação
        valid = True
        
        elapsed = time.perf_counter() - start_time
        return valid, elapsed

class CryptoBenchmark:
    """Classe principal para benchmark de algoritmos criptográficos"""
    
    def __init__(self):
        self.results = []
        self.message = b"Mensagem de teste para benchmark criptografico - SENAI CIMATEC 2025"
        
    def setup_environment(self):
        """Configura ambiente de teste controlado"""
        print("🔧 Configurando ambiente de teste controlado...")
        
        # Aquece a CPU
        for _ in range(1000):
            _ = time.perf_counter()
        
        print("✅ Ambiente configurado com sucesso!")
        
    def benchmark_rsa(self, key_size=2048, iterations=1000):
        """Benchmark RSA clássico"""
        print(f"🔐 Testando RSA-{key_size}...")
        
        # Geração de chaves
        keygen_times = []
        signing_times = []
        verification_times = []
        
        for i in range(iterations):
            if i % 100 == 0:
                print(f"  Progresso: {i}/{iterations}")
            
            # Geração de chaves
            start = time.perf_counter()
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size
            )
            public_key = private_key.public_key()
            keygen_time = time.perf_counter() - start
            keygen_times.append(keygen_time)
            
            # Assinatura
            start = time.perf_counter()
            signature = private_key.sign(
                self.message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            signing_time = time.perf_counter() - start
            signing_times.append(signing_time)
            
            # Verificação
            start = time.perf_counter()
            try:
                public_key.verify(
                    signature,
                    self.message,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                verification_time = time.perf_counter() - start
                verification_times.append(verification_time)
            except InvalidSignature:
                verification_times.append(float('inf'))
        
        return {
            'algorithm': f'RSA-{key_size}',
            'type': 'Clássico',
            'keygen_times': keygen_times,
            'signing_times': signing_times,
            'verification_times': verification_times
        }
    
    def benchmark_ecdsa(self, curve_name='P-256', iterations=1000):
        """Benchmark ECDSA clássico"""
        print(f"🔐 Testando ECDSA {curve_name}...")
        
        curve = ec.SECP256R1() if curve_name == 'P-256' else ec.SECP384R1()
        
        keygen_times = []
        signing_times = []
        verification_times = []
        
        for i in range(iterations):
            if i % 100 == 0:
                print(f"  Progresso: {i}/{iterations}")
            
            # Geração de chaves
            start = time.perf_counter()
            private_key = ec.generate_private_key(curve)
            public_key = private_key.public_key()
            keygen_time = time.perf_counter() - start
            keygen_times.append(keygen_time)
            
            # Assinatura
            start = time.perf_counter()
            signature = private_key.sign(self.message, ec.ECDSA(hashes.SHA256()))
            signing_time = time.perf_counter() - start
            signing_times.append(signing_time)
            
            # Verificação
            start = time.perf_counter()
            try:
                public_key.verify(signature, self.message, ec.ECDSA(hashes.SHA256()))
                verification_time = time.perf_counter() - start
                verification_times.append(verification_time)
            except InvalidSignature:
                verification_times.append(float('inf'))
        
        return {
            'algorithm': f'ECDSA-{curve_name}',
            'type': 'Clássico',
            'keygen_times': keygen_times,
            'signing_times': signing_times,
            'verification_times': verification_times
        }
    
    def benchmark_post_quantum(self, security_level="44", iterations=1000):
        """Benchmark algoritmos pós-quânticos (simulado)"""
        print(f"🔐 Testando ML-DSA-{security_level}...")
        
        pq_algo = PostQuantumSimulator(security_level)
        
        keygen_times = []
        signing_times = []
        verification_times = []
        
        for i in range(iterations):
            if i % 100 == 0:
                print(f"  Progresso: {i}/{iterations}")
            
            # Geração de chaves
            keypair, keygen_time = pq_algo.generate_keypair()
            keygen_times.append(keygen_time)
            
            private_key, public_key = keypair
            
            # Assinatura
            signature, signing_time = pq_algo.sign(self.message, private_key)
            signing_times.append(signing_time)
            
            # Verificação
            valid, verification_time = pq_algo.verify(self.message, signature, public_key)
            verification_times.append(verification_time)
        
        return {
            'algorithm': f'ML-DSA-{security_level}',
            'type': 'Pós-Quântico',
            'keygen_times': keygen_times,
            'signing_times': signing_times,
            'verification_times': verification_times
        }
    
    def run_all_benchmarks(self, iterations=1000):
        """Executa todos os benchmarks"""
        print(f"🚀 Iniciando benchmark com {iterations} operações por algoritmo...")
        print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        self.setup_environment()
        
        algorithms_to_test = [
            ('rsa', 2048),
            ('ecdsa', 'P-256'),
            ('post_quantum', '44'),
            ('post_quantum', '65'),
            ('post_quantum', '87')
        ]
        
        all_results = []
        
        for algo_type, param in algorithms_to_test:
            try:
                if algo_type == 'rsa':
                    result = self.benchmark_rsa(param, iterations)
                elif algo_type == 'ecdsa':
                    result = self.benchmark_ecdsa(param, iterations)
                elif algo_type == 'post_quantum':
                    result = self.benchmark_post_quantum(param, iterations)
                
                all_results.append(result)
                
            except Exception as e:
                print(f"❌ Erro ao testar {algo_type}-{param}: {e}")
        
        return all_results
    
    def calculate_statistics(self, results):
        """Calcula médias, medianas e desvios padrão"""
        stats_data = []
        
        for result in results:
            algorithm = result['algorithm']
            algo_type = result['type']
            
            # Estatísticas para cada operação
            for operation in ['keygen', 'signing', 'verification']:
                times = result[f'{operation}_times']
                
                if times:
                    stats_data.append({
                        'Algoritmo': algorithm,
                        'Tipo': algo_type,
                        'Operação': operation.title(),
                        'Média (ms)': np.mean(times) * 1000,
                        'Mediana (ms)': np.median(times) * 1000,
                        'Desvio Padrão (ms)': np.std(times) * 1000,
                        'Min (ms)': np.min(times) * 1000,
                        'Max (ms)': np.max(times) * 1000
                    })
        
        return pd.DataFrame(stats_data)
    
    def create_performance_dashboard(self, stats_df):
        """Cria dashboard de performance"""
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Dashboard de Performance - Criptografia Clássica vs Pós-Quântica', 
                     fontsize=16, fontweight='bold')
        
        # Gráfico 1: Comparação de médias por operação
        ax1 = axes[0, 0]
        pivot_mean = stats_df.pivot(index='Algoritmo', columns='Operação', values='Média (ms)')
        pivot_mean.plot(kind='bar', ax=ax1, width=0.8)
        ax1.set_title('Tempo Médio por Operação')
        ax1.set_ylabel('Tempo (ms)')
        ax1.legend(title='Operação')
        ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico 2: Comparação Clássico vs Pós-Quântico
        ax2 = axes[0, 1]
        type_comparison = stats_df.groupby(['Tipo', 'Operação'])['Média (ms)'].mean().unstack()
        type_comparison.plot(kind='bar', ax=ax2, width=0.8)
        ax2.set_title('Clássico vs Pós-Quântico')
        ax2.set_ylabel('Tempo Médio (ms)')
        ax2.legend(title='Operação')
        ax2.tick_params(axis='x', rotation=0)
        
        # Gráfico 3: Desvio padrão (consistência)
        ax3 = axes[1, 0]
        pivot_std = stats_df.pivot(index='Algoritmo', columns='Operação', values='Desvio Padrão (ms)')
        pivot_std.plot(kind='bar', ax=ax3, width=0.8)
        ax3.set_title('Desvio Padrão (Consistência)')
        ax3.set_ylabel('Desvio Padrão (ms)')
        ax3.legend(title='Operação')
        ax3.tick_params(axis='x', rotation=45)
        
        # Gráfico 4: Heatmap de performance
        ax4 = axes[1, 1]
        heatmap_data = stats_df.pivot(index='Algoritmo', columns='Operação', values='Média (ms)')
        sns.heatmap(heatmap_data, annot=True, fmt='.2f', cmap='YlOrRd', ax=ax4)
        ax4.set_title('Heatmap de Performance (ms)')
        
        plt.tight_layout()
        return fig
    
    def generate_recommendations(self, stats_df):
        """Gera recomendações baseadas nos resultados"""
        recommendations = []
        
        # Análise por operação
        for operation in ['Keygen', 'Signing', 'Verification']:
            op_data = stats_df[stats_df['Operação'] == operation]
            fastest = op_data.loc[op_data['Média (ms)'].idxmin()]
            slowest = op_data.loc[op_data['Média (ms)'].idxmax()]
            
            recommendations.append({
                'Operação': operation,
                'Mais Rápido': f"{fastest['Algoritmo']} ({fastest['Média (ms)']:.2f}ms)",
                'Mais Lento': f"{slowest['Algoritmo']} ({slowest['Média (ms)']:.2f}ms)",
                'Diferença': f"{(slowest['Média (ms)'] / fastest['Média (ms)']):.1f}x mais lento"
            })
        
        # Recomendações específicas
        practical_recommendations = [
            "🏙️ **Torres Urbanas**: ML-DSA-65 é aceitável devido à energia constante",
            "🌾 **Torres Rurais**: Híbrido (ECDSA + ML-DSA-44) equilibra performance e segurança",
            "⚡ **Aplicações em Tempo Real**: Considerar ECDSA P-256 para transição gradual",
            "🔒 **Máxima Segurança**: ML-DSA-87 para dados extremamente sensíveis",
            "💡 **Recomendação Geral**: Implementar hibridização durante período de transição"
        ]
        
        return recommendations, practical_recommendations

def main():
    """Função principal"""
    print("🛡️ BENCHMARK CRIPTOGRAFIA: CLÁSSICA vs PÓS-QUÂNTICA")
    print("=" * 60)
    
    # Configuração do benchmark
    benchmark = CryptoBenchmark()
    iterations = 1000  # Pode ajustar para testes mais rápidos (ex: 100)
    
    # Execução dos testes
    results = benchmark.run_all_benchmarks(iterations)
    
    if not results:
        print("❌ Nenhum resultado obtido. Verifique as dependências.")
        return
    
    # Cálculo das estatísticas
    print("\n📊 Calculando estatísticas...")
    stats_df = benchmark.calculate_statistics(results)
    
    # Exibição dos resultados
    print("\n📈 ANÁLISE ESTATÍSTICA")
    print("=" * 60)
    print(stats_df.to_string(index=False))
    
    # Dashboard visual
    print("\n📊 Gerando dashboard de performance...")
    fig = benchmark.create_performance_dashboard(stats_df)
    plt.show()
    
    # Recomendações
    print("\n💡 RECOMENDAÇÕES DE USO")
    print("=" * 60)
    recommendations, practical_recommendations = benchmark.generate_recommendations(stats_df)
    
    for rec in recommendations:
        print(f"**{rec['Operação']}**:")
        print(f"  • Mais rápido: {rec['Mais Rápido']}")
        print(f"  • Mais lento: {rec['Mais Lento']}")
        print(f"  • Diferença: {rec['Diferença']}\n")
    
    print("🎯 **Recomendações Práticas:**")
    for rec in practical_recommendations:
        print(f"  {rec}")
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"benchmark_criptografia_{timestamp}.csv"
    stats_df.to_csv(filename, index=False)
    print(f"\n💾 Resultados salvos em: {filename}")
    
    # Salvar gráfico
    graph_filename = f"dashboard_performance_{timestamp}.png"
    fig.savefig(graph_filename, dpi=300, bbox_inches='tight')
    print(f"📊 Dashboard salvo em: {graph_filename}")

if __name__ == "__main__":
    main()