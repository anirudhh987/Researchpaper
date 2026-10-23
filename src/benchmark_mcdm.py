"""
src/benchmark_mcdm.py
Classical MCDM (TOPSIS) & Sobol Sensitivity Analysis baseline.
"""

import numpy as np
from SALib.sample import saltelli
from SALib.analyze import sobol

def topsis_score(weights: np.ndarray, criteria_matrix: np.ndarray, benefit_mask: np.ndarray) -> np.ndarray:
    norm_factor = np.sqrt(np.sum(criteria_matrix**2, axis=0))
    norm_matrix = criteria_matrix / norm_factor
    weighted_matrix = norm_matrix * weights
    
    ideal_best = np.zeros(criteria_matrix.shape[1])
    ideal_worst = np.zeros(criteria_matrix.shape[1])
    
    for j in range(criteria_matrix.shape[1]):
        if benefit_mask[j]:
            ideal_best[j] = np.max(weighted_matrix[:, j])
            ideal_worst[j] = np.min(weighted_matrix[:, j])
        else:
            ideal_best[j] = np.min(weighted_matrix[:, j])
            ideal_worst[j] = np.max(weighted_matrix[:, j])
            
    dist_best = np.sqrt(np.sum((weighted_matrix - ideal_best)**2, axis=1))
    dist_worst = np.sqrt(np.sum((weighted_matrix - ideal_worst)**2, axis=1))
    
    closeness = dist_worst / (dist_best + dist_worst + 1e-12)
    return closeness

def run_classical_sobol(num_samples: int = 1024):
    problem = {
        'num_vars': 4,
        'names': ['w1', 'w2', 'w3', 'w4'],
        'bounds': [[0.05, 0.95]] * 4
    }
    
    np.random.seed(42)
    decision_matrix = np.array([
        [80, 70, 90, 60],
        [90, 60, 85, 75],
        [70, 85, 80, 90],
        [60, 90, 70, 85],
        [85, 75, 95, 65]
    ], dtype=float)
    benefit_mask = np.array([True, True, False, True])
    
    param_values = saltelli.sample(problem, num_samples, calc_second_order=False)
    
    y = np.zeros(param_values.shape[0])
    for i, w in enumerate(param_values):
        norm_w = w / np.sum(w)
        scores = topsis_score(norm_w, decision_matrix, benefit_mask)
        y[i] = np.max(scores)
        
    sobol_indices = sobol.analyze(problem, y, calc_second_order=False)
    print("--- Classical Sobol Analysis Complete ---")
    print("S1 (First-order):", {k: float(v) for k, v in zip(problem['names'], sobol_indices['S1'])})
    print("ST (Total-effect):", {k: float(v) for k, v in zip(problem['names'], sobol_indices['ST'])})
    return sobol_indices

if __name__ == "__main__":
    run_classical_sobol(1024)
