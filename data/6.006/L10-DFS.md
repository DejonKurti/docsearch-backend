<a name="br1"></a> 

Introduction to Algorithms: 6.006

Massachusetts Institute of Technology

October 12, 2021

Instructors: Mauricio Karchmer, Anand Natarajan, Julian Shun Lecture 10: Depth-First Search

Lecture 10: Depth-First Search

Previously

• Graph deﬁnitions (directed/undirected, simple, neighbors, degree)

• Graph representations (Set mapping vertices to adjacency lists)

• Paths and simple paths, path length, distance, shortest path

• Graph Path Problems

– Single Pair Reachability(G,s,t)

– Single Source Reachability(G,s)

– Single Pair Shortest Path(G,s,t)

– Single Source Shortest Paths(G,s) (SSSP)

• Breadth-First Search (BFS)

– algorithm that solves Single Source Shortest Paths

– with appropriate data structures, runs in O(|V | + |E|) time (linear in input size)

Examples

G<sub>1</sub>

G<sub>2</sub>

a

d

c

a

d

c

b

e

b

e

f

f

Depth-First Search (DFS)

• Searches a graph from a vertex s, similar to BFS

• Solves Single Source Reachability, not SSSP. Useful for solving other problems (later!)

• Return (not necessarily shortest) parent tree of parent pointers back to s

• Idea! Visit outgoing adjacencies recursively, but never revisit a vertex



<a name="br2"></a> 

2

Lecture 10: Depth-First Search

• i.e., follow any path until you get stuck, backtrack until ﬁnding an unexplored path to explore

• P(s) = None, then run visit(s), where

• visit(u) :

– for every v ∈ Adj+(u) that does not appear in P:

∗ set P(v) = u and recursively call visit(v)

– (DFS ﬁnishes visiting vertex u, for use later!)

• Example: Run DFS on G and/or G from a

1

2

Correctness

• Claim: DFS visits v and correctly sets P(v) for every vertex v reachable from s

• Proof: induct on k, for claim on only vertices within distance k from s

– Base case (k = 0): P(s) is set correctly for s and s is visited

– Inductive step: Consider vertex v with δ(s, v) = k0 + 1

– Consider vertex u, the second to last vertex on some shortest path from s to v

– By induction, since δ(s, u) = k0, DFS visits u and sets P(u) correctly

– While visiting u, DFS considers v ∈ Adj+(u)

– Either v is in P, so has already been visited, or v will be visited while visiting u

– In either case, v will be visited by DFS and will be added correctly to P

Running Time

• Algorithm visits each vertex u at most once and spends O(1) time for each v ∈ Adj(u)

P

• Work upper bounded by O(1) +

O(deg (u)) = O(|E|)

\+

u∈V

• Unlike BFS, not returning a distance for each vertex, so DFS runs in O(|E|) time

Full-BFS and Full-DFS

• Suppose want to explore entire graph, not just vertices reachable from one vertex

• Idea! Repeat a graph search algorithm A on any unvisited vertex

• Repeat the following until all vertices have been visited:



<a name="br3"></a> 

Lecture 10: Depth-First Search

– Choose an arbitrary unvisited vertex s, use A to explore all vertices reachable from s

3

• We call this algorithm Full-A, speciﬁcally Full-BFS or Full-DFS if A is BFS or DFS

• Visits every vertex once, so both Full-BFS and Full-DFS run in O(|V | + |E|) time

• Example: Run Full-DFS/Full-BFS on G<sub>1</sub> and/or G<sub>2</sub>

G<sub>1</sub>

G<sub>2</sub>

a

d

c

a

d

c

b

e

b

e

f

f

Graph Connectivity

• An undirected graph is connected if there is a path connecting every pair of vertices

• In a directed graph, vertex u may be reachable from v, but v may not be reachable from u

• Connectivity is more complicated for directed graphs (we won’t discuss in this class)

• Connectivity(G): is undirected graph G connected?

• Connected Components(G): given undirected graph G = (V, E), return partition of V

into subsets V ⊆ V (connected components) where each V is connected in G and there are

i

i

no edges between vertices from different connected components

• Consider a graph algorithm A that solves Single Source Reachability

• Claim: A can be used to solve Connected Components

• Proof: Run Full-A. For each run of A, put visited vertices in a connected component

Topological Sort

• A Directed Acyclic Graph (DAG) is a directed graph that contains no directed cycle.

• A Topological Order of a graph G = (V, E) is an ordering f on the vertices such that:

every edge (u, v) ∈ E satisﬁes f(u) < f(v).

• Exercise: Prove that a directed graph admits a topological ordering if and only if it is a DAG.

• How to ﬁnd a topological order?



<a name="br4"></a> 

4

Lecture 10: Depth-First Search

• A Finishing Order is the order in which a Full-DFS ﬁnishes visiting each vertex in G

• Claim: If G = (V, E) is a DAG, the reverse of a ﬁnishing order is a topological order

• Proof: Need to prove, for every edge (u, v) ∈ E that u is ordered before v,

i.e., the visit to v ﬁnishes before visiting u. Two cases:

– If u visited before v:

∗ Before visit to u ﬁnishes, will visit v (via (u, v) or otherwise)

∗ Thus the visit to v ﬁnishes before the visit to u ﬁnishes

– If v visited before u:

∗ u can’t be reached from v since graph is acyclic

∗ Thus the visit to v ﬁnishes before the visit to u ﬁnishes

• Topological sort takes O(|V | + |E|) time from calling Full-DFS.

Cycle Detection

• Full-DFS will ﬁnd a topological order if a graph G = (V, E) is acyclic

• If reverse ﬁnishing order for Full-DFS is not a topological order, then G must contain a cycle

• Check if G is acyclic: for each edge (u, v), check if v is before u in reverse ﬁnishing order

• Can be done in O(|E|) time via a hash table or direct access array

• To return such a cycle, maintain the set of ancestors along the path back to s in Full-DFS

• Claim: If G contains a cycle, Full-DFS will traverse an edge from v to an ancestor of v.

• Proof: Consider a cycle (v , v , . . . , v , v ) in G

0

1

k

0

– Without loss of generality, let v<sub>0</sub> be the ﬁrst vertex visited by Full-DFS on the cycle

– For each v , before visit to v ﬁnishes, will visit v and ﬁnish

i

i

i+1

– Will consider edge (v<sub>i</sub>, v<sub>i+1</sub>), and if v<sub>i+1</sub> has not been visited, it will be visited now

– Thus, before visit to v ﬁnishes, will visit v (for the ﬁrst time, by v assumption)

0

k

0

– So, before visit to v ﬁnishes, will consider (v , v ), where v is an ancestor of v

k

k

k

0

0

