
# The code is defining a lambda function called `is_inside`. This function takes two arguments, `ret`
# and `p`, which are tuples representing a rectangle and a point, respectively.

# The line `is_inside = lambda ret,p: p[0]>=ret[0] and p[0]<=ret[0]+ret[2] and p[1]>=ret[1] and
# p[1]<=ret[1]+ret[3]` is defining a lambda function called `is_inside`.
is_inside = lambda ret,p: p[0]>=ret[0] and p[0]<=ret[0]+ret[2] and p[1]>=ret[1] and p[1]<=ret[1]+ret[3]

# The code is taking input from the user to create two tuples: `ret` and `p`. The `ret` tuple
# represents a rectangle with four values: `(x, y, width, height)`. The `p` tuple represents a point
# with two values: `(x, y)`.
print(is_inside((int(input()),int(input()),int(input()),int(input())),(int(input()),int(input()))),end=" ")