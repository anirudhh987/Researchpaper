"""
src/generate_paper_figures.py
Generates two IEEE publication-grade research figures directly from empirical experiment runs.
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 11,
    'font.family': 'sans-serif',
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 13
})

# ==============================================================================
# Figure 1: Classical Variance Decomposition (Sobol Indices S1 vs ST)
# ==============================================================================
criteria = ['$w_1$ (Quality)', '$w_2$ (Cost)', '$w_3$ (Lead Time)', '$w_4$ (Risk)']
s1_values = [0.6983, 0.0170, -0.0013, 0.0629]
st_values = [0.9123, 0.1595, 0.0589, 0.1620]
s1_err = [0.038, 0.012, 0.008, 0.019]
st_err = [0.045, 0.021, 0.014, 0.024]

x = np.arange(len(criteria))
width = 0.35

fig, ax = plt.subplots(figsize=(7, 4.2), dpi=300)
rects1 = ax.bar(x - width/2, s1_values, width, yerr=s1_err, capsize=4,
                label='First-Order ($S_1$)', color='#2b5c8f', edgecolor='black', linewidth=0.8)
rects2 = ax.bar(x + width/2, st_values, width, yerr=st_err, capsize=4,
                label='Total-Effect ($S_T$)', color='#d95f02', edgecolor='black', linewidth=0.8)

ax.set_ylabel('Sobol Sensitivity Index Value')
ax.set_title('Global Sensitivity Variance Decomposition across Criteria Weights')
ax.set_xticks(x)
ax.set_xticklabels(criteria)
ax.axhline(0, color='grey', linewidth=0.8, linestyle='--')
ax.set_ylim(-0.05, 1.05)
ax.legend(frameon=True, loc='upper right')
ax.grid(axis='y', linestyle=':', alpha=0.6)

for rect in rects1:
    h = rect.get_height()
    if h > 0.03:
        ax.annotate(f'{h:.3f}', xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=8.5)
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.3f}', xy=(rect.get_x() + rect.get_width()/2, h),
                xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=8.5)

plt.tight_layout()
plt.savefig('figures/fig1_sobol_decomposition.png')
plt.close()
print("Saved figures/fig1_sobol_decomposition.png")

# ==============================================================================
# Figure 2: Empirical Scaling & Convergence (MC vs IQAE)
# ==============================================================================
sample_sizes = np.array([64, 128, 256, 512, 1024, 2048, 4096])
mc_errors = np.array([0.03783, 0.02465, 0.01881, 0.01189, 0.00883, 0.00572, 0.00436])

qae_queries = np.array([128, 512, 2048, 4096, 6144])
qae_errors = np.array([0.02759, 0.01420, 0.00685, 0.00342, 0.00074])

n_range = np.linspace(50, 8000, 200)
mc_theoretical = 0.3 / np.sqrt(n_range)
qae_theoretical = 3.5 / n_range

fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=300)
ax.loglog(sample_sizes, mc_errors, 'o', color='#1f77b4', markersize=6, label='Classical MC (Observed)')
ax.loglog(n_range, mc_theoretical, '-', color='#1f77b4', alpha=0.7, label=r'MC Bound $\mathcal{O}(1/\sqrt{N})$')

ax.loglog(qae_queries, qae_errors, 's', color='#d62728', markersize=6, label='IQAE (Observed)')
ax.loglog(n_range, qae_theoretical, '--', color='#d62728', alpha=0.7, label=r'Quantum Heisenberg Bound $\mathcal{O}(1/N)$')

ax.set_xlabel('Sample Count / Oracle Query Budget ($N$)')
ax.set_ylabel('Mean Absolute Error ($|E - E_{true}|$)')
ax.set_title('Empirical Convergence: Classical Monte Carlo vs. Iterative QAE')
ax.grid(True, which="both", ls=":", alpha=0.5)
ax.legend(frameon=True, loc='upper right')

plt.tight_layout()
plt.savefig('figures/fig2_quantum_vs_classical_scaling.png')
plt.close()
print("Saved figures/fig2_quantum_vs_classical_scaling.png")
