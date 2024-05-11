<a name="br1"></a> 

Introduction to Algorithms: 6.006

Massachusetts Institute of Technology

October 21, 2021

Instructors: Mauricio Karchmer, Anand Natarajan, Julian Shun Lecture 12: Dijkstra’s Algorithm

Lecture 12: Dijkstra’s Algorithm

Weighted Graphs

• A weighted graph is a graph G = (V, E) together with a weight function w : E → R

• i.e., assigns each edge e = (u, v) ∈ E an integer weight: w(e) = w(u, v)

• Many applications for edge weights in a graph:

– distances in road network

– latency in network connections

– strength of a relationship in a social network

• Two common ways to represent weights computationally:

– Inside graph representation: store edge weight with each vertex in adjacency lists

– Store separate Set data structure mapping each edge to its weight

• We assume a representation that allows querying the weight of an edge in O(1) time

Examples

G<sub>1</sub>

−5

−1

5

a

e

c

b

d

6

9

7

−4

1

4

8

g

f

h

3

2

−2



<a name="br2"></a> 

2

Lecture 12: Dijkstra’s Algorithm

Weighted Paths

• The weight w(π) of a path π in a weighted graph is the sum of weights of edges in the path

• The (weighted) shortest path from s ∈ V to t ∈ V is path of minimum weight from s to t

• δ(s, t) = inf{w(π) | path π from s to t} is the shortest-path weight from s to t

• (Often use “distance” for shortest-path weight in weighted graphs, not number of edges)

• As with unweighted graphs:

– δ(s, t) = ∞ if no path from s to t

– Subpaths of shortest paths are shortest paths (or else could splice in a shorter path)

• Why inﬁmum not minimum? Possible that no ﬁnite-length minimum-weight path exists

• When? Can occur if there is a negative-weight cycle in the graph, Ex: (b, f, g, c, b) in G<sub>1</sub>

• A negative-weight cycle is a path π starting and ending at same vertex with w(π) < 0

• δ(s, t) = −∞ if there is a path from s to t through a vertex on a negative-weight cycle

• If this occurs, don’t want a shortest path, but may want the negative-weight cycle

• In the Singel Source Shortest Paths problems, when the source s is ﬁxed, we denote δ(v) =

δ(s, v).

Today

• Single-Source Shortest Paths on weighted graphs

• Today: Algorithm for graphs with non-negative edge weights, i.e., for e ∈ E, w(e) ≥ 0

Restrictions

SSSP Algorithm

Graph Weights

Name

Running Time O(·) Lecture

General Unweighted BFS

General Non-negative Dijkstra

DAG Any

General Any

|V | + |E| L09

|V | log |V | + |E| Today!

|V | + |E| L13

DAG Relaxation

Bellman-Ford

|V | · |E| L13



<a name="br3"></a> 

Lecture 12: Dijkstra’s Algorithm

3

Non-negative Edge Weights

• Idea! Generalize BFS approach to weighted graphs:

– Grow a sphere centered at source s

– Repeatedly explore closer vertices before further ones

