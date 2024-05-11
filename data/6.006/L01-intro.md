<a name="br1"></a> 

Introduction to Algorithms: 6.006

Massachusetts Institute of Technology

September 9, 2021

Instructors: Mauricio Karchmer, Anand Natarajan, Julian Shun

Lecture 1: Introduction

Lecture 1: Introduction

This class is an introduction to the design and analysis of algorithms and data structures. The

goals of the class are

• To teach you to think and communicate like an algorithmist: we will show you techniques

to design algorithms for many types of problems, and to logically argue that an algorithm is

correct and efﬁcient.

• To teach you a number of classic algorithms and data structures that are used widely in theory

and practice, and to let you implement them yourself in Python.

• To show how to recognize when a problem likely doesn’t have an efﬁcient algorithm

An example: peak ﬁnding

An algorithm is a procedure for solving a computational problem. In this class, we will want

algorithms that are correct and efﬁcient. By correct, we simply mean that the procedure gives the

correct answer on every possible input.

The notion of efﬁciency is a little bit more complicated. In this class, we’ll study efﬁciency

asymptotically: we’ll study how the resources used by the algorithm (mostly runtime, but also

space) scale asymptotically as a function of the size of the input, using the O and Ω notation.

Let’s make these ideas concrete with an example. The problem is called “peak ﬁnding.” To

specify a computaitonal problem, I have to tell you what the input and desired output are.

• Input: A list A of n integers.

• Output: The index i of an element in the list that is a “peak”: it is greater than or equal to

its neighbors (so A[i] ≥ A[i ± 1]). Note that if you’re on the ends of the list, you only have

one neighbor.

Now the zeroth question you should ask when you’re given a problem is whether it is well-

deﬁned. Does there always exist a “peak”? Any ideas why or why not?

Indeed, there is always a peak, because the global maximum (the largest element) of the list has

to be a peak. Now, let’s try to ﬁnd an algorithm. My preferred approach is always to start out by

ﬁnding the simplest correct algorithm you can, and then worrying about efﬁciency. I think you’ll

agree that the simplest possible algorithm is to just scan the whole array from beginning to end

until you hit a peak.

1

2

3

def is\_peak(A, i, n):

’’’

Determine whether element i is a peak of A



<a name="br2"></a> 

2

Lecture 1: Introduction

4

5

6

7

8

9

Input: list A of numbers, index i, length n

Output: boolean

’’’

return ( (i == 0 or A[i] >= A[i-1]) and (i == n-1 or A[i] >= A[i+1]))

10 def find\_peak(A):

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

’’’

Find the index of an element of A which is a peak (>= its neighbors)

Input: list A of numbers

Output: index of peak

’’’

n = len(A)

\# O(1)

for i in range(n):

if is\_peak(A, i, n):

return i

\# n

\# Peak found!

\# Should never happen!

return None

Is it correct? Obviously yes.

What about efﬁciency? Let’s forget about space/memory and just think about runtime. How

much time does it take for this algorithm to run? It’s hard to say because we could be lucky: the

peak could be at the very beginning of the list, and we’d terminate in just one step. However, we

could also be unlucky: the peak could be at the end of the list, in which case we’d have to scan

through the whole thing. In this class, the measure of runtime we use is the worst-case runtime:

the time it takes for the algorithm to run on the worst possible input. In math notation, if T(n, A)

is the time it takes for my algorithm to run on input A with length n, then the function I am trying

to bound is

T(n) = max T(n, A).

A:|A|=n

In this case, it is going to scale linearly with n, so we say that the runtime of this algorithm is Θ(n).

(Remember from 6.042: Θ(n) means both O(n) and Ω(n). So we’re saying the worst-case

runtime grows exactly as fast as a linear function—you can always sandwich it between two linear

functions.)

A better algorithm?

Linear runtime is nothing to sneeze at: it says that you can solve the problem in no more time than

it takes to just read through the whole input. But it turns out for this problem, we can do a lot

better! A hunch: being a peak is a weaker condition than being a global max. But a linear scan

through the array could just ﬁnd the global max outright! So maybe it is doing “too much” work?

That doesn’t tell us how to improve the algorithm. To do this, you have to be creative! But

you can draw inspiration from an algorithm you all already know. Does anyone remember binary

search?

As a reminder, binary search solves the following problem: given a list A of n numbers in

sorted order and a given number x, return the index i of x in A if it is present, or otherwise return



<a name="br3"></a> 

Lecture 1: Introduction

3

that it is absent. This problem could be solved in Θ(n) time with a linear scan, but binary search

does it in Θ(log(n)) time, by exploiting the sorted structure of the array. The logarithmic runtime

comes from the fact that binary search is a divide-and-conquer algorithm: in each step, it cuts

down the range of the array that needs to be searched by a half.

