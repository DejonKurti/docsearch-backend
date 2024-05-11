<a name="br1"></a> 

Introduction to Algorithms: 6.006

Massachusetts Institute of Technology

September 28, 2021

Instructors: Mauricio Karchmer, Anand Natarajan, Julian Shun

Lecture 6: Binary Trees I

Lecture 6: Binary Trees I

Previous and New Goal

Operations O(·)

Sequence

Container Static

Dynamic

Data Structure

build(X)

get at(i) insert first(x) insert last(x) insert at(i, x)

set at(i,x) delete first() delete last()

delete at(i)

Array

Linked List

Dynamic Array

n

n

n

1

n

1

n

1

n

n

n

1<sub>(am)</sub>

n

n

n

Goal

n

log n

log n

log n

log n

Operations O(·)

Set

Container Static

Dynamic

Order

Data Structure

build(X)

find(k)

insert(x)

find min()

find prev(k)

delete(k)

find max()

find next(k)

Array

n

n log n

u

n

log n

1

n

n

1

n

1

u

n

n

log n

u

Sorted Array

Direct Access Array

Hash Table

n<sub>(avg)</sub>

1<sub>(avg)</sub>

1<sub>(am)(avg)</sub>

n

Goal

n log n

log n

log n

log n

log n

How? Binary Trees!

• Pointer-based data structures (like Linked List) can achieve worst-case performance

• Binary tree is pointer-based data structure with three pointers per node

• Node representation: node.{item, parent, left, right}

• Example:

1

2

3

4

5

\_\_\_\_\_\_\_\_<A>\_\_\_\_\_

\_\_<B>\_\_\_\_\_ <C> item

\_\_<D> <E>

<F>

node | <A> | <B> | <C> | <D> | <E> | <F> |

|

A

\-

|

B

|

C

|

D

|

E

|

F

|

parent |

| <A> | <A> | <B> | <B> | <D> |

left | <B> | <C> |

right | <C> | <D> |

\-

\-

| <F> |

\-

\-

|

|

\-

\-

|

|

|

\-

|



<a name="br2"></a> 

2

Lecture 6: Binary Trees I

Terminology

• The root of a tree has no parent (Ex: <A>)

• A leaf of a tree has no children (Ex: <C>, <E>, and <F>)

• The ancestors of a node <X> is the set of nodes reachable by following parent pointers.

• The descendants of a node <X> is the set of nodes reachable by following left or right

pointers.

• The Subtree rooted at <X> is the tree consisting of <X> and its descendants.

• Deﬁne depth(<X>) of node <X> in a tree rooted at <R> to be length of path from <X> to <R>

• Deﬁne height(<X>) of node <X> to be max depth of any node in the subtree rooted at <X>

• Idea: Design operations to run in O(h) time for root height h, and maintain h = O(log n)

• A binary tree has an inherent order: its traversal order

– every node in node <X>’s left subtree is before <X>

– every node in node <X>’s right subtree is after <X>

• List nodes in traversal order via a recursive algorithm starting at root:

– Recursively list left subtree, list self, then recursively list right subtree

– Runs in O(n) time, since O(1) work is done to list each node

– Example: Traversal order is (<F>, <D>, <B>, <E>, <A>, <C>)

• Right now, traversal order has no meaning relative to the stored items

• Later, assign semantic meaning to traversal order to implement Sequence/Set interfaces

Tree Navigation

• Find ﬁrst node in the traversal order of node <X>’s subtree (last is symmetric)

– If <X> has left child, recursively return the ﬁrst node in the left subtree

– Otherwise, <X> is the ﬁrst node, so return it

– Running time is O(h) where h is the height of the tree

– Example: ﬁrst node in <A>’s subtree is <F>

• Find successor of node <X> in the traversal order (predecessor is symmetric)



<a name="br3"></a> 

Lecture 6: Binary Trees I

– If <X> has right child, return ﬁrst of right subtree

3

– Otherwise, return lowest ancestor of <X> for which <X> is in its left subtree

– Running time is O(h) where h is the height of the tree

– Example: Successor of: <B> is <E>, <E> is <A>, and <C> is None



<a name="br4"></a> 

4

Lecture 6: Binary Trees I

Dynamic Operations

• Change the tree by a single item (only add or remove leaves):

– add a node after another in the traversal order (before is symmetric)

– remove an item from the tree

• Insert node <Y> after node <X> in the traversal order

– If <X> has no right child, make <Y> the right child of <X>

– Otherwise, make <Y> the left child of <X>’s successor (which cannot have a left child)

– Running time is O(h) where h is the height of the tree

1

2

3

4

<sup>• Example: In</sup>\_<sup>s</sup>\_<sup>e</sup>\_<sup>rt</sup>\_<sup>n</sup>\_<sup>o</sup><<sup>d</sup>A<sup>e</sup>>\_<sup><</sup>\_<sup>G> before <E> in traversal order</sup>

