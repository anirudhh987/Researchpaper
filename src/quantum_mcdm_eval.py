"""
src/quantum_mcdm_eval.py
Direct Quantum Sensitivity evaluation for TOPSIS criteria weights.
"""

import numpy as np
from src.benchmark_mcdm import topsis_score
from src.quantum_sensitivity import QuantumIntegrator

def evaluate_quantum_sensitivity():
    # Benchmark 5x4 Decision Matrix
    decision_matrix = np.array([
        [80, 70, 90, 60],
        [90, 60, 85, 75],
        [70, 85, 80, 90],
        [60, 90, 70, 85],
        [85, 75, 95, 65]
    ], dtype=float)
    benefit_mask = np.array([True, True, False, True])

    # 1. Marginal objective function E_{W~1}[f(W) | w1]:
    # Fix w1, sample over remaining weights (w2, w3, w4)
    def conditional_mean_w1(w1_val: float, num_mc_inner: int = 50) -> float:
        scores = []
        for _ in range(num_mc_inner):
            w_other = np.random.uniform(0.05, 0.95, size=3)
            w_full = np.array([w1_val, w_other[0], w_other[1], w_other[2]])
            w_norm = w_full / np.sum(w_full)
            scores.append(np.max(topsis_score(w_norm, decision_matrix, benefit_mask)))
        return float(np.mean(scores))

    # 2. Integrate using QuantumIntegrator
    print("Executing Quantum State-Preparation for w1 Sensitivity Integral...")
    q_integrator = QuantumIntegrator(num_qubits=4, epsilon=0.015, alpha=0.05)
    
    result = q_integrator.estimate(conditional_mean_w1, bounds=(0.05, 0.95))
    
    print("\n=== Quantum Sensitivity Analysis Result ===")
    print(f"Target Criterion: w1 (Quality/Cost Driver)")
    print(f"Quantum Expected Value E[Y|w1]: {result['estimation']:.5f}")
    print(f"95% Confidence Interval: [{result['confidence_interval'][0]:.5f}, {result['confidence_interval'][1]:.5f}]")
    print(f"Grover Oracle Query Budget: {result['num_oracle_queries']}")

if __name__ == "__main__":
    evaluate_quantum_sensitivity()
