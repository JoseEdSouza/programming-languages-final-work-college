# The code is defining two lambda functions and then calling one of them.

# The line `input_list = lambda:list(map(lambda x: int(x),input().split()))` is defining a lambda
# function called `input_list`.
input_list = lambda:list(map(lambda x: int(x),input().split()))

# The line `change_num = lambda n1,n2,_list: list(map(lambda x: x+n2 if x==n1 else x,_list))` is
# defining a lambda function called `change_num`.
change_num = lambda n1,n2,_list: list(map(lambda x: x+n2 if x==n1 else x,_list))

# The line `print(*change_num(int(input()),int(input()),input_list()),end=" ")` is calling the
# `change_num` lambda function with three arguments: the first argument is the result of calling
# `int(input())`, the second argument is the result of calling `int(input())`, and the third argument
# is the result of calling `input_list()`.
print(*change_num(int(input()),int(input()),input_list()),end=" ")