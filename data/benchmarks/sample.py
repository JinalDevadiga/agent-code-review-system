# Fibonacci function - classic inefficient algorithm
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


# Unoptimized sorting
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


# Simple search function
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


# String manipulation without optimization
def count_vowels(text):
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count


# Complex nested loops
def matrix_operation(matrix):
    result = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            for k in range(len(matrix)):
                val = matrix[i][j] * matrix[k][j]
                result.append(val)
    return result
