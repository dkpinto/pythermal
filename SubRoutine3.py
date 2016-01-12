from __future__ import division, print_function

import warnings

import numpy as np
import scipy.linalg as la
from tqdm import tqdm

import SubRoutine2


# Returns a random eigenvector by placing eigenvectors from A in a zero matrix
def random_eigenvector(e_vecs, relabelled_states, nos, nos_a, nop):
    psi_initial = np.zeros(nos, dtype=np.complex)
    rand = np.random.randint(0, nos_a)
    j = 0
    for idx, val in enumerate(relabelled_states[:, 1]):
        if val == nop:
            psi_initial[idx] = e_vecs[rand][j]
            j += 1

    # print "\nEigenvector", rand, "chosen randomly for time evolution"
    psi_initial /= la.norm(psi_initial)
    return psi_initial


# Calculates Von-Neumann entropy as entropy = - tr(rho * ln(rho))
def von_neumann_b(psi_array, relabelled_states, nos, nol_b, nop):
    entropy_b = np.zeros(len(psi_array), dtype=np.complex)
    trace2_b = np.zeros(len(psi_array), dtype=np.float64)

    # [CAUTION] Replaces default warning, ignores future warnings within scope
    # Output.warning('The logm input matrix may be nearly singular')
    warnings.filterwarnings('ignore')

    for idx, psi_val in tqdm(enumerate(psi_array)):
        d_matrix_b, trace2_b[idx] = SubRoutine2.density_matrix_b(relabelled_states, psi_val, nos, nol_b, nop)
        entropy_b[idx] = -1.0 * np.trace(np.dot(d_matrix_b, la.logm(d_matrix_b)))

    return entropy_b.real, trace2_b


# Psi evolved as |psi(t)> = exp(-i * H * t)|psi(0)>
def time_evolution(psi_initial, hamiltonian, nos, timestep_array):
    psi_t = np.zeros(shape=(len(timestep_array), nos), dtype=np.complex)

    for idx, t in tqdm(enumerate(timestep_array)):
        psi_t[idx] = np.dot(la.expm(-1.0j * hamiltonian * t), psi_initial)

    return psi_t
