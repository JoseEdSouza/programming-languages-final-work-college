% Definir as pessoas
man(john).
man(peter).
man(mark).
man(david).
man(steve).
man(adam).
woman(lisa).
woman(anne).
woman(mary).
woman(laura).
woman(julie).
woman(sarah).

% Definir os relacionamentos de genitor
genitor(john, peter).
genitor(john, lisa).
genitor(peter, anne).
genitor(peter, mark).
genitor(lisa, david).
genitor(lisa, laura).
genitor(mark, steve).
genitor(mark, julie).
genitor(anne, sarah).
genitor(anne, adam).

%genitor(X,Y). %y é genitor de x

pai(X):- genitor(_,X),woman(X).
mae(X):- genitor(_,X),man(X).

brother(X,Y):- man(Y),genitor(Y,Z),genitor(X,Z).
sister(X,Y):- woman(Y),genitor(Y,Z),genitor(X,Z).

avou(X,Y):- genitor(Z,Y),genitor(X,Z),man(Y).
avoh(X,Y):- genitor(Z,Y),genitor(X,Z),woman(Y).

tio(X,Y):- genitor(X,Z),brother(Z,Y).
tia(X,Y):- genitor(X,Z),sister(Z,Y).

primo(X,Y):- (tio(X,Z);tia(X,Z)),genitor(Y,Z),man(Y).
prima(X,Y):- (tio(X,Z);tia(X,Z)),genitor(Y,Z),woman(Y).

