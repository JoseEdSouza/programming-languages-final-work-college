
/**
 * primo_rec(X, Y)
 *
 * Checks if a given integer X is a prime number using recursive evaluation.
 *
 * @param X  The integer to be checked for primality.
 * @param Y  The divisor used for recursive evaluation, starting from 2.
 *
 * Example Usage:
 * - To check if 7 is a prime number:
 *   primo_rec(7, 2).
 *
 * Note:
 * - The predicate succeeds if X is a prime number (no divisors other than 1 and itself are found).
 * - It fails if X is not a prime number (at least one divisor other than 1 and itself is found).
 */

primo_rec(_,2).
primo_rec(X,Y):- X>2,(X mod Y =\= 0),Z is Y-1,primo_rec(X,Z).

/**
 * primo(X)
 *
 * Checks if a given integer X is a prime number using a combination of predicates.
 *
 * @param X  The integer to be checked for primality.
 *
 * Example Usage:
 * - To check if 7 is a prime number:
 *   primo(7).
 *
 * Note:
 * - The predicate succeeds if X is a prime number (no divisors other than 1 and itself are found).
 * - It fails if X is not a prime number (at least one divisor other than 1 and itself is found).
 * - This predicate combines both direct checks for prime numbers (2 and 3) and recursive evaluation
 *   using the `primo_rec/2` predicate to determine primality.
 */

primo(2).
primo(3).
primo(X):- Y is X-1 , primo_rec(X,Y).

/**
 * list_primos(List)
 *
 * Checks if all elements in the given List are prime numbers.
 *
 * @param List  The input list to be checked.
 *
 * Example Usage:
 * - To check if all elements in [2, 3, 5, 7] are prime numbers:
 *   list_primos([2, 3, 5, 7]).
 *
 * Note:
 * - The predicate succeeds if all elements in the list are prime numbers.
 * - It fails if there is at least one non-prime element in the list.
 */

list_primos([]).
list_primos([H|T]):- primo(H),list_primos(T).