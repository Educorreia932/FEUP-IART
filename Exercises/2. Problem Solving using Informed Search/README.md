> # 2. Problem Solving using Informed Search  
> ## 2.1 Strategies for Uninformed/Informed Search
>
> Assuming the following search tree in which each arc displays the cost of the corresponding operator, and the nodes contain the value of the heuristic function, indicate justifying, which node is expanded next using each of the following methods: 
>
> **a)** Breadth-First Search (“Pesquisa em
Largura”);

C, pois é o próximo nó em largura que ainda não foi explorado

> **b)** Depth-First Search (“Pesquisa em
Profundidade”);

E, pois é o próximo nó em profundidade que ainda não foi explorado

> **c)** Uniform Cost Search (“Pesquisa de Custo Uniforme”);

D, pois é o nó com menor custo, no caso 3

> **d)** Greedy Search (“Pesquisa Gulosa”); 

C, pois é o nó com menor distância heuristíca à solução, no caso 2

> **e)** A* Algorithm Search (“Pesquisa com Algoritmo A*”) 

G, pois é o nó cuja soma do custo e da distância heurística é o menor, no caso 11

> ## 2.2 Solving the N-Puzzle Problem 
> The objective of this exercise is the application of search methods, with emphasis on informed search methods and the A* algorithm, to solve the well-known N-Puzzle problem. The desired objective state for the puzzle is as follows (0 represents the empty space):
> ```
> 9 Puzzle      16 Puzzle
>   1 2 3       1  2  3  4  
>   4 5 6       5  6  7  8  
>   7 8 0       9 10 11 12  
>              13 14 15  0  
> ```
> 
> Starting from a given initial state, the goal is to determine which operations to perform to solve the puzzle, reaching the desired objective state. 
>
> **a)** Formulate the problem as a search problem indicating the state representation, operators (their names, preconditions, effects, and cost), initial state, and objective test. 

**States:** Matriz N x N a representar o puzzle, em que cada elemento representaria uma célula do puzzle, numerados de 1 a N. A célula 0 representaria um espaço vazio.
**Initial State:** Matriz com elementos dispostos aleatoriamente.
**End State:** Matriz ordenada pelos números da célula por ordem crescente ao nível das linhas / colunas.
**Operators:** Mover célula vazia para cima, baixo, esquerda ou direita.
**Objective test:** Resolver o puzzle.

> **b)** Implement code to solve this problem using the “breath-first” strategy (in this case
identical to "Uniform Cost").