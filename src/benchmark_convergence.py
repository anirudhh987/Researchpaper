"""
src/benchmark_convergence.py
Empirical convergence comparative analysis: Classical MC vs. Iterative QAE.
"""

import numpy as np
import matplotlib.pyplot as plt
from src.quantum_sensitivity import QuantumIntegrator

def run_scaling_benchmark():
    func = lambda x: np.sin(np.pi * x) ** 2
    true_val = 0.5
    
    # 1. Classical Monte Carlo Evaluation Scaling
    sample_sizes = [64, 128, 256, 512, 1024, 2048, 4096]
    mc_errors = []
    
    for n in sample_sizes:
        trials = [np.mean(func(np.random.uniform(0, 1, n))) for _ in range(40)]
        mc_errors.append(float(np.mean(np.abs(np.array(trials) - true_val))))
        
    # 2. Iterative Quantum Amplitude Estimation Scaling
    target_epsilons = [0.1, 0.05, 0.025, 0.0125]
    qae_queries = []
    qae_errors = []
    
    for eps in target_epsilons:
        q_eng = QuantumIntegrator(num_qubits=4, epsilon=eps)
        q_res = q_eng.estimate(func, bounds=(0.0, 1.0))
        qae_queries.append(int(q_res["num_oracle_queries"]))
        qae_errors.append(float(abs(q_res["estimation"] - true_val)))
        
    print("=== Convergence Profiling Complete ===")
    print(f"Sample Sizes (MC): {sample_sizes}")
    print(f"MC Absolute Errors: {[round(x, 5) for x in mc_errors]}")
    print(f"QAE Oracle Queries: {qae_queries}")
    print(f"QAE Absolute Errors: {[round(x, 5) for x in qae_errors]}")

    # Generate Figure 1 for Manuscript
    plt.figure(figsize=(7, 4.5))
    plt.loglog(sample_sizes, mc_errors, 'o-', label=r'Classical MC ($\mathcal{O}(1/\sqrt{N})$)', color='#1f77b4', lw=2)
    plt.loglog(qae_queries, qae_errors, 's--', label=r'Iterative QAE ($\mathcal{O}(1/N)$)', color='#d62728', lw=2)
    plt.xlabel('Oracle Queries / Sample Count ($N$)', fontsize=11)
    plt.ylabel('Mean Absolute Estimation Error', fontsize=11)
    plt.title('Empirical Scaling: Classical Monte Carlo vs. Iterative QAE', fontsize=12)
    plt.grid(True, which="both", ls=":", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('figures/convergence_comparison.png', dpi=300)
    print("Saved plot to figures/convergence_comparison.png")

if __name__ == "__main__":
    run_scaling_benchmark()
