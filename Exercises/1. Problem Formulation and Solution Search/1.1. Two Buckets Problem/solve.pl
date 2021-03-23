:- use_module(library(lists)).

:- consult('transitions.pl').

% Breadth-first search

bfs([[E|Path]|_], [E|Path]) :-
    end_state(E).

bfs([[E|Path]|R], S) :-
    findall(
        [E1|[E|Path]],
        (trans(E, E1), \+(member(E1, [E|Path]))),
        LS
    ),
    append(R, LS, L),
    bfs(L, S).

solve_bfs(S) :-
    start_state(Ei),
    bfs([[Ei]], SR),
    reverse(SR, S).

% Depth-first search (without checking visited nodes)

dfs(E, [E]) :-
    end_state(E).

dfs(E, [E|R]) :-
    trans(E, E1),
    dfs(E1, R).

solve_dfs_(S) :-
    start_state(Ei),
    dfs(Ei, S).

% Depth-first search (checking visited nodes)

dfs(E, _, [E]) :-
    end_state(E).

dfs(E, Visited, [E|R]) :-
    trans(E, E1), 
    dfs(E1, R).

solve_dfs(S) :-
    start_state(Ei),
    dfs(Ei, S).
