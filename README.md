PyThermal - Thermal equilibrium of hard-core bosons on a 2D crystal lattice
---------------------------------------------------------------------------
PyThermal v2.2.0


**Thermalization and Quantum Entanglement Project Group, St. Stephen's Centre for Theoretical Physics**

*Project Mentor - Dr. A. Gupta*   
*Project Students - A. Kumar, D. Pinto and M. Ghosh*

## Current Status
PyThermal has been branched. The [cython](https://github.com/dkpinto/PyThermal/tree/cython) aims to significantly improve performance. Currently in beta.

[Open issues](https://github.com/dkpinto/PyThermal/issues) has further details.


## Programmers Notes 

*Documentation by D. Pinto*

The code is centered around the main functions (main_time() & main_states()). From which the entire program can be controlled. It derives data from a class which is used to store (and process) initial values. 

The source code consists of:

1. main.py - Overall control of program, program execution begins and ends here
2. routines.py - Set of 19 functions for simulating the hard-core bosons on a 2D lattice
3. output.py - Set of 8 functions to control Input/Output for files (csv) and images (png)
4. about.py - Set of 4 functions to check hardware, dependencies and test OpenBLAS, NumPy and SciPy
5. gui.py (Alpha) - Set of 3 functions forming a graphical interface for PyThermal

This code requires the following modules:

1. NumPy & SciPy (Recommended build against Fortran OpenBLAS libraries for parallel processing)
2. Matplotlib 
3. Multiprocessing
4. Tqdm
5. Tkinter(Py2) or tkinter(Py3) (for graphical interface)

Execute without graphical interface: `python3 main.py`

Execute with graphical interface: `python3 gui.py`

To manually control the threads used by OpenBLAS, call OpenMP when running the program:

        OMP_NUM_THREADS=16 python3 main.py 

or  

        OMP_NUM_THREADS=16 python3 gui.py 
        

**Note:** the code was designed on Python 2.7 and will not work with versions older than Python 2.6. Care has been taken to make it fully compatible with Python 3.x (no modifications necessary). [PEP8](https://www.python.org/dev/peps/pep-0008/) styling guidelines have been strictly followed throughout the code.  


## Previous build(s)

All further changelogs are shifted to [commit logs](https://github.com/dkpinto/pythermal/commits/master).

### Changelog (21/1/2015)
1. Function eigenstates() rewritten to account for missing lattice sites, site deletion controlled by [lat_del_pos]
2. Function nos() deprecated, nos replaced with len(c) in eigenstates()
3. Changed Hamiltonian, using if conditions to place 1's(on numpy.zeros matrix)

### Changelog (15/2/2015)

4. Parallel processing of hamiltonian() governed by distribution function distribute()
5. Parallel processing carried out using Process function from multiprocessing library
6. multiprocessing.queue to store output of each process and clear(optional, improves stability) it afterwards

### Changelog (1/3/2015)

7. Replaced math.fabs() with abs()
8. Added elif and else statements

### Changelog (16/4/2015)

9. la.eig replaced with la.eigh to exploit symmetry of Hamiltonian matrix
10. Original (la.eig)eigenvalvec() deprecated, replaced with (la.eigh)eigenvalvec()

### Changelog (23/15/2015)

11. Separate timers for hamiltonian() and eigenvalvec()
12. Sizes of all arrays printed
13. Output printed to file("LOG.txt") using tabulate

### Changelog (26/6/2015)

14. OpenBLAS(/opt/OpenBLAS) linkage of Numpy(and consequently Scipy) in virtualenv "pyenv" [for SSCTP workstation]
15. Program down-dated to work with Python 2.x
16. Functions ncr(), sum_ncr(), relabel() and denmatrix() added
17. la.eigh deprecated, la.eig reinstated to generate complex eigenvectors
18. Hamiltonian np.zeros switched to np.float32 data type
19. else condition(in hamiltonian_2d) now with continue statements

### Changelog (6/7/2015)

20. Direct call to hamiltonian_2d deprecated
21. Output made more verbose
22. Function ncr() deprecated

### Changelog (19/8/2015)

23. Parallel processing of Von-Neumann entropy calculation and time-evolution (using OpenBLAS linkage with OpenMP for multiple threads sidesteps Python GIL)
24. Trace of density matrix B = 1.95 (almost constant, only observed under 1D time evolution), instead of 1.00

### Changelog (13/9/2015)

25. Recursion time temporary fix using inverse of |least eigenvalue|
26. recursion_time(), gcd(), lcm(), lcm_call() added

### Changelog (1/10/2015)

27. Complete program structure redesign
28. class System created to store variables(defined in documentation)
29. Extensive documentation added 

### Changelog (15/12/2015)

30. Error checking for trace of density matrix (Permitted error = 1.0e-4) 
31. Write output to disk (.csv) during program run
32. Large eigenvalue problem fixed (within Main.py)

### Changelog (16/12/2015)

33. tqdm reinstated for measuring progress of time-evolution and entropy [loop counter tqdm.tqdm]
34. Error checking for trace of density matrix made non-fatal [program execution uninterrupted]
35. Verbose output to disk

### Changelog (16-12-2015) 

36. **eigenstates()** function shifted to SubRoutine1
37. Recursion time calculation added *[Beta]*
38. Full forward compatibility with both Python 3
39. Error checking now outputs to **stderr**

### Changelog (30-12-2015)

40. Lattice site deletion automated
41. Error checking for particles in sub lattice A
42. Von Neumann entropy output returned as 'real'
43. Function **write_file()** for saving to disk
44. Writing output made more verbose
