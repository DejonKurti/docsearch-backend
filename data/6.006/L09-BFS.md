<a name="br1"></a> 

Introduction to Algorithms: 6.006

Massachusetts Institute of Technology

October 7, 2021

Instructors: Mauricio Karchmer, Anand Natarajan, Julian Shun Lecture 9: Breadth-First Search

Lecture 9: Breadth-First Search

New Unit: Graphs!

• Today, start new unit, lectures L09 - L14 on Graph Algorithms

Graph Applications

• Why? Graphs are everywhere!

• any network system has direct connection to graphs

• e.g., road networks, computer networks, social networks

• the state space of any discrete system can be represented by a transition graph

• e.g., puzzle & games like Chess, Tetris, Rubik’s cube

• e.g., application workﬂows, speciﬁcations

Graph Deﬁnitions

G<sub>1</sub>

G<sub>2</sub>

G<sub>3</sub>

0

2

1

3

0

1

a

b

s

c

f

g

d

e

2

• Graph G = (V, E) is a set of vertices V and a set of pairs of vertices E ⊆ V × V .

• Directed edges are ordered pairs, e.g., (u, v) for u, v ∈ V

• Undirected edges are unordered pairs, e.g., {u, v} for u, v ∈ V i.e., (u, v) and (v, u)

• In this class, we assume all graphs are simple:

– edges are distinct, e.g., (u, v) only occurs once in E (though (v, u) may appear), and

– edges are pairs of distinct vertices, e.g., u = v for all (u, v) ∈ E

ꢀ ꢁ

ꢀ ꢁ

– Simple implies |E| = O(|V |<sup>2</sup>), since |E| ≤ |V | for undirected, ≤ 2 |V | for directed

2

2



<a name="br2"></a> 

2

Lecture 9: Breadth-First Search

Neighbor Sets/Adjacencies

• The outgoing neighbor set of u ∈ V is Adj<sup>+</sup>(u) = {v ∈ V | (u, v) ∈ E}

• The incoming neighbor set of u ∈ V is Adj<sup>−</sup>(u) = {v ∈ V | (v, u) ∈ E}

• The out-degree of a vertex u ∈ V is deg (u) = |Adj (u)|

\+

\+

• The in-degree of a vertex u ∈ V is deg (u) = |Adj (u)|

−

−

• For undirected graphs, Adj (u) = Adj (u) deg (u) = deg (u)

−

\+

and

−

\+

• Dropping superscript defaults to outgoing, i.e., Adj(u) = Adj<sup>+</sup>(u) deg(u) = deg<sup>+</sup>(u)

and

Graph Representations

• To store a graph G = (V, E), we need to store the outgoing edges Adj(u) for all u ∈ V

• First, need a Set data structure Adj to map u to Adj(u)

• Then for each u, need to store Adj(u) in another data structure called an adjacency list

• Common to use direct access array or hash table for Adj, since want lookup fast by vertex

• Common to use array or linked list for each Adj(u) since usually only iteration is needed<sup>1</sup>

• For the common representations, Adj has size Θ(|V |), while each Adj(u) has size Θ(deg(u))

P

• Since

deg(u) ≤ 2|E| by handshaking lemma, graph storable in Θ(|V | + |E|) space

u∈V

• Thus, for algorithms on graphs, linear time will mean Θ(|V | + |E|) (linear in size of graph)

Examples

• Examples 1 and 2 assume vertices are labeled {0, 1, . . . , |V | − 1}, so can use a direct access

array for Adj, and store Adj(u) in an array. Example 3 uses a hash table for Adj.

Ex 1 (Undirected) | Ex 2 (Directed) | Ex 3 (Undirected)

