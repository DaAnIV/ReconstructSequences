from common_reconstruction import *
import numpy as np

def get_u_a_i(U, a, i):
    if i == 1:
        return U[:,U[0,:] == a][1:]
    results = []
    for s in U.T:
        if len(np.where(s == a)[0]) == 0: continue
        if np.where(s == a)[0][0] == i-1:
            results.append(s)

    if len(results) == 0:
        return None
    
    return np.stack(results).T[i:]

# Reconstructing from subsequences

def get_composition_vector(x, q):
    k = np.zeros(q,dtype=int)
    for i in x:
        k[i] += 1
    return k

def get_ordering(x, q=2):
    k = get_composition_vector(x, q)
    t = np.argsort(-k, kind='stable') # -k so it will be in descending order
    c = k[t]
    return t, c

def reconstruct_x_from_subsequences(n, subsequences, q=2, verbose=0):
    t = n-subsequences.shape[1]
    N = get_maximal_number_of_common_subsequences(n,t,q)+1
    if subsequences.shape[0] < N:
        raise Exception(f"Not enough subsequences, need at least {N}")
    U = subsequences[:N].T
    

    reconstruction = np.array([], dtype=int)
    if verbose > 0:
        print(f"n={n}, t={t}, U.shape={U.shape}")
    iteration_count = 0

    while t >= 1:
        iteration_count += 1
        order_perm, order_comp = get_ordering(U[0], q)
        j = get_subsequence_reconstruction_threshold(n, t, order_comp, q)
        reconstruction = np.concatenate((reconstruction, order_perm[:j+1]))
        if verbose > 1:
            print(f"threshold={j}, reconstructed={reconstruction}")

        n = n-j-1
        t = t-j    
        N = get_maximal_number_of_common_subsequences(n,t,q)+1
        U = get_u_a_i(U, order_perm[j], 1)
        U = U[:,:N]
        if verbose > 1:
            print(f"n={n}, t={t}, U.shape={U.shape}")
        
    if verbose > 0:
        print(f'Took {iteration_count} iterations')

    return np.concatenate((reconstruction, U.T[0]))

# Reconstructing from supersequences

def get_m_vector(U, t, a):
    m_vec = np.zeros((t+1,), dtype=np.uint)
    for i in range(t+1):
        u_a_i = get_u_a_i(U, a, i+1)
        if u_a_i is None:
            m_vec[i] = 0
        else:
            m_vec[i] = u_a_i.shape[1]

    return m_vec

def get_first_x(supersequences, t):
    N = supersequences.shape[1]
    candidates = []
    for i in range(2):
        m_v = get_m_vector(supersequences, t, i)
        if m_v.sum() == N:
            candidates.append((i, m_v))

    if len(candidates) == 1:
        return candidates[0]

    U_0_1 = 0
    U_1_0 = 0

    for s in supersequences.T:
        indices_0 = np.where(s == 0)[0]
        indices_1 = np.where(s == 1)[0]
        if len(indices_0) == 0 or len(indices_1) == 0: continue
        if indices_0[0] < indices_1[0]:
            U_0_1 += 1
        else:
            U_1_0 += 1

        # Since len(candidates)>1 then both 0 and 1 are candidates 
        # and because we added them by order candidates[0] represents 0
    if U_0_1 > U_1_0:
        return candidates[0] 
    
    return candidates[1]

def reconstruct_x_from_supersequences(n, supersequences, verbose=0):
    t = supersequences.shape[1]-n
    N = get_maximal_number_of_common_supersequences(n,t)+1
    if supersequences.shape[0] < N:
        raise Exception(f"Not enough supersequences, need at least {N}")

    U = supersequences[:N].T
    reconstruction = np.array([], dtype=int)
    if verbose > 0:
        print(f"n={n}, t={t}, U.shape={U.shape}")
    iteration_count = 0

    while t >= 1:
        iteration_count += 1
        x_1, m_x_1 = get_first_x(U, t)
        reconstruction = np.append(reconstruction, x_1)
        if n == 1:
            U = None 
            break
        j = get_supersequence_resonstruction_threshold(n, t, m_x_1)
        if verbose > 1:
            print(f"threshold={j}, reconstructed={reconstruction}")

        U = get_u_a_i(U, x_1, j+1)
        n = n-1
        t = t-j  
        N = get_maximal_number_of_common_supersequences(n,t)+1
        U = U[:,:N]
        if verbose > 1:
            print(f"n={n}, t={t}, U.shape={U.shape}")
        
    if verbose > 0:
        print(f'Took {iteration_count} iterations')
        
    if U is None:
        return reconstruction
    return np.concatenate((reconstruction, U.T[0]))
