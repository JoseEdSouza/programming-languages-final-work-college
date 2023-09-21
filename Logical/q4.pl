/**
 * pertence(X, List)
 *
 * Checks if a given element X belongs to a given list List.
 *
 * @param X     The element to be checked for membership in the list.
 * @param List  The input list in which the membership of X is to be determined.
 *
 * Example Usage:
 * - To check if 3 belongs to the list [1, 2, 3, 4], the query would be:
 *   pertence(3, [1, 2, 3, 4]).
 *
 * Note:
 * - The predicate succeeds if X is found in the list.
 * - It fails if X is not present in the list.
 * - The predicate uses recursive calls to traverse the list elements.
 * - The first clause checks if X is the head of the list, and the second clause
 *   continues searching for X in the tail of the list.
 */

pertence(X, [X|_]).
pertence(X, [_|L]) :- pertence(X, L).



/**
 * elimina_repetidos_rec(List, Acc, Result)
 *
 * Removes duplicate elements from a given List using recursion.
 *
 * @param List    The input list from which duplicates are to be removed.
 * @param Acc     An accumulator list that stores unique elements.
 * @param Result  The output variable where the list with duplicates removed is stored.
 *
 * Example Usage:
 * - To remove duplicate elements from [1, 2, 2, 3, 3, 4], Result should be unified with [1, 2, 3, 4].
 *   elimina_repetidos_rec([1, 2, 2, 3, 3, 4], [], Result).
 *
 * Note:
 * - The predicate succeeds by unifying Result with a list that contains only unique elements
 *   from the input List, preserving their original order.
 * - It uses an accumulator (Acc) to build the unique list during recursion.
 * - The first clause checks if the current element (X) is already in the accumulator (L2).
 *   If so, it continues the recursion.
 * - The second clause adds X to the accumulator (L2) and continues the recursion.
 */

elimina_repetidos_rec([],L2, L2).
elimina_repetidos_rec([X|T], L2, Result) :-pertence(X, L2), elimina_repetidos_rec(T, L2, Result).
elimina_repetidos_rec([X|T], L2, Result) :- \+ pertence(X, L2),append(L2, [X], L3),elimina_repetidos_rec(T, L3, Result).

/**
 * elimina_repetidos(List, Result)
 *
 * Removes duplicate elements from a given List.
 *
 * @param List    The input list from which duplicates are to be removed.
 * @param Result  The output variable where the list with duplicates removed is stored.
 *
 * Example Usage:
 * - To remove duplicate elements from [1, 2, 2, 3, 3, 4], Result should be unified with [1, 2, 3, 4].
 *   elimina_repetidos([1, 2, 2, 3, 3, 4], Result).
 *
 * Note:
 * - This predicate serves as an entry point for removing duplicates by initializing the accumulator ([]) and
 *   then calling the recursive predicate elimina_repetidos_rec/3.
 */
elimina_repetidos(L1, Result) :- elimina_repetidos_rec(L1, [], Result).
