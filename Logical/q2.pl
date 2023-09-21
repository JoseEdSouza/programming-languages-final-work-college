/**
 * n_esimo(N, List, X)
 *
 * Finds the N-th element (1-based index) in a given List.
 *
 * @param N     The index of the element to retrieve.
 * @param List  The input list.
 * @param X     The output variable where the N-th element is stored.
 *
 * Example Usage:
 * - To find the 1st element of [1, 2, 3], X should be unified with 1.
 *   n_esimo(1, [1, 2, 3], X).
 *
 * Note:
 * - If N is out of bounds (less than 1 or greater than the length of the List),
 *   X will not be unified with any value.
 */


n_esimo(1, [H|_], H).
n_esimo(N, [_|T], X) :- N1 is N - 1, n_esimo(N1, T, X).