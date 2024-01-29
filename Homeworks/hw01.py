# TASK-4
def reverse_string(given_string):
    return given_string[::-1]       # Strings have indexes. By using indexing, we can reverse the strings.

string = "Samet Kenar"
reversed_string = reverse_string(string)
print(reversed_string)

# TASK-5

# R-1.2 ANSWER
def is_even(k):                 # We are checking the least significant bit (LSB) here by using '&' bitwise operator . If the LSB is equivalent to 0, the number is even.
    return k & 1 == 0           # If the LSB is equivalent to 1, the number is odd.

number = 124
print(is_even(number))

# R-1.6 ANSWER
# Finding the sum of squares of odd numbers according to given n input.
def sum_of_squares(n):
    summation = 0
    for i in range(1, n, 2):
        summation += i**2

    return summation

n = 15
print(sum_of_squares(n))

# R-1.7 ANSWER

n = 20      # We can change this number as we wish.

summation1 = sum(i**2 for i in range(1, n, 2))  # Here we used list comprehension method.
print(summation1)

# R-1.9 ANSWER
the_list1 = [i for i in range(50,90,10)] # the parameters are from 50 to 90 with the step operator 10.
print(the_list1)

# R-1.11 ANSWER
the_list2 = [2**i for i in range(9)] # Demonstrated here.
print(the_list2)

# C-1.19 ANSWER
import string   # importing the string module

the_alphabet = [x for x in string.ascii_lowercase] # by using the string module, we are getting each letter one by one with list comprehension.
print(the_alphabet)

# C-1.20 ANSWER
import random

def shuffle(data):
    n = len(data)
    for i in range(n-1, 0, -1):
        j = random.randint(0,i) 
        data[i], data[j] = data[j], data[i] 

the_list3 = [11,12,13,14,15,16,17,18,19,20]
shuffle(the_list3)
print(the_list3)

# C-1.28 ANSWER
import math

def norm(v, p=2):       # p=2 here. This results in traditonal Euclidean norm.
    if p == 2:
        return math.sqrt(sum(x**2 for x in v))
    else:
        if p <= 0 :
            raise ValueError("p must be a positive number")     # Due to square root.
        return math.pow(sum(math.pow(abs(x),p) for x in v), 1/p)

vector = [4,3]
p_norm = norm(vector, 2)
euiclidean_norm = norm(vector)
print(f"2-norm (Euiclidean norm): {euiclidean_norm:.2f}")
print(f"3-norm: {norm(vector, 3):.2f}")

# TASK-6 
# P-1.35 ANSWER
import random

def has_shared_birthday(n):
    birthdays = [random.randint(1, 365) for _ in range(n)]
    unique_birthdays = set(birthdays)
    return len(birthdays) != len(unique_birthdays)

def birthday_paradox_simulation(experiments, n_values):
    for n in n_values:
        shared_count = 0
        for _ in range(experiments):
            if has_shared_birthday(n):
                shared_count += 1
        probability = shared_count / experiments
        print(f"For {experiments} experiments with {n} people, the probability of shared birthdays is approximately {probability:.4f} ")

experiments = 100
n_values = range(5, 101, 5)
birthday_paradox_simulation(experiments, n_values)        

# TASK - 7 
# What does the code snippet below do?

""" while len(l1) != 0:
        l2.insert(len(l2), l1.pop (0))"""

# Firstly, this code snippet is utilized for element transferring from l1 to l2. While loop checks whether the element number of l1 is equal to zero or not.
# Then, in the loop environment, firstly l1.pop(0) removes the [0] indexed element from list 1 and returns it. It takes the first element of the l1.
# The l2.insert(.....) inserts the element obtained from l1.pop(0) at the end of the l2 by measuring the length of l2 with len method. 