<a name="br1"></a> 

Introduction to Algorithms: 6.006

Massachusetts Institute of Technology

Oct. 1, 2019

Instructors: Mauricio Karchmer, Anand Natarajan, Julian Shun

Lecture 8: Binary Heaps

Lecture 8: Binary Heaps

Priority Queues

• New interface which implements a limited Set (intrinsic keyed order)

• Efﬁciently remove the most important item (highest key), optimize for build and space

– Example: router with limited bandwidth, must prioritize certain kinds of messages;

process scheduling in operating system kernels; graph algorithms (later in the course)

• Priority queue operations:

build(A)

build priority queue from iterable A

insert(x)

add item x to priority queue

delete max() remove and return the stored item with largest key

• (Usually max, can make a minimum priority queue via negation)

• Delete max only new operation: can be simulated via find max followed by a delete

• (If know n < m can get worst-case: array of size m, store length n of priority queue preﬁx)

Priority Queue Sort

• Additional Goal: in-place O(n log n) sorting algorithm

• Given a priority queue, we can use it to sort

• Build the priority queue on A (or insert items one at a time)

• Repeatedly remove and return the maximum element

• If build, insert, delete max have running times B, I, D, runs in min(B, n · I) + n · D

Priority Queue

Data Structure

Dynamic Array

Sorted Dynamic Array n log n

Balanced Binary Tree n log n log n

Operations O(·)

Priority Queue Sort

Time In-place?

build(A) insert(x) delete max()

n

1<sub>(a)</sub>

n

n

n<sup>2</sup>

n<sup>2</sup>

Y

Y

N

1<sub>(a)</sub>

log n

n log n

Goal

n

log n<sub>(a)</sub> log n<sub>(a)</sub> n log n

Y



<a name="br2"></a> 

2

Lecture 8: Binary Heaps

Priority Queue Sort: Array

• Maintain the ﬁrst k items as a priority queue implemented with an unsorted array

• insert take no time, just increase k by 1 to incorporate next item

• To delete max, ﬁnd max via linear search, swap to end and decrease k by 1

• insert is quick O(1), but delete max is slow O(n), runs in O(n<sup>2</sup>)

• This is exactly selection sort!

Priority Queue: Sorted Array

• Maintain the ﬁrst k items as a priority queue implemented with a sorted array

• insert takes linear time to put next item k + 1 in correct place in sorted order

• delete max takes no time (max is already at end) so just decrease k by 1

• Eventhough delete max is O(1), insert is slow O(n). Runs in O(n<sup>2</sup>)

• This is exactly insertion sort!

Balance Insert/Delete In-place

• Can we balance the cost of insertions and deletions?

• Yes! Use balanced binary tree: insert/delete in O(log n) time, sort in O(n log n) time

• Not in place (build a linked tree)

• Can we get O(n log n) sorting in-place, i.e., using at most O(1) additional space?

Array as a Complete Binary Tree

• Idea: interpret array (or array preﬁx) as a left-aligned complete binary tree

• A binary tree is complete if it is fully balanced: every level except last is full

• A binary tree is left-aligned if leaves in last level are packed to the left

• A binary tree is packed if it is complete and left-aligned

• There is exactly one left-aligned complete binary tree on n nodes for any n



<a name="br3"></a> 

Lecture 8: Binary Heaps

3

1

2

3

4

5

6

7

8

A = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]

|

|

|

|

heap prefix | k = 9

|

d0

d1

d2

d3

0

->

->

\_\_\_\_\_\_0\_\_\_\_

1 2

\_\_\_\_1\_\_\_\_ \_\_2\_\_

3 4 5 6

-> \_\_3\_\_ \_\_4

7 8 9 ->

5

6

7

8

9

• So there is a bijection between arrays and packed binary trees

• Height of packed tree perspective of array of n item is Θ(log n)

• Implicit tree: compute parent/left/right by index arithmetic (no need to store pointers!)

– Root is at index 0

ꢀ

ꢁ

– Parent of index i is at index <sup>i</sup>~~−~~1

2

– Left child of index i is at index 2i + 1

– Right child of index i is at index 2i + 2

Binary Heaps

• Idea: keep larger elements higher in tree, but only locally

– Node max-heap property (MHP) at i: Q[i] ≥ Q[left(i)], Q[right(i)]

– Tree max-heap property (Tree MHP) at i: Q[i] ≥ Q[j] for every index j ∈ S(i)

• A max-heap is an array where every node satisﬁes the node MHP

• Claim: Every node in max-heap satisﬁes the tree MHP

• Proof:

– Claim: If j is in subtree S(i) and d = depth(j) − depth(i), then Q[i] ≥ Q[j]

– Induction on d:

– Base case: d = 0 implies i = j implies Q[i] ≥ Q[i]

– depth(parent(j)) − depth(i) < d, so Q[i] ≥ Q[parent(j)] by induction

– Q[parent(j)] ≥ Q[j] by node MHP at parent(j)

• In particular, if MHP everywhere, max item is at root

• Note: Preﬁx of well-formed heap array is a well-formed heap array.



<a name="br4"></a> 

4

Lecture 8: Binary Heaps

Binary Heap Insert

• Given array satisfying MHP, how to insert an element?

– Append to end or expand preﬁx (next leaf)

– max heapify up: Swap with parent until MHP satisﬁed!

• max heapify up ﬁxes last element of otherwise well-formed heap.

• Correctness:

– MHP assumes all nodes ≥ descendants, except Q[c] might be > some ancestors

– If swap necessary, same assumption is true with Q[c] swapped with Q[p]

• Running time: height of tree, so O(log n)!

Binary Heap Delete Max

• Given array satisfying MHP, how to delete item with maximum key?

– Swap root to end and remove it, or reduce preﬁx

– max heapify down: Swap new root with its larger child until MHP satisﬁed!

• max heapify down: Fixes root of otherwise well-formed heap.

• Correctness:

– MHP assumes all nodes ≥ descendants, except Q[p] might be < some descendants

– if swap is necessary, same property holds with Q[p] swapped with Q[c]

Heap Sort

• Can insert and delete max, each in-place and in O(log n) time

• Yields heap sort, an in-place O(n log n) comparison sorting algorithm

Linear Build Heap

• To insert n items, each item is heapiﬁed down from root, worst-case is Ω(n log n) swaps:

X<sup>n−1</sup>

worst-case swaps ≈ lg i = lg(n!) = Ω(n log n)

i=0



<a name="br5"></a> 

Lecture 8: Binary Heaps

5

• Idea! Treat full array as a packed binary tree from start, then ﬁx MHP from leaves to root.

We have n/2<sup>k</sup> nodes of height k. For each, HEAPIFY-DOWN makes at most k swaps.

<sup>l</sup>X<sup>og n</sup>

X∞

n

n

worst-case swaps ≤

k ≤

k = 2n

2<sup>k</sup>

2<sup>k</sup>

k=1

k=1

P

(we are using ∞ kx<sup>k</sup> =

k=1

x

)

(1−x)<sup>2</sup>

• Uses at most O(n) swaps, so the heap can be built in linear time

