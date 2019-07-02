import numpy as np

N = 10    # Length of Arithemetic Progressions
L = N*N   # Length of Interval {0,1,2,3...,L-1} containing progressions
M = 15    # Size of Set

# Define lexicographically least characteristic function of set of size M
arr = np.zeros((L,), dtype = np.bool)
arr[L-M:] = 1

# Produces characteristic function on {0,1,...,L_1} of an arithemtic progression
def arith_prog(start, step, length):
  return [( (i >= start) & (((i - start) % step) == 0) & (((i - start) // step) < length) ) for i in range(N*N)]

# Array of characteristic functions all arithmetic progressions
progs = np.array([arith_prog(start, step, N) for step in range(1,N+1) for start in range(L) if (step*(N-1) + start < L)])

# Array of maximal elements of corresponding arithmetic progressions
prog_maxs = np.array([start+((N-1)*step)     for step in range(1,N+1) for start in range(L) if (step*(N-1) + start < L)])

# Produces array of Boolean values representing whether each a.p. intersects the current set
def intersects(arrayofarrays, testarray):
  return np.any((arrayofarrays & testarray), axis=1)


# We think of 2^100 as branches of a tree, with linear order on branches given 
# by  x < y iff for some i all j < i we  have x(j) = y(j)  but x(i) < y(i).
# For a given M, we are concerned with the induced sub-order O_M of this given by 
# branches x for which |{i : x(i) = 1}| = M. Our problem amounts to: for which M
# is O_M non-empty?

# complete takes a branch in the binary tree of height N (represented as a binary array) and changes
# it to have exactly M ones by modifying the tail of the branch to have the form 1000...00111...11,
# (i.e. matching the regex 10*1*) but only if this can be done without modifying bits strictly before
# the pivot. If this is impossible, complete it returns False.
def complete(branch, pivot):
  k = M - np.sum(branch[:pivot]) # number of ones needed in the tail 
  if (k > 0) & (k <= (L-pivot)):
    branch[pivot] = 1
    branch[pivot+1:(L-k)+1] = 0
    branch[(L-k)+1:] = 1
    return True
  else:
    return False     # There aren't enough bits after the pivot

# pivot_next takes a branch in the complete binary tree of height N) and returns the least branch
# in the tree greater than the given branch satisfying:
#    (a) The resulting and input branch disagree at some point non-strictly below the pivot
#    (b) The resulting branch has exactly M ones.
# If this is impossible, pivot_next does nothing returns false.
def pivot_next(branch, pivot):
  if pivot < 0:
    return False  
  elif branch[pivot] == 0:
    if complete(branch, pivot):
      return True
    else:
      return pivot_next(branch, pivot-1)
  else:
    return pivot_next(branch, pivot-1)


def next(array, pivot):
  if np.all(array[:pivot+1]):
    return False
  else:
    return pivot_next(array, pivot)


def best_pivot(arrayofarrays, testarray):
  non_covered_ap_indices = np.logical_not(np.any((arrayofarrays & testarray), axis=1))
  if np.any(non_covered_ap_indices):
    return np.amin(prog_maxs[non_covered_ap_indices])
  else:
    return L-1

not_finished = True

def step(array):
  global not_finished
  not_finished = next(array, best_pivot(progs, array))
  if np.all(intersects(progs,array)):
    return True
  else:
    return False

def percent_traversed(branch):
  total = 0.0
  for i in range(L):
    total = total + (int(branch[i])*(2**(-i-1)))
  return total*100

def main():
  global not_finished
  solved = False
  steps = 0
  while (not_finished):
    if (steps % 1000 == 1):
      print(list(arr.astype(int)))
      print("Current Pivot: ", best_pivot(progs, arr))
      print("Percent Traversed: ", percent_traversed(arr))
    steps = steps+1
    solved = step(arr)
    if solved:
      not_finished = False
      print("Found solution!")
      print(list(arr.astype(int)))
  print('Finished!')
  if solved == False:
    print("Search found no solutions.")
