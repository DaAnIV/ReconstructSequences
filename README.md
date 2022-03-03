# Reconstruct Sequences
Efficient Reconstruction of Sequences from Their Subsequences or Supersequences based on Vladimir I. Levenshtein paper, Efficient Reconstruction of Sequences from Their Subsequences or Supersequences.

The algorithms presented in the paper and implemented here for the binary case can be used given enought subsequences or supersequences of the same length of some original sequence and knowledge of its original size to reconstruct it.

There are two implementations of the reconstruction algorithms presented in Levenshtein paper for the binary case.
- Implementation using an np.array to store the sub/super-sequences
- Implementation using a ranked trie to store the sub/super-sequences

## Tool Usage
In the tool folder there are python scripts which contain implementations of the algorithms to reconstruct an original binary sequence from a list of sub/super-sequences.

The sequences should be store as space seperated binary digit lines in a file. For example:
```
0 1 1 1 0 0 1
1 1 0 1 0 1 0
0 0 0 0 1 0 1
``` 
Or see the example files in the `tool/tests` directory.

To run the tool using a matrix  
```bash
python main.py <n> <file>
```
where \<n\> is the original sequence length and \<file\> is the sequences file

To run the tool using a trie
```bash
python main.py -t <n> <file>
```
where \<n\> is the original sequence length and \<file\> is the sequences file

## Example usage

Using the file `tool/tests/supersequences_10.txt` which is a list of supersequences of the original sequence
```
[0 1 1 0 1 0 0 1 0 1]
```

We run
```
python main.py 10 tests/supersequences_10.txt
```
to get
```
Constructing the matrix took 0.7100 ms.
Reconstructing x from supersequences matrix
Reconstruction took 11.9466 ms. Result:
[1 0 0 0 1 0 0 1 1 1]
```
or using a trie
```
python main.py -t 10 tests/supersequences_10.txt
```
to get
```
Constructing the trie took 27.4424 ms.
Reconstructing x from supersequences trie
Reconstruction took 0.7927 ms. Result:
[1 0 0 0 1 0 0 1 1 1]
```

You can also look at the `ConstructTests` notebook on how to create more tests with different arguments.

## Requirments
- numpy
- jupyter - for running the notebooks

You can use the `env.yml` to install a conda environment.


## Jupyter Notebooks
The two notebooks contain example of the algorithms flow and complexity analysis.

Both notebooks reconstruct random sequences using Levenshtein algorithms.

`BaseReconstructionAlgo.py` uses a np.array to store the sub/super-sequences which are used to construct the original sequence.

`TreeReconstructionAlgo.py` uses a trie to store the sub/super-sequences which are used to construct the original sequence.

## References
Based on the article\
Vladimir I. Levenshtein,\
Efficient Reconstruction of Sequences from Their Subsequences or Supersequences,\
Journal of Combinatorial Theory, Series A,\
Volume 93, Issue 2,\
2001,\
Pages 310-332,\
ISSN 0097-3165,\
https://doi.org/10.1006/jcta.2000.3081.
(https://www.sciencedirect.com/science/article/pii/S0097316500930814)\
Abstract: In the paper two combinatorial problems for the set Fnq of sequences of length n over the alphabet Fq={0, 1, …, q−1} are considered. The maximum size N−q(n, t) of the set of common subsequences of length n−t and the maximum size N+q(n, t) of the set of common supersequences of length n+t of two different sequences of Fnq are found for any nonnegative integers n and t. The number N−q(n, t)+1 (respectively, N+q(n, t)+1) is equal to the minimum number N of different subsequences of length n−t (supersequences of length n+t) of an unknown sequence X∈Fnq which are sufficient for its reconstruction. Simple algorithms to recover X∈Fnq from N−q(n, t)+1 of its subsequences of length n−t and from N+q(n, t)+1 of its supersequences of length n+t are given.
