<a name="br1"></a> 

Introduction to Algorithms: 6.006

Massachusetts Institute of Technology

September 14, 2021

Instructors: Mauricio Karchmer, Anand Natarajan, Julian Shun

Lecture 2: Data Structures

Lecture 2: Data Structures

Last time we did not ﬁnish covering the proof of correctness of the peak ﬁnding algorithm.

Please refer to notes for Lecture 1 for this.

Model of Computation (Word-RAM)

As we hinted at in the Lecture 1 notes, the algorithm for peak ﬁnding made a crucial assumption

that one can index into an arbitrary location in an array in constant time. In general, to make

statements about the runtime of algorithms, we have to have a model of computation, that tells

us which operations can be performed in unit time. The model we use is called the “word RAM

model,” and is an idealization of how most computers you interact with actually work. Here are

the basic features of the model:

• Memory: Addressable sequence of machine words

• Machine word: block of w bits (word size, a w-bit Word-RAM)

• Processor supports many constant time operations on words:

– integer arithmetic: (+, -, <sub>\*</sub>, //, %)

– logical operators: (&&, ||, !, ==, <, >, <=, =>)

– (bitwise arithmetic: (&, |, <<, >>, ...))

– Given word a, can read word at address a, write word to address a. (This means that

a word can store a pointer to another location in memory.)

• Memory addresses must be able to access every place in memory, so there are at most 2<sup>w</sup>

words in memory, and also that any computational input must have length at most n = 2<sup>w</sup>.

• Allocating a block of n words in memory takes time Θ(n).

• In practice, computers usually use 32-bit words → max ∼ 4 GB memory, or 64-bit words

→ max ∼ 10<sup>10</sup> GB of memory

The constraint n ≤ 2<sup>w</sup> implies that w must vary as a function of n. This seems strange, since

in actual computers the word size is ﬁxed. The reason we deﬁne the model this way is so that we

can make sense of asymptotic statements. Observe that if we treated w as a constant (say 64), then

our computer’s memory can never hold more than 2<sup>64</sup> words, each 64 bits long. Thus, the input to

any algorithmic question would have a length that is at most some (astronomically huge) constant.

However, asymptotic complexity requires that our problems be well-deﬁned for inputs of length

tending to inﬁnity. Allowing w to vary with the input length solves this deﬁnitional issue.

Note: the “Python model” of computation is not the same as the word-RAM model. This

is because many of the elementary operations in Python are implemented using non-trivial data



<a name="br2"></a> 

2

Lecture 2: Data Structures

structures underneath. For instance, Python arrays are actually implemented using the “dynamic

array” data structure, discussed later in this lecture, and Python dictionaries are implemented using

a hash map, which you will cover later in the term. So you cannot assume that a single elementary

operation in Python takes O(1) time!

Data Structures and Interfaces

A data structure is a way to store data, with algorithms that support operations on the data.

The collection of supported operations is called an interface (also API or Abstract Data Type). An

interface is a speciﬁcation of a desired behavior, and many different data structures may implement

the interface more or less efﬁciently. In this class, there are two main interfaces we will study: the

Sequence and the Set.

Sequence Interface

• Maintain a sequence of items (order is extrinsic)

• Ex: (x , x , x , . . . , x<sub>n−1</sub>) (zero indexing)

0

1

2

• (use n to denote the number of items stored in the data structure)

• Supports sequence operations:

Container build(A)

given an iterable A, build sequence from items in A

len()

return the number of stored items

return the stored items one-by-one in sequence order

return the i<sup>th item</sup>

Static

iter seq()

get at(i)

set at(i, x)

replace the i<sup>th item with</sup>

x

Dynamic insert at(i, x) add x as the i<sup>th</sup> item

delete at(i)

remove and return the i<sup>th item</sup>

insert first(x) add x as the ﬁrst item

delete first() remove and return the ﬁrst item

insert last(x) add x as the last item

delete last() remove and return the last item

• Special case interfaces:

stack insert last(x) and delete last()

queue insert last(x) and delete first()



<a name="br3"></a> 

Lecture 2: Data Structures

3

Set Interface

• Sequence about extrinsic order, set is about intrinsic order. (E.g. consider a set of students

in a class, where the keys are student names, and the order is given by alphabetical order).

• Maintain a set of items having unique keys (e.g., item x has key x.key)

• (A slight variation is the multi-set, in which duplicate keys are allowed.)

• Often we let key of an item be the item itself, but may want to store more info than just key

• Supports set operations:

Container build(A)

given an iterable A, build sequence from items in A

return the number of stored items

len()

Static

find(k)

return the stored item with key k

Dynamic insert(x)

add x to set (replace item with key x.key if one already exists)

remove and return the stored item with key k

delete(k)

Order

iter ord() return the stored items one-by-one in key order

find min() return the stored item with smallest key

find max() return the stored item with largest key

find next(k) return the stored item with smallest key larger than k

find prev(k) return the stored item with largest key smaller than k

• Special case interfaces:

dictionary set without the Order operations

• In recitation, you will be asked to implement a Set, given a Sequence data structure.

Three implementations of the Sequence interface

Static Arrays An array is just a contiguous chunk of cells in memory.

• Array is great for static operations! get at(i) and set at(i, x) in Θ(1) time!

• But not so great at dynamic operations—if the array is full, then inserting an additional

element requires

– reallocating the array (Θ(n) time)

– shifting all items after the modiﬁed item (Θ(n) time)



<a name="br4"></a> 

4

Lecture 2: Data Structures

Operation, Worst Case O(·)

Dynamic

Data

Container Static

Structure build(A)

get at(i) insert first(x) insert last(x) insert at(i, x)

set at(i,x) delete first() delete last()

delete at(i)

Array

n

1

n

n

n

Linked Lists

• Pointer data structure (this is not related to a Python “list”)

• Each item stored in a node which contains a pointer to the next node in sequence

• Each node has two ﬁelds: node.item and node.next

• Can manipulate nodes simply by relinking pointers!

• Maintain pointers to the ﬁrst node in sequence (called the head)

• Can now insert and delete from the front in Θ(1) time! Yay!

• (Inserting/deleting efﬁciently from back is also possible; you will do this in PS1)

• But now get at(i) and set at(i, x) each take O(n) time... :(

Operation, Worst Case O(·)

Data

Container Static

Dynamic

Structure

build(A)

get at(i) insert first(x) insert last(x) insert at(i, x)

set at(i,x) delete first() delete last()

delete at(i)

Linked List

n

n

1

n

n

Dynamic Arrays This data structure achieves the “best of both words”: insertions/deletions to

the end, and get/set to any location are efﬁcient. But we will have to slightly modify our deﬁniton

of fast...

• Goal: make an array efﬁcient for last dynamic operations. This is the data structure behind

the Python list!

• Idea! Whenever the array ﬁlls up, allocate a lot of extra space, so that the array doesn’t ﬁll

up again soon.

• Fill ratio: 0 ≤ r ≤ 1 the ratio of items to space

• Whenever array is full (r = 1), allocate Θ(n) extra space at end to ﬁll ratio r . E.g., if

i

r = 1/2, then when the array ﬁlls up, we create a new array of twice the size, and copy over

i

elements to the new array.



<a name="br5"></a> 

Lecture 2: Data Structures

5

• Will have to insert Θ(n) items before the next reallocation

• A single operation can take Θ(n) time for reallocation in the worst case.

• However, any sequence of Θ(n) operations takes Θ(n) time. For instance, suppose we

perform n inserts starting from an empty array. Every insert takes at least some constant

time c , so we get a contribution of c · n to the total running time. In addition, we have

0

0

a contribution of c · <sup>1</sup> · (current array size) whenever the array ﬁlls up and is resized. For

1

r

i

r = 1/2, this happens whenever the array size hits a power of two. The total amount of time

i

these resizings cost is

T<sub>resize</sub>(n) = c · (2 + 4 + 8 + · · · + 2 <sup>ne</sup>)

dlog

2

1

= O(n),

where we have obtained the bound by summing the geometric series. In some sense, each

insert takes time Θ(1) “on average over operations.” We say that insertion has amortized

complexity Θ(1).

Amortized Analysis

• Data structure analysis technique to distribute cost over many operations

• Operation has amortized cost T(n) if k operations cost at most ≤ kT(n)

• “T(n) amortized” roughly means T(n) “on average” over many operations

• Inserting into a dynamic array takes Θ(1) amortized time

• More amortization analysis techniques in 6.046!

A note on space complexity Observe that using a dynamic array, the total amount of allocated

space that may be a constant multiple of the number of elements in the array. (E.g. just after you

double, there are n elements and 2n cells in memory allocated). So this data structure has a Θ(n)

space overhead. In general, for space complexity, we care about the additional space required

on top of what is necessary to store the input. Yo u will explore this on the mini-quiz!

Some questions to think about: what is the space overhead of a linked list? What about a static

array?

Dynamic Array Deletion It turns out that deletion from the end of a dynamic array can also be

done in amortized time Θ(1), while maintaining a space overhead of only Θ(n).

• Delete from back? Θ(1) time without effort, yay!

• However, can be very wasteful in space. Want size of data structure to stay Θ(n)



<a name="br6"></a> 

6

Lecture 2: Data Structures

• Attempt: if very empty, resize to r = 1. Alternating insertion and deletion could be bad as

we may end up resizing on every operation...

• Idea! When r < r , resize array to ratio r where r < r (e.g., r = 1/4, r = 1/2)

d

i

d

i

d

i

• Then Θ(n) cheap operations must be made before next expensive resize

• Can limit extra space usage to (1 + ε)n for any ε > 0 (set r<sub>d</sub> = <sub>1 +</sub><sup>1</sup> <sub>ε</sub>, r<sub>i</sub> =

• Dynamic arrays only support dynamic last operations in Θ(1) time

<sup>r +1</sup>)

d

2

• Python List append and pop are amortized O(1) time, other operations can be O(n)!

• (Inserting/deleting efﬁciently from front is also possible; you will do this in PS1)

Operation, Worst Case O(·)

Data

Container Static

Dynamic

Structure

build(A)

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

1<sub>(a)</sub>

n

n

n

