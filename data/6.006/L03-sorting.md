<a name="br1"></a> 

Introduction to Algorithms: 6.006

Massachusetts Institute of Technology

Instructors: Mauricio Karchmer, Anand Natarajan, Julian Shun

September 16, 2021

Lecture 3: Sorting

Lecture 3: Sorting

Sorting

• Given a sorted array, we can leverage binary search to make an efﬁcient set data structure.

• But how can we sort an array?

• Input: (static) array A of n numbers. More generally: an array of n records with keys that

can be compared. (E.g. students in 6.006, where each record is keyed by a student’s name,

and contains the student’s assignments. Keys are compared in alphabetical order.)

• Output: (static) array B which is a sorted permutation of A

– Permutation: array with same elements in a different order

– Sorted: B[i − 1] ≤ B[i] for all i ∈ {1, . . . , n}

• Example: [8, 2, 4, 9, 3] → [2, 3, 4, 8, 9]

• A sort is in place if it uses O(1) extra space

• A sort is stable if it preserves the input order of elements with equal keys. (Not important

for this lecture, but will be in L05!)

• Brute-force sorting by trying all permutations of A takes time O(n!·n) which is exponential—

unacceptable! Instead, we will try to ﬁnd an efﬁcient recursive algorithm.

Solving Recurrences

To analyze the runtime of a recursive algorithm, we usually have to solve a recurrence equation

for the runtime. For instance, the recurrence for binary search or 1D peak ﬁnding is

T(n) = O(1) + T(n/2).

There are three main techniques for doing this.

• Substitution: Guess a solution, replace with representative function, recurrence holds true.

• Recurrence Tree: Draw a tree representing the recursive calls label each node with the

amount of work done in the corresponding call. Sum up the values of all the nodes to get the

total value.

• Master Theorem: A formula to solve many recurrences asymptotically (R03). (You can

prove the Master Theorem using the previous two techniques).



<a name="br2"></a> 

2

Lecture 3: Sorting

Insertion Sort

• Recursively sort preﬁx A[:i]

• Sort preﬁx A[:i + 1] assuming that preﬁx A[:i] is sorted by repeatedly swapping A[i+1]

backwards until it is in the correct place.

• Example: [8, 2, 4, 9, 3], [2, 8, 4, 9, 3], [2, 4, 8, 9, 3], [2, 4, 8, 9, 3], [2, 3, 4, 8, 9]

1

2

def insertion\_sort(A, i = None):

’’’Sort A[:i + 1]’’’

if i is None: i = len(A) - 1

if i > 0:

\# T(i)

3

\# O(1)

\# O(1)

4

5

insertion\_sort(A, i - 1)

insert\_last(A, i)

\# T(i - 1)

\# S(i)

6

7

8

def insert\_last(A, i):

\# S(i)

9

’’’Sort A[:i + 1] assuming sorted A[:i]’’’

10

11

12

if i > 0 and A[i] < A[i - 1]:

A[i], A[i - 1] = A[i - 1], A[i]

insert\_last(A, i - 1)

\# O(1)

\# O(1)

\# S(i - 1)

• insert last analysis:

– Base case: for i = 0, array has one element so is sorted

– Induction: assume correct for i, if A[i] >= A[i - 1], array is sorted; otherwise,

swapping last two elements allows us to sort A[:i] by induction

– S(1) = Θ(1), S(n) = S(n − 1) + Θ(1) =⇒ S(n) = Θ(n)

• insertion sort analysis:

– Base case: for i = 0, array has one element so is sorted

– Induction: assume correct for i, algorithm sorts A[:i] by induction, and then

insert last correctly sorts the rest as proved above

– T(1) = Θ(1), T(n) = T(n−1) + Θ(n) =⇒ T(n) = Θ(n<sup>2</sup>). (Recall 1+2+· · ·+n =

n(n + 1)/2 = Θ(n<sup>2</sup>).)

– Insertion sort is in place: just need O(1) extra space to swap.

– Insertion sort is stable. Exercise: what if line 10 in insert last had a ≤ instead of

<?



<a name="br3"></a> 

Lecture 3: Sorting

3

Merge Sort

