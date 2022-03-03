import math
from functools import cache

# Reconstructing from subsequences

@cache
def get_maximal_deletion_ball_size(n, t, q=2):
    if n < t or t < 0:
        return 0
    if q == 1:
        return 1

    size = 0
    for i in range(t+1):
        size += math.comb(n-t, i) * get_maximal_deletion_ball_size(t, t-i, q-1)
    return size

@cache
def get_maximal_number_of_common_subsequences(n, t, q=2):
    if n <= t or t <= 0:
        return 0
    return get_maximal_deletion_ball_size(n,t,q) - get_maximal_deletion_ball_size(n-1,t,q) + get_maximal_deletion_ball_size(n-2,t-1,q)

def get_subsequence_reconstruction_threshold(n, t, order_comp, q=2):
    for i in range(q):
        w_i = order_comp[i]
        tau_i = get_maximal_number_of_common_subsequences(n-i-1,t-i,q)
        if w_i > tau_i:
            return i

# Reconstructing from supersequences

@cache
def get_maximal_insertion_ball_size(n, t, q=2):
    if n < 0 or t < 0:
        return 0
    size = 0
    for i in range(t+1):
        size += math.comb(n+t, i)*int(math.pow((q-1),i))
    return size

@cache
def get_maximal_number_of_common_supersequences(n, t):
    if t <= 0:
        return 0
    result = 0
    for i in range(1, t+1):
        result += get_maximal_insertion_ball_size(n,t-i)
    return 2*result

def get_supersequence_resonstruction_threshold(n, t, m_v):
    for i in range(t+1):
        w_i = m_v[i]
        tau_i = get_maximal_number_of_common_supersequences(n-1,t-i)
        if w_i > tau_i:
            return i