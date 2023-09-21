/**
 * tamanho(List, X)
 *
 * Computes the length of a given list using recursion.
 *
 * @param List  The input list for which the length is to be computed.
 * @param X     The output variable where the length of the list is stored.
 *
 * Example Usage:
 * - To find the length of [1, 2, 3, 4], X should be unified with 4.
 *   tamanho([1, 2, 3, 4], X).
 *
 * Note:
 * - The predicate succeeds by unifying X with the length of the input list.
 * - It uses recursive calls to traverse the list, incrementing X for each element.
 * - The base case is when an empty list is encountered, in which case X is unified with 0.
 */

tamanho([],0).
tamanho([_|T], X) :-tamanho(T, N), X is N+1.