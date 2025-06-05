% ATOMS
{atom(A)}   :- pool_atm(A).
{assumption(A)} :- pool_asm(A).

pool_atm(300..305). % and a set of extra atoms

inarg(X,Arg) :- rule(R,Arg), head(R,X), learnable(R). %guess content for the new rules
inarg(X,Arg) :- rule(R,Arg), body(R,X), learnable(R).
%transfer elements in guessed existent rule to the new argument in which it was guessed to now belong
inarg(X,Arg) :- rule(R,Arg), head(R,X).
inarg(X,Arg) :- rule(R,Arg), body(R,X).

% RULES
{learnable(1..20)}.
{rule(R, Arg)} :- learnable(R), argument(Arg). 
{rule(R, Arg2)} :- rule(R, Arg), argument(Arg2). %for existent rules

%Guess rules :only fill learnable rules, for already available rules we can "just transfer" them.
{head(R,X)} :- atom(X), learnable(R).
{body(R,X)}:- atom(X),  learnable(R).
{body(R,X)}:- assumption(X), learnable(R).

:- #count {X: body(R,X)} > 5, learnable(R). %not more than 5 body elements per rule
:- not body(R,_), learnable(R). % not an empty body
:- not head(R,_), learnable(R). % not an emtpy head
:- body(R,X), head(R,X), learnable(R). % not an atom both in head and body of rule.
:- head(R,X), head(R,Y), X != Y, learnable(R). % not (rule has more than one atom in the head).
:- rule(R1, Arg), rule(R2, Arg), head(R1, X), head(R2, X), R1 != R2. % atom not the head of multiple rules in the same argument.

%checkme(Arg,X):- rule(R1, Arg), rule(R2, Arg), head(R1, X), head(R2, X), R1 != R2. % atom not the head of multiple rules in the same argument.
%#show checkme/2.

% DERIVABILITY
derivable(X,Arg) :- assumption(X), inarg(X,Arg).
derivable(X,Arg) :- head(R,X), triggered(R, Arg), rule(R, Arg), inarg(X,Arg).
triggered(R,Arg) :-  rule(R,Arg), derivable(X,Arg) : body(R,X).
:- atom(X), inarg(X, Arg), not derivable(X, Arg). % in an argument, all atoms must be derivable (otherwise BK of them being in an argument was wrong).

% REACHABILITY
start(X, Arg) :- assumption(X), inarg(X, Arg).
start(X, Arg) :- head(R,X), not conclusion(X,Arg), inarg(X, Arg), rule(R, Arg).
reach(X,X,Arg) :- start(X,Arg).
reach(X,Y, Arg) :- head(R,Y), body(R,X), rule(R, Arg).
reach(X,C, Arg) :- reach(X,D, Arg), body(R,D), head(R,C), rule(R, Arg).
:- conclusion(Y,Arg), start(X, Arg), not reach(X,Y, Arg), inarg(X, Arg), inarg(Y, Arg). % conclusions in all arguments are reached from all atoms (all components are connected)

% % PREFERENCES
in_rule(R,X) :- atom(X), 1{body(R,X);head(R,X)}, learnable(R).
in_rule(R,X) :- assumption(X), 1{body(R,X);head(R,X)}, learnable(R).
:~ related(T1, X), related(T2, Y), T1!=T2, learnable(R), in_rule(R,X), in_rule(R,Y). [1@1, R,T1]


#show assumption/1.
#show argument/1.
#show inarg/2.
#show body/2.
#show head/2.
#show learnable/1.
%#show distance/2.
#show rule/2.
#show conclusion/2.
#show derivable/2.
%#show reach/3.