# LR-Grammar
Программа-распознаватель  для LR(k) грамматики данного вида:

S ::= ABC | BC | C  
A ::= (B) | Aa | a
B ::= (BC) | b
C ::= (D) | c
D ::= A
