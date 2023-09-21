# The code is defining three lambda functions and then using them to find the symmetric difference
# between two lists.

# The line `input_list = lambda:list(map(lambda x: int(x),input().split()))` is defining a lambda
# function called `input_list`.
input_list = lambda:list(map(lambda x: int(x),input().split()))

# The line `contains = lambda elem,_list: len(_list) != 0 and (elem ==_list[0] or
# contains(elem,_list[1:]))` is defining a lambda function called `contains`.
contains = lambda elem,_list: len(_list) != 0 and (elem ==_list[0] or contains(elem,_list[1:]))

# The line `simetric_dif = lambda l1,l2: list(filter(lambda x: contains(x,l1+l2) and (not
# contains(x,l2) or not contains(x,l1)),l1+l2))` is defining a lambda function called `simetric_dif`.
simetric_dif = lambda l1,l2: list(filter(lambda x: contains(x,l1+l2) and (not contains(x,l2) or not contains(x,l1)),l1+l2))

print(*simetric_dif(input_list(),input_list()),end=" ")

