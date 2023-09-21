# Logical Programming Problems in Prolog

This repository contains Prolog programs that solve various logical programming problems. Each Prolog file addresses a specific problem or set of problems. Below, you'll find descriptions and explanations for each problem along with their respective Prolog files.

## Q1 - Prime Numbers and List Manipulation

[q1.pl](q1.pl)

- `primo_rec(X, Y)` checks if an integer `X` is a prime number using recursive evaluation.
- `primo(X)` checks if an integer `X` is a prime number by combining direct checks and recursive evaluation.
- `list_primos(List)` checks if all elements in a given list are prime numbers.

## Q2 - Finding N-th Element in a List

[q2.pl](q2.pl)

- `n_esimo(N, List, X)` finds the N-th element (1-based index) in a given list.

## Q3 - Calculating the Length of a List

[q3.pl](q3.pl)

- `tamanho(List, X)` computes the length of a given list using recursion.

## Q4 - Checking Membership in a List and Removing Duplicates

[q4.pl](q4.pl)

- `pertence(X, List)` checks if an element `X` belongs to a given list.
- `elimina_repetidos_rec(List, Acc, Result)` removes duplicate elements from a given list using recursion.
- `elimina_repetidos(List, Result)` serves as an entry point for removing duplicates by initializing the accumulator.

## Q5 - Family Relationships

[q5.pl](q5.pl)

- Defines relationships between family members and allows queries about family relationships.
- Includes predicates to define people, parents, siblings, aunts/uncles, cousins, etc.

---

You can explore each problem separately by opening the corresponding Prolog file. Feel free to use and modify these Prolog programs as needed to suit your requirements.
