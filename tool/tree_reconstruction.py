from common_reconstruction import *
from ranked_trie import RankedTrieNode
import numpy as np
import copy

def get_u_a_i(U, a, i):
    root = RankedTrieNode()
    node = U
    for j in range(i-1):
        node = node.children[1-a]        
        if node is None:
            return root
    
    node = node.children[a]
    if node is None:
        return root

    root = copy.copy(node)
    root.char = -1
    
    return root

# Reconstructing from subsequences

def get_composition_vector(U):
    k = np.zeros_like(U.children)
    for i, child in enumerate(U.children):
        if child is None:
            k[i] = 0
        else:
            k[i] = child.size
    return k

def get_ordering(U):
    k = get_composition_vector(U)
    t = np.argsort(-k, kind='stable') # -k so it will be in descending order
    c = k[t]
    return t, c

def reconstruct_x_from_subsequences_tree(n, subsequences, verbose=0):
    t = n-subsequences.height
    N = get_maximal_number_of_common_subsequences(n,t)+1
    if subsequences.size < N:
        raise Exception(f"Not enough subsequences, need at least {N}")

    U = subsequences.decrease_size_to(N)
    reconstruction = np.array([], dtype=int)
    if verbose > 0:
        print(f"n={n}, t={t}, U.size={U.size}, U.height={U.height}")
    iteration_count = 0

    while t >= 1:
        iteration_count += 1
        order_perm, order_comp = get_ordering(U)
        j = get_subsequence_reconstruction_threshold(n, t, order_comp)
        reconstruction = np.concatenate((reconstruction, order_perm[:j+1]))
        if verbose > 1:
            print(f"threshold={j}, reconstructed={reconstruction}")

        n = n-j-1
        t = t-j    
        N = get_maximal_number_of_common_subsequences(n,t)+1
        U = get_u_a_i(U, order_perm[j], 1)
        U = U.decrease_size_to(N)
        if verbose > 1:
            print(f"n={n}, t={t}, U.size={U.size}, U.height={U.height}")
        
    if verbose > 0:
        print(f'Took {iteration_count} iterations')

    return np.concatenate((reconstruction, U.get_unique_path()))

# Reconstructing from supersequences

def get_m_vector(U, t, a):
    m_vec = np.zeros((t+1,), dtype=np.uint)
    for i in range(t+1):
        u_a_i = get_u_a_i(U, a, i+1)
        m_vec[i] = u_a_i.size

    return m_vec

def get_first_x(U, t):
    N = U.size
    candidates = []
    for i in range(2):
        m_v = get_m_vector(U, t, i)
        if m_v.sum() == N:
            candidates.append((i, m_v))

    if len(candidates) == 1:
        return candidates[0]

    U_0_1 = 0
    U_1_0 = 0

    if U.children[0] is not None:
        U_0_1 = U.children[0].size - (1 if U.contains_0_vector else 0)
    if U.children[1] is not None:
        U_1_0 = U.children[1].size - (1 if U.contains_1_vector else 0)

    # Since len(candidates)>1 then both 0 and 1 are candidates 
    # and because we added them by order candidates[0] represents 0
    if U_0_1 > U_1_0:
        return candidates[0] 
    
    return candidates[1]

def reconstruct_x_from_supersequences_tree(n, supersequences, verbose=0):
    t = supersequences.height-n
    N = get_maximal_number_of_common_supersequences(n,t)+1
    if supersequences.size < N:
        raise Exception(f"Not enough supersequences, need at least {N}")

    U = supersequences.decrease_size_to(N)

    reconstruction = np.array([], dtype=int)
    N = get_maximal_number_of_common_supersequences(n,t)+1
    if verbose > 0:
        print(f"n={n}, t={t}, U.size={U.size}, U.height={U.height}")
    iteration_count = 0

    while t >= 1:
        iteration_count += 1
        x_1, m_x_1 = get_first_x(U, t)
        reconstruction = np.append(reconstruction, x_1)
        if n == 1: 
            U = RankedTrieNode()
            break
        j = get_supersequence_resonstruction_threshold(n, t, m_x_1)
        if verbose > 1:
            print(f"threshold={j}, reconstructed={reconstruction}")

        U = get_u_a_i(U, x_1, j+1)
        n = n-1
        t = t-j  
        N = get_maximal_number_of_common_supersequences(n,t)+1
        U = U.decrease_size_to(N)
        if verbose > 1:
            print(f"n={n}, t={t}, U.size={U.size}, U.height={U.height}")
        
    if verbose > 0:
        print(f'Took {iteration_count} iterations')

    return np.concatenate((reconstruction, U.get_unique_path()))
