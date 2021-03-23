start_state(b(0, 0)).

end_state(b(2, 0)).

trans(b(A, B), b(4, B)) :- A < 4.  % Fill up bucket A
trans(b(A, B), b(A, 3)) :- B < 3.  % Fill up bucket B
trans(b(A, B), b(0, B)) :- A > 0.  % EmptB bucket A
trans(b(A, B), b(A, 0)) :- B > 0.  % EmptB bucket B

trans(b(A, B), b(4, B1)) :-        % Pour bucket B into bucket A
    A + B >= 4,
    A < 4,
    B1 is B - (4 - A).

trans(b(A, B), b(A1, 3)) :-        % Pour bucket B into bucket A
    A + B >= 3,
    B < 3,
    A1 is A - (3 - B).

trans(b(A, B), b(0, B1)) :-        % Pour bucket B into bucket A
    A + B < 3,
    A > 0,
    B1 is A + B.
    