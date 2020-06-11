## Basic Usage

```
$ python3 main.py data2.csv

Node with id '1' became permanent.
Node with id '3' became permanent.
Node with id '2' became permanent.
Node with id '5' became permanent.
Node with id '4' became permanent.
Node with id '6' became permanent.
Node with id '7' became permanent.

Dijkstra finished in 0.000186920166015625 seconds

N = Node
D = Total Cost/Distance
V = Via/Pred

N       D       V
-       -       -
1       0       None
3       1       1
2       3       3
5       4       2
4       7       3
6       9       5
7       11      6

Enter id of node to display shortest path to or 'quit' to exit: 5
Path: 1 -> 3 -> 2 -> 5
Distance: 4
Enter id of node to display shortest path to or 'quit' to exit: 7
Path: 1 -> 3 -> 2 -> 5 -> 6 -> 7
Distance: 11
Enter id of node to display shortest path to or 'quit' to exit: quit

$
```
