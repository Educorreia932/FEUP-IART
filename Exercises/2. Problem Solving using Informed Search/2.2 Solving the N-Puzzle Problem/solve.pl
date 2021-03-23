:- use_module(library(lists)).

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