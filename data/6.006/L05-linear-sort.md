<a name="br1"></a> 

Introduction to Algorithms: 6.006

Massachusetts Institute of Technology

September 23, 2021

Instructors: Mauricio Karchmer, Anand Natarajan, Julian Shun

Lecture 5: Linear Sorting

Lecture 5: Linear Sorting

Review

• Comparison search lower bound: any decision tree with n nodes has height ≥ dlg(n+1)e−1

• Can do faster using random access indexing: an operation with linear branching factor!

• Direct access array is fast, but may use a lot of space (Θ(u))

• Solve space problem by mapping (hashing) key space u down to m = Θ(n)

• With the simple uniform hashing assumption, hash tables give average-case O(1) time

operations, amortized if dynamic

• Data structure overview!

• Last time we achieved faster ﬁnd. Can we also achieve faster sort?

Operations O(·)

Container Static

Dynamic

Order

Data Structure

build(A)

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



<a name="br2"></a> 

2

Lecture 5: Linear Sorting

Comparison Sort Lower Bound

• Comparison model implies that algorithm decision tree is binary (constant branching factor)

• Requires # leaves L ≥ # possible outputs

• Tree height lower bounded by Ω(log L), so worst-case running time is Ω(log L)

• To sort array of n elements, # outputs is n! permutations

• Thus height lower bounded by log(n!) ≥ log((n/2)<sup>n/2</sup>) = Ω(n log n)

• So merge sort is optimal in comparison model

• Can we exploit a direct access array to sort faster?

Direct Access Array Sort

• Example: [5, 2, 7, 0, 4]

• Suppose all keys are unique non-negative integers in range {0, . . . , u − 1}, so n < u

• Insert each item into a direct access array with size u in Θ(n)

• Return items in order they appear in direct access array in Θ(u)

• Running time is Θ(u), which is Θ(n) if u = Θ(n). Yay!

1

2

def direct\_access\_sort(A):

"Sort A assuming items have distinct non-negative keys"

u = 1 + max([x.key for x in A]) # O(n) find maximum key

3

4

D = [None] \* u

for x in A:

\# O(u) direct access array

\# O(n) insert items

5

6

D[x.key] = x

i = 0

7

8

for key in range(u):

if D[key] is not None:

A[i] = D[key]

i += 1

\# O(u) read out items in order

9

10

11

• What if keys are in larger range, like u < n<sup>2</sup>?

• Idea! Represent each key k by tuple (a, b) where k = an + b and 0 ≤ b < n

• Speciﬁcally a = bk/nc < n and b = (k mod n) (just a 2-digit base-n number!)

• This is a built-in Python operation (a, b) = divmod(k, n)

• Example: [17, 3, 24, 22, 12] =⇒ [(3,2), (0,3), (4,4), (4,2), (2,2)]

• How can we sort tuples?



<a name="br3"></a> 

Lecture 5: Linear Sorting

3

Tuple Sort

• Item keys are tuples of equal length, i.e. item x.key = (x.k , x.k , x.k , . . .).

1

2

2

• Want to sort on all entries lexicographically, so ﬁrst digit k<sub>1</sub> is most signiﬁcant

• How to sort? Idea! Use other auxiliary sorting algorithms to separately sort each key

• (Like sorting rows in a spreadsheet by multiple columns)

• What order to sort them in? Least signiﬁcant to most signiﬁcant!

• Exercise: [32, 03, 44, 42, 22] =⇒ [42, 22, 32, 03, 44] =⇒ [03, 22, 32, 42, 44]

• Idea! Use tuple sort with auxiliary direct access array sort to sort tuples (a, b).

• Wrong! Many integers could have the same a or b value, even if input keys distinct

• Need sort allowing repeated keys which preserves input orders

• Want sort to be stable: repeated keys appear in output in same order as input

• Direct access array sort cannot even sort arrays having repeated keys!

• Can we modify direct access array sort to admit multiple keys in a way that is stable?

Counting Sort

• Instead of storing a single item at each array index, store a chain, just like hashing!

• For stability, chain data structure should remember the order in which items were added

• Use a sequence data structure which maintains insertion order (speciﬁcally, a queue)

• To insert item x, add to the end of the chain at index x.key

• Then to sort, read through all chains in sequence order, returning items one by one

1

2

def counting\_sort(A):

"Sort A assuming items have non-negative keys"

u = 1 + max([x.key for x in A]) # O(n) find maximum key

3

4

D = [[] for i in range(u)]

for x in A:

\# O(u) direct access array of chains

\# O(n) insert into chain at x.key

5

6

D[x.key].append(x)

i = 0

7

8

for chain in D:

for x in chain:

A[i] = x

\# O(u) read out items in order

9

10

11

i += 1



<a name="br4"></a> 

4

Lecture 5: Linear Sorting

Radix Sort

• Use tuple sort with auxiliary counting sort to sort tuples (a, b)

• Sort least signiﬁcant digit b, then most signiﬁcant digit a

• Stability ensures that previous sorts stay sorted

• Running time for this algorithm is O(2n) = O(n). Yay!

• If every key < n<sup>c</sup> for some positive c = log<sub>n</sub>(u), every key has at most digits base n

• A c-digit number can be written as a c-element tuple

• So tuple sort with auxiliary counting sort runs in O(cn) time

• If c is constant, and each key is < n<sup>c</sup>, this sort is linear O(n)!

1

2

def radix\_sort(A):

"Sort A assuming items have non-negative keys"

n = len(A)

3

4

u = 1 + max([x.key for x in A])

c = 1 + (u.bit\_length() // n.bit\_length())

class Obj: pass

D = [Obj() for a in A]

for i in range(n):

\# O(n) find maximum key

\# O(nc) make digit tuples

\# O(c) make digit tuple

5

6

7

8

9

D[i].digits = []

D[i].item = A[i]

high = A[i].key

for j in range(c):

10

11

12

13

14

15

16

17

18

19

20

high, low = divmod(high, n)

D[i].digits.append(low)

for i in range(c):

\# O(nc) sort each digit

\# O(n) assign key i to tuples

for j in range(n):

D[j].key = D[j].digits[i]

counting\_sort(D)

\# O(n) sort on digit i

\# O(n) output to A

for i in range(n):

A[i] = D[i].item

Algorithm

Time O(·) In-place? Stable? Comments

Insertion Sort

Selection Sort

Merge Sort

n<sup>2</sup>

n<sup>2</sup>

Y

Y

N

Y

Y

Y

O(nk) for k-proximate

Y

O(n) swaps

n log n

n + u

N

N

N

stable, optimal comparison

u = Θ(n) is domain of possible keys

u = Θ(n<sup>c</sup>) is domain of possible keys

Counting Sort

Radix Sort n + n log<sub>n</sub>(u)