– But how to explore closer vertices if you don’t know distances beforehand? :(

• Observation 1: If weights non-negative, monotonic distance increase along shortest paths

– i.e., if vertex u appears on a shortest path from s to v, then δ(s, u) ≤ δ(s, v)

– Let V ⊂ V be the subset of vertices reachable within distance ≤ x from s

x

– If v ∈ V , then any shortest path from s to v only contains vertices from V

x

x

– Perhaps grow V one vertex at a time! (but slow to consider every x if weights large)

x

• Observation 2: Can solve SSSP fast if given order of vertices in increasing distance from s

– Remove edges that go against this order (since cannot participate in shortest paths)

– May still have cycles if zero-weight edges: repeatedly collapse into single vertices

– Compute δ(s, v) for each v ∈ V using DAG relaxation in O(|V | + |E|) time



<a name="br4"></a> 

4

Lecture 12: Dijkstra’s Algorithm

Dijkstra’s Algorithm

• Named for famous Dutch computer scientist Edsger Dijkstra (actually Dy¨kstra!)

• Idea! Relax edges from each vertex in increasing order of distance from source s

• Idea! Efﬁciently ﬁnd next vertex in the order using a data structure

• Changeable Priority Queue Q on items with keys and unique IDs, supporting operations:

Q.build(X)

initialize Q with items in iterator X

Q.delete min()

remove an item with minimum key

Q.decrease key(id, k) ﬁnd stored item with ID id and change key to k

• Implement by cross-linking a Priority Queue Q0 and a Dictionary D mapping IDs into Q0

• Assume vertex IDs are integers from 0 to |V | − 1 so can use a direct access array for D

• For brevity, say item x is the tuple (x.id, x.key)

• Set d(v) = ∞ for all v ∈ V , then set d(s) = 0

• Build changeable priority queue Q with an item (v, d(v)) for each vertex v ∈ V

• While Q not empty, delete an item (u, d(u)) from Q that has minimum d(s, u)

– For vertex v in outgoing adjacencies Adj+(u):

∗ If d(v) > d(u) + w(u, v):

· Relax edge (u, v), i.e., set d(v) = d(u) + w(u, v)

· Decrease the key of v in Q to new estimate d(v)

• Run Dijkstra on example



<a name="br5"></a> 

Lecture 12: Dijkstra’s Algorithm

5

Example

Delete

d(v)

v from Q

s

a

b

c

d

2

a

c

G

s

b

s

c

0 ∞ ∞ ∞ ∞

10

3

10 ∞

7

3

∞

5

4

1

5

7

d

a

b

11

10

9

8

2

7

d

δ(v)

0

7

9

3

5

Correctness

• Claim: At end of Dijkstra’s algorithm, d(v) = δ(v) for all v ∈ V

• Proof:

– If relaxation sets d(v) to δ(v), then d(v) = δ(v) at the end of the algorithm

∗ Relaxation can only decrease estimates d(v)

∗ Relaxation is safe, i.e., maintains that each d(v) is weight of a path to v (or ∞)

– Sufﬁces to show d(v) = δ(v) when vertex v is removed from Q

∗ Proof by induction on ﬁrst k vertices removed from Q

∗ Base Case (k = 1): s is ﬁrst vertex removed from Q, and d(s) = 0 = δ(s)

∗ Inductive Step: Assume true for k < k0, consider k0th vertex v0 removed from Q

∗ Consider some shortest path π from s to v0, with w(π) = δ(v0)

∗ Let (x, y) be the ﬁrst edge in π where y is not among ﬁrst k<sup>0</sup> − 1 (perhaps y = v0)

∗ When x was removed from Q, d(x) = δ(x) by induction, so:

d(y) ≤ δ(x) + w(x, y) relaxed edge (x, y) when removed x

= δ(y)

subpaths of shortest paths are shortest paths

non-negative edge weights

0

≤ δ(v )

0

relaxation is safe

≤ d(v )

0 in

≤ d(y)

v<sup>0 is vertex with minimum</sup> d(s, v )

Q

∗ So d(v0) = δ(v0), as desired



<a name="br6"></a> 

6

Lecture 12: Dijkstra’s Algorithm

Running Time

• Count operations on changeable priority queue Q, assuming it contains n items:

Operation

Time Occurrences in Dijkstra

B<sub>n</sub>

M<sub>n</sub> |V |

Q.build(X) (n = |X|)

Q.delete min()

1

Q.decrease key(id, k) D<sub>n</sub> |E|

• Total running time is O(B<sub>|V |</sub> + |V | · M<sub>|V |</sub> + |E| · D<sub>|V |</sub>)

• Assume pruned graph to search only vertices reachable from the source, so |V | = O(|E|)

Priority Queue Q0

on n items

Q Operations O(·)

Dijkstra O(·)

build(X) delete min() decrease key(id, k) n = |V | = O(|E|)

Array

n

n

n

n

1

|V |<sup>2</sup>

Binary Heap

Fibonacci Heap

log n<sub>(a)</sub>

log n<sub>(a)</sub>

log n

1<sub>(a)</sub>

|E| log |V |

|E| + |V | log |V |

• If graph is dense, i.e., |E| = Θ(|V |<sup>2</sup>), using an Array for Q0 yields O(|V |<sup>2</sup>) time

• If graph is sparse, i.e., |E| = Θ(|V |), using a Binary Heap for Q0 yields O(|V | log |V |) time

• A Fibonacci Heap is theoretically good in all cases, but is not used much in practice

• We won’t discuss Fibonacci Heaps in 6.006 (see 6.854 or CLRS chapter 19 for details)

• Yo u should assume Dijkstra runs in O(|E|+|V | log |V |) time when using in theory problems

