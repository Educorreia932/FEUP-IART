> ## 1. Problem Formulation and Solution Search 
> 
> ### 1.1 Two Buckets Problem 
> 
> Two buckets, of capacities c1 (e.g. 4 liters) and c2 (e.g. 3 liters), respectively, are initially empty.  
> 
> Buckets do not have any intermediate markings. The only operations you can perform are:
> 
> - Fill (completely) a bucket
> - Empty a bucket.
> - Pour one bucket into the other (until the second one is full or until the first one is empty).
> 
> The aim is to determine which operations to carry out so that the first bucket contains 2 liters. 
>
> **a)** Formulate this problem as a search problem by
defining the state representation, initial state,
operators (their name, preconditions, effects, and cost), and objective test. 

**States:** Two integers, representing how filled up each bucket is  
**Initial State:** 0, 0  
**End State:** 2, 0   
**Operators:** fill, empty, pour     
**Objective test:** First bucket contains *n* liters.

> **b)** Solve the problem, by hand, using tree search.

![](1.2%20Two%20Buckets%20Problem/states.png)

> **c)** Using a programming language of your choice, solve the problem by applying:  
> 
> **(c1)** Breadth-first search strategy. 

