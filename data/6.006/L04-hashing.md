<a name="br1"></a> 

Introduction to Algorithms: 6.006

Massachusetts Institute of Technology

Instructors: Mauricio Karchmer, Anand Natarajan, Julian Shun

September 21, 2021

Lecture 4: Hashing

Lecture 4: Hashing

Review

Operations O(·)

Container Static Dynamic

Order

Data Structure build(X) find(k) insert(x) find min() find prev(k)

delete(k) find max() find next(k)

Array

n

n

n

n

n

n

Sorted Array

n log n log n

1

log n

• Idea! Want faster search and dynamic operations. Can we find(k) faster than Θ(log n)?

• Answer is no (lower bound)! (But actually, yes...!?)

Comparison Model

• In this model, assume algorithm can only differentiate items via comparisons

• Comparable items: black boxes only supporting comparisons between pairs

• Comparisons are <, ≤, >, ≥, =, =, outputs are binary: True or False

• Goal: Store a set of n comparable items, support find(k) operation

• Running time is lower bounded by # comparisons performed, so count comparisons!

Decision Tree

• Any algorithm can be viewed as a decision tree of operations performed

• An internal node represents a binary comparison, branching either True or False

• For a comparison algorithm, the decision tree is binary (draw example)

• A leaf represents algorithm termination, resulting in an algorithm output

• A root-to-leaf path represents an execution of the algorithm on some input

• Need at least one leaf for each algorithm output, so search requires ≥ n + 1 leaves



<a name="br2"></a> 

2

Lecture 4: Hashing

Comparison Search Lower Bound

• What is worst-case running time of a comparison search algorithm?

• running time ≥ # comparisons ≥ max length of any root-to-leaf path ≥ height of tree

• What is minimum height of any binary tree on ≥ n nodes?

• Minimum height when binary tree is complete (all rows full except last)

• Height ≥ dlg(n + 1)e − 1 = Ω(log n), so running time of any comparison sort is Ω(log n)

• Sorted arrays achieve this bound! Yay!

• More generally, height of tree with Θ(n) leaves and max branching factor b is Ω(log<sub>b</sub> n)

• To get faster, need an operation that allows super-constant ω(1) branching factor. How??

Direct Access Array

• Exploit Word-RAM O(1) time random access indexing! Linear branching factor!

• Idea! Give item unique integer key k in {0, . . . , u − 1}, store item in an array at index k

• Associate a meaning with each index of array

• If keys ﬁt in a machine word, i.e. u ≤ 2<sup>w</sup>, worst-case O(1) ﬁnd/dynamic operations! Yay!

• 6.006: assume input numbers/strings ﬁt in a word, unless length explicitly parameterized

• Anything in computer memory is a binary integer, or use (static) 64-bit address in memory

• But space O(u), so really bad if n ꢀ u... :(

• Example: if keys are ten-letter names, for one bit per name, requires 26<sup>10</sup> ≈ 17.6 TB space

• How can we use less space?

Hashing

• Idea! If n ꢀ u, map keys to a smaller range m = Θ(n) and use smaller direct access array

• Hash function: h(k) : {0, . . . , u − 1} → {0, . . . , m − 1} (also hash map)

• Direct access array called hash table, h(k) called the hash of key k

• If m ꢀ u, no hash function is injective by pigeonhole principle



<a name="br3"></a> 

Lecture 4: Hashing

3

• Always exists keys a, b such that h(a) = h(b) → Collision! :(

• Can’t store both items at same index, so where to store? Either:

– store somewhere else in the array (open addressing)

∗ complicated analysis, but common and practical

– store in another data structure supporting dynamic set interface (chaining)

Chaining

• Idea! Store collisions in another data structure (a chain)

• If keys roughly evenly distributed over indices, chain size is n/m = n/Ω(n) = O(1)!

• If chain has O(1) size, all operations take O(1) time! Yay!

• If not, many items may map to same location, e.g. h(k) = constant, chain size is Θ(n) :(

• Need good hash function! So what’s a good hash function?

Hash Functions

Division (bad):

h(k) = (k mod m)

• Heuristic, good when keys are uniformly distributed!

• m should avoid symmetries of the stored keys

• Large primes far from powers of 2 and 10 can be reasonable

• Python uses a version of this with some additional mixing

• If u ꢁ n, every hash function will have some input set that will a create O(n) size chain

• Any ﬁxed simple hash function can be attacked!

• To see how to design a provably good hash function using randomness, take 6.046.

In this class, we will use the following simplifying assumption.

Simple uniform hashing assumption (SUHA): Each key k maps to a uniformly random h(k) in

[0, . . . , m − 1], independently of any other keys.

•

\# elements

table size

n

load factor: α =

\=

m

• For random data, with chaining, the average chain size will be α, and thus all operations take

O(1 + α) average-case time.



<a name="br4"></a> 

4

Lecture 4: Hashing

Dynamic

• If α = n/m far from 1, rebuild the hash table for new size m

• Same analysis as dynamic arrays, cost can be amortized over many dynamic operations

• So a hash table can implement dynamic set operations in average amortized O(1) time! :)

Operations O(·)

Container Static

Dynamic

Order

Data Structure

build(X)

find(k)

insert(x)

find min() find prev(k)

find max() find next(k)

delete(k)

Array

n

n

n

n

1

n

1

n

log n

u

Sorted Array

Direct Access Array

Hash Table

n log n log n

u

1

u

n

n<sub>(avg)</sub>

1<sub>(avg)</sub>

1<sub>(am)(avg)</sub>

n

(avg) = average-case running time (averaged across random data)

(am) = amortized running time (averaged across a sequence of operations)

Open Addressing

Open addressing is a different way of dealing with collisions. Whereas in chaining we use a

different data structure to deal with collisions, in open addressing collisions are stored in the hash

table itself!

Different open addressing schemes are deﬁned by different probing strategies. A probing strat-

egy dictates which slot to try next if the particular slot being looked at is occupied with a different

key. Mathematically, an open addressing hashing scheme is deﬁned by a function (the probing

scheme)

h : U × {0, . . . , m − 1} → {0, . . . , m − 1}

For a given key k, we ﬁrst attempt to store k in h(k, 0), if occupied, we try h(k, 1), then h(k, 2)

and so on (see Figure 1).

Given a ﬁxed probing scheme h, how do we perform an insert, delete or search operation?

1\. INSERT: When inserting a key k, we just follow the probing scheme, in order, until we ﬁnd

an open slot. See Figure 2. In the example, we are inserting key 496.

2\. SEARCH: When searching for a key k, we again follow the probing scheme until we either

ﬁnd k, or we ﬁnd an empty slot. If we ﬁnd an empty slot, we report NOT FOUND.



<a name="br5"></a> 

Lecture 4: Hashing

5

Figure 1: A probing scheme

3\. DELETE: When deleting keys, one needs to use lazy-deleting. If one just deletes entries,

one may prevent existing keys from being found. Consider the example in Figure 2. If we

delete key 586, then we wouldn’t be able to ﬁnd key 496! Rather, instead of deleting an item,

we replace it with a special key (say −1). This special key is treated as “occupied” when

searching, but as “empty” when inserting.

Figure 2: Inserting a key

Assuming that the probing scheme function h can be evaluated in O(1) time and that proving

sequences are random, open addressing has similar performance to chaining, with some efﬁcien-



<a name="br6"></a> 

6

Lecture 4: Hashing

cies especially for small load factors. Yo u will learn more about speciﬁc probing schemes in

recitation.


