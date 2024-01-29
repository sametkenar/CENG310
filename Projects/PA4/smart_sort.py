def smart_sort(input_array):
    if len(input_array) == 1: # if input_array's length is equivalent to 1, no need to sort.
        return input_array
    if not all(isinstance(element, (int, float)) for element in input_array): # Raising exception if data is neither int nor float.
        raise ValueError("input_array have to be formed by int or float values.")
    if len(input_array) < 50:   # if size of the array less than 50, utilize selection sort algorithm.
        return selection_sort(input_array)
    else:                       # if size of the array greater than 50, utilize quick sort algorithm.
        return quick_sort(input_array)

def selection_sort(input_array): # selection sort algorithm, since there is nested loop time complexity is O(n^2) in worst-case.
    n = len(input_array)
    for pointer in range(n - 1): 
        minimum_value = pointer  # setting pointer value as minimum value for comparison
        for other_element in range(pointer + 1, n): # comparing the pointer value with the other elements
            if input_array[other_element] < input_array[minimum_value]: # comparing elements 
                minimum_value = other_element  # replacing                         
        input_array[pointer], input_array[minimum_value] = input_array[minimum_value], input_array[pointer]  # swapping the minimum element with the current element
    return input_array

def quick_sort(input_array):  # quick sort algorithm, works in best case. Since we set the pivot value to half of the input_array's size. 
                              # It divides input_ array recursively equal halves. The time complexity is omega(NlogN)
    if len(input_array) <= 1:   # if input_array's size is less than or is equivalent to 1, return input_array no need to sort.
        return input_array
    pivot_value = input_array[len(input_array) // 2]        # setting the pivot value as size's half for the best case scenario 
    leftmostside = [element for element in input_array if element < pivot_value]  # seperating leftmostside
    pivot = [element for element in input_array if element == pivot_value]       # separating the middle element as pivot 
    rightmostside = [element for element in input_array if element > pivot_value]   # seperating the rightmostside
    return quick_sort(leftmostside) + pivot + quick_sort(rightmostside)    # recursively calling the function for leftmost and rightmostside and concatenating it with middle element.
