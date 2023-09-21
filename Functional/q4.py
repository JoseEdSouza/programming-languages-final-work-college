# The code is defining two lambda functions and using them to filter and print prime numbers from an
# input list.
# The line `input_list = lambda:list(map(lambda x: int(x),input().split()))` is defining a lambda
# function called `input_list`.
input_list = lambda:list(map(lambda x: int(x),input().split()))

# The line `is_primo = lambda n: n>=2 and len(list(filter(lambda i: n%i == 0,range(2,n)))) == 0` is
# defining a lambda function called `is_primo`.
is_primo = lambda n: n>=2 and len(list(filter(lambda i: n%i == 0,range(2,n)))) == 0

# The line `print(*list(filter(is_primo,input_list())),end=" ")` is printing all the prime numbers
# from the input list.
print(*list(filter(is_primo,input_list())),end=" ")