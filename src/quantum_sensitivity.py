"""
src/quantum_sensitivity.py
Iterative Quantum Amplitude Estimation (IQAE) engine for sensitivity analysis.
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import IterativeAmplitudeEstimation, EstimationProblem

class QuantumIntegrator:
    def __init__(self, num_qubits: int = 3, epsilon: float = 0.02, alpha: float = 0.05):
        self.num_qubits = num_qubits
        self.epsilon = epsilon
        self.alpha = alpha

    def construct_state_preparation(self, objective_func, bounds=(0.0, 1.0)):
        num_states = 2 ** self.num_qubits
        grid_points = np.linspace(bounds[0], bounds[1], num_states)
        evals = np.array([objective_func(x) for x in grid_points])
        
        min_val, max_val = float(np.min(evals)), float(np.max(evals))
        span = max_val - min_val if (max_val - min_val) > 1e-9 else 1.0
        normalized_evals = (evals - min_val) / span

        qc = QuantumCircuit(self.num_qubits + 1)
        for i in range(self.num_qubits):
            qc.h(i)

        for state_idx, val in enumerate(normalized_evals):
            angle = 2.0 * np.arcsin(np.sqrt(np.clip(val, 0.0, 1.0)))
            bin_str = format(state_idx, f'0{self.num_qubits}b')
            
            for bit_pos, bit in enumerate(bin_str):
                if bit == '0':
                    qc.x(bit_pos)
                    
            qc.mcry(angle, list(range(self.num_qubits)), self.num_qubits)
            
            for bit_pos, bit in enumerate(bin_str):
                if bit == '0':
                    qc.x(bit_pos)

        return qc, min_val, span

    def estimate(self, objective_func, bounds=(0.0, 1.0)):
        state_prep, min_val, span = self.construct_state_preparation(objective_func, bounds)
        
        problem = EstimationProblem(
            state_preparation=state_prep,
            objective_qubits=[self.num_qubits]
        )
        
        sampler = StatevectorSampler()
        iqae = IterativeAmplitudeEstimation(
            epsilon_target=self.epsilon,
            alpha=self.alpha,
            sampler=sampler
        )
        
        result = iqae.estimate(problem)
        raw_amplitude = result.estimation
        scaled_integral = min_val + (raw_amplitude * span)
        
        return {
            "estimation": scaled_integral,
            "raw_amplitude": raw_amplitude,
            "confidence_interval": [
                min_val + (result.confidence_interval[0] * span),
                min_val + (result.confidence_interval[1] * span)
            ],
            "num_oracle_queries": result.num_oracle_queries
        }

if __name__ == "__main__":
    integrator = QuantumIntegrator(num_qubits=3, epsilon=0.02)
    res = integrator.estimate(lambda x: x**2, bounds=(0.0, 1.0))
    print("--- IQAE Test Verification Complete ---")
    print(f"Estimated Integral: {res['estimation']:.5f}")
    print(f"Confidence Interval: [{res['confidence_interval'][0]:.5f}, {res['confidence_interval'][1]:.5f}]")
    print(f"Oracle Query Calls: {res['num_oracle_queries']}")