Here, for peak ﬁnding, the input data is totally unstructured. But there is some structure to

the notion of a peak. Can we do a divide and conquer algorithm here? Yes! The key observation

is this: suppose I observe that index i is not a peak of the array. This implies that either the left

neighbor of i or the right neighbor of i is strictly greater than it. I claim that whichever side this

neighbor lies on, there must be a peak in the corresponding subarray (i.e. A[0 : i] for the left, and

A[i + 1 : n] for the right). This is easiest to see if you imagine the values in the array as the graph

of some continuous function. If you keep on “climbing uphill,” you have to either reach a peak, or

reach the edge of the array!

So here is my algorithm: given the array A, take i = n/2, and check whether it is a peak. If

it is not, then recursively run the peak ﬁnding algorithm on the subarray in the “uphill” direction,

and return whatever it returns.

1

2

def find\_peak\_fast\_helper(A, start, end):

’’’

3

Find the index of an element of A[start:end] which is a peak (>= its neighbors)

Input: list of numbers, start and end indices

Output: index of peak

4

5

6

’’’

7

i = (start + end) // 2

8

if (i == start or A[i] >= A[i-1]):

if (i == end - 1 or A[i] >= A[i+1])):

return i # We found a peak!

else: # Right neighbor is greater

return find\_peak(A, i+1, end)

9

10

11

12

13

14

15

else: # Left neighbor is greater

return find\_peak(A, start, i - 1)

16 def find\_peak\_fast(A):

17

18

19

20

21

22

23

’’’

Find the index of an element of A which is a peak (>= its neighbors)

Input: list of numbers

Output: index of peak

’’’

n = len(A)

return find\_peak\_fast\_helper(A, 0, n)

Why is this correct? To formally prove this, we need to use mathematical induction, which

is the natural tool for analyzing recursion. As our base case, let’s take an array of one element:

it clearly works! So for a larger array of size n, assume that the algorithm performs correctly on

all inputs of size smaller than n (this is called “strong induction”). This basically tells us that our

recursive calls are guaranteed to give a peak for the subarray they’re called on. Why does this

imply that our overall answer is correct? There’s one step to argue: you need to show that a peak



<a name="br4"></a> 

4

Lecture 1: Introduction

returned in the subarray is also a peak in the whole array. There are two cases. In the ﬁrst case,

the subarray peak is not sitting on the inner boundary (it’s not adjacaent to the midpoint of A). In

this case, it is clear that it must be a peak of the whole array A, since all of its neighbors are in

the subarray. The second case is when the subarray peak is on the inner boundary, i.e. adjacent

to the midpoint of A. In this case, observe that we chose the subarray in the “uphill” direction, so

the value on the inner boundary must be greater than or equal to the value at the midpoint of A.

Hence, if this location is a subarray peak, it must also be a peak in all of A. Thus, we have shown

that the algorithm is correct for inputs of length n.

What about runtime? In each recursive call, I do O(1) work, and I cut the search space in half.

So the total runtime is going to be O(log n). Just like for binary search! Can anyone think of a

worst-case input that takes this much time, showing that the runtime is actually Θ(log n)? One

possibility is to take an input that is sorted in increasing order. Then you will always recurse to the

right subarray, and go till the end because a midpoint will never be a peak.

To sum up, this algorithm is exponentially more efﬁcient than the linear scan. For large inputs,

this can be a huge savings! To achieve this, we had to apply a general technique (the idea of divide-

and-conquer), together with some speciﬁc insights about the problem, which we had to come up

with by being creative.

The importance of data structures

A recurring theme we’ll see in this class is that a good algorithm is enabled by a good data structure:

a way of representing data in the computer that is useful for some purpose. There actually is a

simple but powerful data structure hiding inside this algorithm: it’s called the static array. The

crucial thing about an array is that it enables indexing in constant time: given an index i, I can read

out the ith element of my array in time that is independent of how long the array is. It is a minor

miracle that computers let you do this. Imagine a computer whose memory used VHS tapes: then

if the tape head starts pointing at A[0], to read a value A[i] would require running the tape forward

for i steps, which would take time Ω(i).

In the next lecture, we will discuss this data structure, and some others (such as the linked list,

and the dynamic array) in more detail. We will also discuss the model of computation that enables

the static array to be implemented, and which we will use throughout this class: this is called the

RAM machine model.

Parting words

For details about the lecture schedule, assignments, assessments, and other policies, please read

the course information handout. For now, I will just give you this heads-up:

• Communication is a major part of this course, so pay attention to your writing!

• Algorithms problems require creativity and attention to detail. Staying up to date with lec-

ture and starting to think about the problem sets as early as possible will save you time and

effort in the long run.



<a name="br5"></a> 

Lecture 1: Introduction

5

• Go to recitation!

• Feel free to approach the TA s and instructors for any help you need in the class.


