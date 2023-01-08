import numpy as np
from itertools import combinations

dat = np.loadtxt('nn_sites')

def get_unique_ion_indices(N_nn=1, vasp_ids=True):
  """
  Considering the twelve nearest neighbour lattice points about a central lattice point
  (indexed as point 0) in an FCC lattice, this function obtains a group of indices sets
  (including the central point, 0) corresponding to the unique / symmetry-inequivalent
  way to choose a set of N_nn nearest neighbour lattice points.

  This problem can also be thought of as the ways in which we can pick N_nn unique vertices
  of a cuboctahedron.

  Args:
      N_nn (int)    : Number of nearest neighbours.
      vasp_ids (boo): Whether or not the indices correspond to the VASP POSCAR file's for a 
                      2 x 2 x 2 supercell of an 8-atom conventional cell of MgO.
  """
  sets_of_dists = []
  # start with all '12 C N_nn' combinations and collect the set of
  # pairwise distances associated with each combination
  for combo in combinations(dat, N_nn):
      pairwise_dists = []
      # calculate pairwise distances
      for pairs in combinations(combo, 2):
          pairwise_dists.append(np.sum((pairs[0][2:] - pairs[1][2:])**2))  # actually dist^2
      pairwise_dists.sort()
      if vasp_ids:
          ions = [60,] + [int(ion[1]) for ion in combo]
      else:
          ions = [0,] + [int(ion[0]) for ion in combo]
      ions.sort()
      sets_of_dists.append((tuple(ions), tuple(pairwise_dists)))

  # get unique set of pairwise distances
  unique_dist_combos = set([dists for id, dists in sets_of_dists])

  # iterate over all combinations to get a set of symmetry-inequivalent ion positions 
  # based on the set of unique pairwise distances
  unique_ion_pos = []
  for unique_dist_combo in unique_dist_combos:
      for set_of_dist in sets_of_dists:
          if set_of_dist[1] == unique_dist_combo:
              unique_ion_pos.append(set_of_dist[0])
              break
  return unique_ion_pos