G1 = [

| G2 = [

[2],

[2, 0], # 1 |

| G3 = {

[2, 1], # 0 |

\# 0 |

a: [s, b], b: [a],

[2, 0, 3], # 1 |

[1, 3, 0], # 2 |

[1, 2], # 3 | ]

|

s: [a, c], c: [s, d, e],

d: [c, e, f], e: [c, d, f],

f: [d, e], g: [],

[1],

\# 2 |

|

]

| }

• Note that in an undirected graph, connections are symmetric as every edge is outgoing twice

<sup>1</sup>A hash table for each

Adj(u)

can allow checking for an edge

in

(u, v) ∈ E O(1)<sub>(avg)</sub>

time



<a name="br3"></a> 

Lecture 9: Breadth-First Search

3

Paths

• A path is a sequence of vertices p = (v , v , . . . , v ) where (v , v<sub>i+1</sub>) ∈ E for all 1 ≤ i < k.

1

2

k

i

• A path is simple if it does not repeat vertices<sup>2</sup>

• The length `(p) of a path p is the number of edges in the path

• The distance δ(u, v) from u ∈ V to v ∈ V is the minimum length of any path from u to v,

i.e., the length of a shortest path from u to v

(by convention, δ(u, v) = ∞ if u is not connected to v)

Graph Path Problems

• There are many problems you might want to solve concerning paths in a graph:

• SINGLE PAIR REACHABILITY(G, s, t): is there a path in G from s ∈ V to t ∈ V ?

• SINGLE PAIR SHORTEST PATH(G, s, t): return distance δ(s, t), and

a shortest path in G = (V, E) from s ∈ V to t ∈ V

• SINGLE SOURCE SHORTEST PATHS(G, s): return δ(s, v) for all v ∈ V , and

a shortest-path tree containing a shortest path from s to every v ∈ V (deﬁned below)

• Each problem above is at least as hard as every problem above it

(i.e., you can use a black-box that solves a lower problem to solve any higher problem)

• We won’t show algorithms to solve all of these problems

• Instead, show one algorithm that solves the hardest in O(|V | + |E|) time!

Shortest Paths Tree

• How to return a shortest path from source vertex s for every vertex in graph?

• Many paths could have length Ω(|V |), so returning every path could require Ω(|V |<sup>2</sup>) time

• Instead, for all v ∈ V , store its parent P(v): second to last vertex on a shortest path from s

• Let P(s) be null (no second to last vertex on shortest path from s to s)

• Set of parents comprise a shortest paths tree with O(|V |) size!

(i.e., reversed shortest paths back to s from every vertex reachable from s)

<sup>2</sup>A path in 6.006 is a “walk” in 6.042. A “path” in 6.042 is a simple path in 6.006.



<a name="br4"></a> 

4

Lecture 9: Breadth-First Search

Breadth-First Search (BFS)

• How to compute δ(s, v) and P(v) for all v ∈ V ?

• Store δ(s, v) and P(v) in Set data structures mapping vertices v to distance and parent

• (If no path from s to v, do not store v in P and set δ(s, v) to ∞)

• Idea! Explore graph nodes in increasing order of distance

• Goal: Compute level sets L<sub>i</sub> = {v | v ∈ V and d(s, v) = i} (i.e., all vertices at distance i)

• Claim: Every vertex v ∈ L<sub>i</sub> must be adjacent to a vertex u ∈ L<sub>i−1</sub> (i.e., v ∈ Adj(u))

• Claim: No vertex that is in L<sub>j</sub> for some j < i, appears in L<sub>i</sub>

• Invariant: δ(s, v) and P(v) have been computed correctly for all v in any L<sub>j</sub> for j < i

• Base case (i = 1): L<sub>0</sub> = {s}, δ(s, s) = 0, P(s) = None

• Inductive Step: To compute L<sub>i</sub>:

– for every vertex u in L<sub>i−1</sub>

:

∗ for every vertex v ∈ Adj(u) that does not appear in any L for j < i:

j

· add v to L , set δ(s, v) = i, and set P(v) = u

i

• Repeatedly compute L from L for j < i for increasing i until L is the empty set

i

j

i

• Set δ(s, v) = ∞ for any v ∈ V for which δ(s, v) was not set

• Breadth-ﬁrst search correctly computes all δ(s, v) and P(v) by induction

• Running time analysis:

– Store each L in data structure with Θ(|L |)-time iteration and O(1)-time insertion

i

i

(i.e., in a dynamic array or linked list)

– Checking for a vertex v in any L<sub>j</sub> for j < i can be done by checking for v in P

– Maintain δ and P in Set data structures supporting dictionary ops in O(1) time

(i.e., direct access array or hash table)

– Algorithm adds each vertex u to ≤ 1 level and spends O(1) time for each v ∈ Adj(u)

P

– Work upper bounded by O(1) ×

deg(u) = O(|E|) by handshake lemma

u∈V

– Spend Θ(|V |) at end to assign δ(s, v) for vertices v ∈ V not reachable from s

– So breadth-ﬁrst search runs in linear time! O(|V | + |E|)

• Run breadth-ﬁrst search from s in the graph in Example 3