• A divide and conquer algorithm: recursively sort ﬁrst half and second half.

• Merge sorted halves into one sorted list. To merge, use the “two ﬁnger algorithm”: initialize

two indices pointing to the end of both lists. At each step, pick the larger of the two indexed

values, add it to the merged list, and move the corresponding index back by one.

• Example: [7, 1, 5, 6, 2, 4, 9, 3], [1, 7, 5, 6, 2, 4, 3, 9], [1, 5, 6, 7, 2, 3, 4, 9], [1, 2, 3, 4, 5, 6, 7, 9]

1

2

def merge\_sort(A, a = 0, b = None):

’’’Sort A[a:b]’’’

\# T(b - a = n)

3

if b is None: b = len(A)

if 1 < b - a:

\# O(1)

\# O(1)

4

5

c = (a + b + 1) // 2

\# O(1)

6

merge\_sort(A, a, c)

merge\_sort(A, c, b)

L, R = A[a:c], A[c:b]

merge(L, R, A, len(L), len(R), a, b)

\# T(n / 2)

\# T(n / 2)

\# O(n)

7

8

9

\# S(n)

10

11 def merge(L, R, A, i, j, a, b):

\# S(b - a = n)

\# O(1)

12

13

14

15

16

17

18

19

20

’’’Merge sorted L[:i] and R[:j] into A[a:b]’’’

if a < b:

if (j <= 0) or (i > 0 and L[i - 1] > R[j - 1]): # O(1)

A[b - 1] = L[i - 1]

i = i - 1

else:

A[b - 1] = R[j - 1]

j = j - 1

merge(L, R, A, i, j, a, b - 1)

\# O(1)

\# O(1)

\# O(1)

\# O(1)

\# O(1)

\# S(n - 1)

• merge analysis:

– Base case: for n = 0, arrays are empty, so vacuously correct

– Induction: assume correct for n, item in A[r] must be a largest number from remaining

preﬁxes of L and R, and since they are sorted, taking largest of last items sufﬁces;

remainder is merged by induction

– S(0) = Θ(1), S(n) = S(n − 1) + Θ(1) =⇒ S(n) = Θ(n)

• merge sort analysis:

– Base case: for n = 1, array has one element so is sorted

– Induction: assume correct for k < n, algorithm sorts smaller halves by induction, and

then merge merges into a sorted array as proved above.

– T(1) = Θ(1), T(n) = 2T(n/2) + Θ(n)

∗ Substitution: Guess T(n) = Θ(n log n)

cn log n = Θ(n) + 2c(n/2) log(n/2) =⇒ cn log(2) = Θ(n)



<a name="br4"></a> 

4

Lecture 3: Sorting

∗ Recurrence Tree: complete binary tree with depth log n and n leaves, level i has 2<sup>i</sup>

P

2

P

nodes with O(n/2<sup>i</sup>) work each, total: <sup>log n</sup>(2<sup>i</sup>)(n/2<sup>i</sup>) = <sup>log n</sup> n = Θ(n log n)

2

i=0

2

i=0

∗ Master theorem: try this out in recitation!

• Merge sort is not in-place: the merge step requires Θ(n) extra space!

