import time
import numpy as np
from argparse import ArgumentError, ArgumentParser
import ranked_trie
import base_reconstruction
import tree_reconstruction

def parse_line(line):
    seq = np.fromstring(line, dtype=int, sep=' ')
    if np.count_nonzero((seq != 0) & (seq != 1)) > 0:
        raise Exception("There exists a non-binary sequence")

    return seq

def construct_trie_from_sequence_file(sequence_file):
    seq_len = -1
    trie = ranked_trie.RankedTrieNode()
    for line in sequence_file:
        seq = parse_line(line)
        if seq_len == -1:
            seq_len = seq.size
        elif seq_len != seq.size:
            raise ArgumentError("Sequence file contains sequences of different lengths.")
        trie.insert_sequence(seq)

    return trie, seq_len

def construct_matrix_from_sequence_file(sequence_file):
    seq_len = -1

    sequences = []

    for line in sequence_file:
        seq = parse_line(line)
        if seq_len == -1:
            seq_len = seq.size
        elif seq_len != seq.size:
            raise ArgumentError("Sequence file contains sequences of different lengths.")
        
        sequences.append(seq)

    mat = np.array(sequences, dtype=int)

    return mat, seq_len

def run_with_trie(n, sequence_file_path):
    x = None
    trie = None
    seq_len = -1

    with open(sequence_file_path, 'r') as sequence_file:
        start = time.perf_counter()
        trie, seq_len = construct_trie_from_sequence_file(sequence_file)
        end = time.perf_counter()

    print(f"Constructing the trie took {(end-start)*1000:0.4f} ms.")

    if seq_len == n:
        print("Can't reconstruct a sequence from sequences of the same size as n")
        return

    if seq_len > n:
        print("Reconstructing x from supersequences trie")
        start = time.perf_counter()
        x = tree_reconstruction.reconstruct_x_from_supersequences_tree(n, trie) 
        end = time.perf_counter()
    else:
        print("Reconstructing x from subsequences trie")
        start = time.perf_counter()
        x = tree_reconstruction.reconstruct_x_from_subsequences_tree(n, trie) 
        end = time.perf_counter()

    print(f"Reconstruction took {(end-start)*1000:0.4f} ms. Result:")
    print(x)

def run_with_matrix(n, sequence_file_path):
    mat = None
    with open(sequence_file_path, 'r') as sequence_file:
        start = time.perf_counter()
        mat, seq_len = construct_matrix_from_sequence_file(sequence_file)
        end = time.perf_counter()

    print(f"Constructing the matrix took {(end-start)*1000:0.4f} ms.")

    if seq_len == n:
        print("Can't reconstruct a sequence from sequences of the same size as n")
        return

    if seq_len > n:
        print("Reconstructing x from supersequences matrix")
        start = time.perf_counter()
        x = base_reconstruction.reconstruct_x_from_supersequences(n, mat) 
        end = time.perf_counter()
    else:
        print("Reconstructing x from subsequences matrix")
        start = time.perf_counter()
        x = base_reconstruction.reconstruct_x_from_subsequences(n, mat) 
        end = time.perf_counter()

    print(f"Reconstruction took {(end-start)*1000:0.4f} ms. Result:")
    print(x)

def create_parser():
    parser = ArgumentParser(description="Reconstruct a binary sequence from a list of sub/super-sequences")
    parser.add_argument("n", type=int, help="Original sequence size")
    parser.add_argument("sequences_file", help="A file containing binary sub/super-sequences of the original sequence of the same length, each sequence 0 1 seperated by a space")
    parser.add_argument("-t", "--trie", action='store_true', default=False, help="Store sequences in a trie, by default stores as a matrix")
    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if args.trie:
        run_with_trie(args.n, args.sequences_file)
    else:
        run_with_matrix(args.n, args.sequences_file)