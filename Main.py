from __future__ import print_function, division

import math as mt
import sys
import time

import numpy as np

import Output
import SubRoutine1
import SubRoutine2
import SubRoutine3

__author__ = "Thermalization and Quantum Entanglement Project Group, St. Stephen's Centre for Theoretical Physics"


class System:
    def __init__(self):
        # No of particles
        self.nop = 2
        # Shape of square 2D array i.e. nsa = 2(2x2), 3(3x3)
        self.nsa = 4
        # No. of sites in sub-lattice A
        self.nol_a = 4
        # Time Evolution - starting time, ending time and no. of time steps
        self.t_initial = 0.0
        self.t_final = 10.0
        self.t_steps = 10

        # Check for number of particles in A
        if self.nop > self.nol_a:
            exit('Too many particles [{}] for sub-lattice A [{}]'.format(self.nop, self.nol_a))

        # Lattice sites to delete for particular values of nsa & nol_a
        self.lat_del_pos, self.lat_del_pos_a = self.lattice_generator()
        # No of  lattice sites eg. nsa = 3 => nol = 9
        self.nol = self.nsa * self.nsa
        # No. of sites in sub-lattice B
        self.nol_b = self.nol - (self.nol_a + len(self.lat_del_pos)) + 1
        # Site joining sub-lattice A and B (numbered after deleting sites)
        self.link_pos = mt.sqrt(self.nol_a) * self.nsa - (self.nsa - mt.sqrt(self.nol_a))
        # Lattice after deleting sites
        self.lat = np.arange(1, self.nol + 1, dtype=np.int32)
        # Time gap between successive steps
        self.delta_t = (self.t_final - self.t_initial) / self.t_steps
        # Time array
        self.timestep_array = np.arange(self.t_initial, self.t_final, self.delta_t)

    def lattice_generator(self):
        if self.nsa == 4 and self.nol_a == 4:
            self.lat_del_pos = np.array([3, 4, 9, 13])
            self.lat_del_pos_a = np.array([3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        elif self.nsa == 4 and self.nol_a == 9:
            self.lat_del_pos = np.array([4, 8, 13, 14])
            self.lat_del_pos_a = np.array([4, 8, 12, 13, 14, 15, 16])
        elif self.nsa == 5 and self.nol_a == 4:
            self.lat_del_pos = np.array([3, 4, 5, 11, 16, 21])
            self.lat_del_pos_a = np.array([3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                                           25])
        elif self.nsa == 5 and self.nol_a == 9:
            self.lat_del_pos = np.array([4, 5, 9, 10, 16, 17, 21, 22])
            self.lat_del_pos_a = np.array([4, 5, 9, 10, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
        elif self.nsa == 5 and self.nol_a == 16:
            self.lat_del_pos = np.array([5, 10, 15, 21, 22, 23])
            self.lat_del_pos_a = np.array([5, 10, 15, 21, 21, 22, 23, 24, 25])
        else:
            exit('Lattice shape not supported. Unable to delete sites.')
        return self.lat_del_pos, self.lat_del_pos_a

    # Define a unique folder to output to. Path is: Output/Case-(nop)_(nsa)_(nol_a)_(t_final)/
    def folder_path(self):
        name = 'Output/Case-{}_{}_{}_{}/'.format(self.nop, self.nsa, self.nol_a, self.t_final)
        return name


def main():
    s = System()

    Output.warning('Symmetry may still be present in lattice')

    # -----Sub-Routine 1 (Eigenstates, Hamiltonian, Eigenvalues and Eigenvectors)-----

    # Eigenstates
    eigenstates, nos = SubRoutine1.eigenstates_lattice(s.lat, s.nop, s.lat_del_pos)
    eigenstates_a, nos_a = SubRoutine1.eigenstates_lattice(s.lat, s.nop, s.lat_del_pos_a)
    Output.status(1)
    Output.write_file('Eigenstates.csv', eigenstates, fmt='%1d')

    # Hamiltonian
    h_time1 = time.time()
    hamiltonian = SubRoutine1.parallel_call_hamiltonian(eigenstates, nos, s.nsa, s.nop)
    hamiltonian_a = SubRoutine1.parallel_call_hamiltonian(eigenstates_a, nos_a, s.nsa, s.nop)
    h_time2 = time.time()
    Output.status(2, h_time2 - h_time1)
    Output.write_file('Hamiltonian.csv', hamiltonian, fmt='%1d')

    # Eigenvalues and Eigenvectors
    e_time1 = time.time()
    eigenvalues, eigenvectors = SubRoutine1.eigenvalvec(hamiltonian)
    eigenvalues_a, eigenvectors_a = SubRoutine1.eigenvalvec(hamiltonian_a)
    e_time2 = time.time()
    Output.status(3, e_time2 - e_time1)
    Output.write_file('Eigenvalues.csv', eigenvalues)
    Output.write_file('Eigenvectors.csv', eigenvectors)

    # ------Sub-Routine 2 (State Relabelling and Density Matrices)-----

    # State Relabelling
    r_time1 = time.time()
    relabelled_states = SubRoutine2.relabel(eigenstates, s.nop, s.link_pos, s.nol_b)
    r_time2 = time.time()
    Output.status(4, r_time2 - r_time1)
    Output.write_file('RelabelledStates.csv', eigenvalues)

    # -----Sub-Routine 3 (Time Evolution and Von-Neumann Entropy)-----

    # Time Evolution
    evo_time1 = time.time()
    psi_initial = SubRoutine3.random_eigenvector(eigenvectors_a, relabelled_states, nos, nos_a, s.nop)
    # psi_initial = eigenvectors[0] / la.norm(eigenvectors[0])
    psi_t = SubRoutine3.time_evolution(psi_initial, hamiltonian, nos, s.timestep_array)
    evo_time2 = time.time()
    Output.status(5, evo_time2 - evo_time1)
    Output.write_file('Psi.csv', psi_t)

    # Von-Neumann Entropy
    vn_time1 = time.time()
    vn_entropy_b, vn_trace2_b = SubRoutine3.von_neumann_b(psi_t, relabelled_states, nos, s.nol_b, s.nop)
    vn_time2 = time.time()
    Output.status(6, vn_time2 - vn_time1)
    Output.write_file('Entropy_B.csv', vn_entropy_b)

    # -----Output-----
    Output.plot_entropy(s.timestep_array, vn_entropy_b)
    Output.plot_trace2(s.timestep_array, vn_trace2_b)

    # -----Terminate-----
    Output.status(7)
    sys.exit()


if __name__ == '__main__':
    main()