\_\_\_\_\_\_\_\_<A>\_\_

\_\_<B>\_\_\_\_\_ <C>

\_\_<D> \_\_<E>

\_\_<B>\_\_ <C> =>

\_\_<D> <E>

<F>

<F>

<G>

• Example: Insert node <H> after <A> in traversal order

1

\_\_\_\_\_\_\_\_<A>\_\_\_

\_\_<B>\_\_\_\_\_ <C> =>

\_\_<D> \_\_<E>

\_\_\_\_\_\_\_\_<A>\_\_\_\_\_

\_\_<B>\_\_\_\_\_ \_\_<C>

\_\_<D> \_\_<E> <H>

<F> <G>

2

3

4

<F>

<G>

• Delete the item in node <X> from <X>’s subtree

– If <X> is a leaf, detach from parent and return

– Otherwise, <X> has a child

∗ If <X> has a left child, swap items with the predecessor of <X> and recurse

∗ Otherwise <X> has a right child, swap items with the successor of <X> and recurse

– Running time is O(h) where h is the height of the tree

– Example: Remove <F> (a leaf)

1

2

3

4

\_\_\_\_\_\_\_\_<A>\_\_\_\_\_

\_\_<B>\_\_\_\_\_ \_\_<C> => \_\_<B>\_\_\_\_\_

\_\_<D> \_\_<E> <H> <D> \_\_<E> <H>

<F> <G> <G>

\_\_\_\_\_\_\_\_<A>\_\_\_\_\_

\_\_<C>

– Example: Remove <A> (not a leaf, so ﬁrst swap down to a leaf)

1

2

3

4

\_\_\_\_\_\_\_\_<A>\_\_\_\_\_

\_\_<B>\_\_\_\_\_

<D> \_\_<E> <H>

<G>

\_\_\_\_\_\_\_\_<E>\_\_\_\_\_

\_\_\_\_\_<E>\_\_\_\_\_

\_\_<C>

<D> <G> <H>

\_\_<C> => \_\_<B>\_\_\_\_\_

\_\_<C> => \_\_<B>\_\_

<D> \_\_<G> <H>

<A>



<a name="br5"></a> 

Lecture 6: Binary Trees I

5

Application: Set

• Idea! Set Binary Tree (a.k.a. Binary Search Tree / BST):

Traversal order is sorted order increasing by key

– Equivalent to BST Property: for every node, every key in left subtree ≤ node’s key ≤

every key in right subtree

• Then can ﬁnd the node with key k in node <X>’s subtree in O(h) time like binary search:

– If k is smaller than the key at <X>, recurse in left subtree (or return None)

– If k is larger than the key at <X>, recurse in right subtree (or return None)

– Otherwise, return the item stored at <X>

• Other Set operations follow a similar pattern; see recitation

Application: Sequence (in Lecture 7)

• Idea! Sequence Binary Tree: Traversal order is sequence order

• How do we ﬁnd i<sup>th node in traversal order of a subtree? Call this operation</sup> subtree at(i)

• Could just iterate through entire traversal order, but that’s bad, O(n)

• However, if we could compute a subtree’s size in O(1), then can solve in O(h) time

– How? Check the size n<sub>L</sub> of the left subtree and compare to i

– If i < n<sub>L</sub>, recurse on the left subtree

– If i > n , recurse on the right subtree with i0 = i − n − 1

L

L

– Otherwise, i = n , and you’ve reached the desired node!

L

• Maintain the size of each node’s subtree at the node via augmentation

– Add node.size ﬁeld to each node

– When adding new leaf, add +1 to a.size for all ancestors a in O(h) time

– When deleting a leaf, add −1 to a.size for all ancestors a in O(h) time

• Sequence operations follow directly from a fast subtree at(i) operation

• Naively, build(X) takes O(nh) time, but can be done in O(n) time; see recitation



<a name="br6"></a> 

6

Lecture 6: Binary Trees I

So Far

Operations O(·)

Dynamic

insert(x)

delete(k)

h

Set

Container Static

Order

Data Structure build(X)

find(k)

find min()

find prev(k)

find next(k)

h

find max()

Binary Tree

n log n

h

h

Lecture 7

n log n

log n

log n

log n

log n

Operations O(·)

Sequence

Container Static

Dynamic

Data Structure build(X)

get at(i) insert first(x) insert last(x) insert at(i, x)

set at(i,x) delete first() delete last()

delete at(i)

Binary Tree

n

n

h

h

h

h

Lecture 7

log n

log n

log n

log n

Next Time

• Keep a binary tree balanced after insertion or deletion

• Reduce O(h) running times to O(log n) by keeping h = O(log n)