• <sub>m</sub>M<sub>e</sub>e<sub>r</sub>r<sub>g</sub>ge<sub>e?</sub>s<sub>)</sub>ort is stable. (Again, what happens if you have L[i − 1] ≥ R[j − 1] in line 14 of

2D peak ﬁnding

As a more complex example of a divide and conquer algorithm, let us consider a two-dimensional

version of peak ﬁnding.

• Input: an n × m array of integers.

• Output: the index (i, j) of a cell that is a peak, i.e. whose values are greater than or equal

to the values in neighboring cells.

The straighforward scan algorithm takes time Θ(n · m). But, as in the 1D case, there is a better

divide and conquer algorithm, though it is not quite as fast as the 1D one!

Intuitively, we want to divide the 2D array into smaller subarrays, and determine which subar-

ray must contain a peak. Let’s ﬁrst be modest in our ambitions: we want the subarrays to be half

the size of the full array. We can achieve this by taking the subarrays to be the left half (the ﬁrst

m/2 columns) and the right half (the remaining m/2 columns) of the whole array.

How do we tell which of these contains a peak? Inpsired by the 1D case, we should look at the

midpoint between the two subarrays. Let us modify the construction: let j<sub>midpoint</sub> = bm/2c, and

let the left subarray be A[:, 0 : j<sub>midpoint</sub>], and the right subarray be A[:, j<sub>midpoint</sub> + 1 : m], so that

column j<sub>midpoint</sub> does not lie in either subarray. We will now determine whether a peak lies in the

left subarray, the midpoint column, or the right subarray, as follows.

• First, ﬁnd the row index i∗ of a maximum element in the midpoint column (any one will

midpoint

do). Check if A[i∗, j

] is a peak in A. If it is, return (i∗, j<sub>midpoint</sub>).

• If not: then A[i∗, j<sub>midpoint</sub>] must have a neighbor that is strictly greater than it. This neighbor

cannot lie along the midpoint column, because we assumed that this cell was a maximum of

the column. Hence, it must be either the left or the right neighbor of the cell. Recursively

call the peak-ﬁnding procedure on the left or right subarray accordingly.

Let us analyze this algorithm. We must show that it is correct, which we shall do by induction

on m, the number of columns. (This is the right variable to do induction on since it decreases in

every recursive call.)

• Base case: for m = 1, it is clear that the algorithm is correct, since it returns a maximum of

the array, which is necessarily a peak.



<a name="br5"></a> 

Lecture 3: Sorting

5

• Inductive hypothesis: let us assume that the algorithm is correct for all arrays of up to m − 1

columns. Moreover, we will assume that the value returned by the algorithm is a maximum

of its column.

• Inductive step: We would like to prove that the algorithm is correct for an input of m

columns, and that the returned value is a maximum of its column. There are three cases.

– Case 1: the maximum of the midpoint column that was found is in fact a peak of A. In

this case, the algorithm is clearly correct since it returns this element as a peak, and the

returned value is clearly a maximum of its column by construction.

– Case 2: the maximum A[i∗, j<sub>midpoint</sub>] of the midpoint column has a strictly larger neigh-

bor A[i∗, j<sub>midpoint</sub> − 1] to the left. In this case, we recursively call the algorithm on the

left subarray, and obtain an index (i, j) of a cell. We must argue that this cell is a peak

in A. By the inductive hypothesis, we know that A[i, j] is a peak in the left subarray,

and is a maximum of the column j. There are now two subcases:

∗ If j = j

− 1, then this automatically implies that A[i, j] is a peak in A, and

midpoint

we are done.

∗ If j = j

− 1, then we must check that A[i, j] is greater than or equal to its

midpoint

midpoint

neighbor to the right, A[i, j

]. However, we know that A[i, j] is a maximum

of column j. In particular, we know that

A[i, j] ≥ A[i<sup>∗</sup>, j].

Moreover, we assumed above that A[i∗, j] > A[i∗, j<sub>midpoint</sub>], and since A[i∗, j<sub>midpoint</sub>]

is a maximum in column j<sub>midpoint</sub>, we conclude that

A[i, j] ≥ A[i, j<sub>midpoint</sub>].

Thus, it is greater than or equal to its right neighbor, and therefore it is a peak in

the entire array A.

– Case 3: the maximum A[i∗, j<sub>midpoint</sub>] of the midpoint column has a strictly larger neigh-

bor A[i∗, j<sub>midpoint</sub>+1] to the right. This case is entirely symmetric to the previous case,

so we omit it.

This is a pretty complicated inductive proof, but in broad outline it’s similar to the 1D case. It’s

worth trying to modify the algorithm and trying to ﬁnd if the proof breaks. For instance, if instead

of ﬁnding a maximum of the midpoint column, we just ﬁnd a (1D) peak, is the algorithm still

correct?

We conclude with a runtime analysis. Observe that we have the following recurrence relation

T(n, m) = Θ(n) + T(n, m/2)

T(n, 1) = Θ(n).

This can be easily solved with the substitution method, or the tree method, to obtain

T(n, m) = Θ(n log m).


