# Reconstruction of Sequences from Their Subsequences or Supersequences -implementations and improvements

In this project we used Vladimir I.Levenshtein's paper - Efficient Reconstruction of Sequences from Their Subsequences and Supersequences as a reference to implement the algorithms presented (specifically for $q=2$ alphabet size), and we tried to optimise them using Trie.

## Notations:

$x$ - original sequence we will attempt to reconstruct, $\left|x\right|=n$.

$N_{q}^{-}\left(n,t\right)$ - maximum number of common subsequences for a sequence of size $n$ with deletion ball radius of $t$ will be refered to as $N$ within the reconstruction from subsequences algorithm complexity evaluation.

for $q=2$:

$$N_{2}^{-}\left(n,t\right)=2\sum_{i=0}^{t-1}{n-t-1 \choose i}\leq2tn^{t}$$

$N_{q}^{+}\left(n,t\right)$ - maximum number of common supersequences for a sequence of size $n$ with insertion ball radius of $t$ will be refered to as $N$ within the reconstruction from supersequences algorithm complexity evaluation.

for $q=2$:

$$N_{2}^{+}\left(n,t\right)=2\sum_{i=0}^{t-1}{n+t-1 \choose i}\leq2tn^{t}$$

$U$ - set of sub/super-sequences of $x$.

$U^{a,i}$ - contains all $\left\{ s\in U\,|\,\text{the first occurence of {a} in {s} is in index {i}}\right\}$.

$\overline{U^{a,i}}$ - $\left\{ s'=\left(s_{i+1},s_{i+2},\dots,s_{n}\right)\,|\,s\in U^{a,i}\right\}$.

$m\left(a\right)$ - vector of size $t+1$ s.t $m\left(a\right)_{i}=\left|U^{a,i}\right|$.

## Documents: 

### **BaseReconstructionAlgo.ipynb**: 

In this file we implemented both algorithms presented in the paper naively, assuming that we get the sub/super-sequences as a matrix.

given a sequence $x$ of size $n$ and insertion/deletion ball of radius $t$:\
Reconstruction from subsequences complexity is $O\left(Nn+n^{2}t\right)\leq O\left(tn^{t+1}\right)$.

Reconstruction from supersequences complexity is $O\left(Nn^{2}+Nnt^{2}+n^{2}t^{3}\right)\leq O\left(t^{3}n^{t+2}\right)$.\

### **TreeReconstructionAlgo.ipynb**: 

In this file we assumed that the sub/super-sequences were stored using a sequence ranked tree (as described within the file), we managed to improve complexeties of both algorithms, while maintaining that subsequences in a datastructure that requires less memory.\
Improved Reconstruction from subsequences complexity is $O\left(n^{2}t\right)$.

Improved Reconstruction from supersequences complexity is $O\left(n^{2}t^{3}\right)$.
