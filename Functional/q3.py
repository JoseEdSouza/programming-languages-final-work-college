# The code is checking whether a given string `_str` contains a palindrome of length `n` or not.

# The `is_palindrome` lambda function is checking whether a given string `_str` is a palindrome or
# not.
is_palindrome = lambda _str: len(_str)<2 or ((_str[0] == _str[-1] and is_palindrome(_str[1:-1]))) 

# The `contains_palindrome` lambda function is checking whether a given string `_str` contains a
# palindrome of length `n` or not.
contains_palindrome = lambda n,_str: len(_str)>=n and (is_palindrome(_str[:n]) or contains_palindrome(n,_str[1:]))

# The code is taking two inputs from the user: an integer `n` and a string `_str`. It then checks if
# the string `_str` contains a palindrome of length `n` or not using the `contains_palindrome` lambda
# function.
if contains_palindrome(int(input()),input()):
    print('sim')
else:
    print('nao')
