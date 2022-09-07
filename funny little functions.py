# check if list contains integer
l = [1, 2, 3, 4, 111, 65, 3]
print(111 in l)

# find duplicate number in list
def find_duplicates(elements):
    duplicates, seen = set(), set()
    for element in elements:
        if element in seen:
            duplicates.add(element)
        seen.add(element)

    return list(duplicates)

# check if two strings are anagrams
def is_anagram(s1, s2):
    return set(s1) == set(s2)

print(is_anagram('elvis', 'lives'))

# remove all duplicates from list
lst = list(range(10)) + list(range(10))
lst = list(set(lst))
print(lst)

# find pairs of integers in list so that their sum is equal to integer x
def find_pairs(lst, x):
    pairs = []
    for (i, el_1) in enumerate(lst):
        for (j, el_2) in enumerate(lst[i+1:]):
            if el_1 + el_2 == x:
                pairs.append((el_1, el_2))

    return pairs

# check if a string is palindrome
def is_palindrome(phrase):
    return phrase == phrase[::-1]
print(is_palindrome('anna'))

# use list as stack, array and queue
# as list
l = [3, 4]
l += [5, 6]
# as stack
l.append(10)
l.pop()
# as queue
l.insert(0, 5)
l.pop()

# get missing number in [1...100]
def get_missing_number(lst):
    return set(range(lst[len(lst)-1])[1:]) - set(lst)
l = list(range(1, 100))
l.remove(50)
print(get_missing_number(l))

# compute the intersection of two lists
def intersection(lst1, lst2):
    res, lst2_copy = [], lst2[:]
    for el in lst1:
        if el in lst2_copy:
            res.append(el)
            lst2_copy.remove(el)
    return res

# find min and max in unsorted list
l = [4, 3, 6, 3, 4, 888, 1, -11, 22, 3]
print(max(l))
print(min(l))

# reverse string using recursion
def reverse(string):
    if len(string) <= 1: return string
    return reverse(string[1:]) + string[0]

print(reverse('hello'))

# compute the first n fibonacci numbers
def fibon(n):
    a, b = 0, 1
    for i in range(n):
        print(b)
        a, b = b, a+b

# sort list with quicksort algorithm
def qsort(L):
    if L == []: return []
    return qsort([x for x in L[1:] if x < L[0]]) + L[0:1] + qsort([x for x in L[1:] if x >= L[0]])

lst = [44, 33, 22, 11, 77, 5, 55, 969]
print(qsort(lst))

# find all permutations of a string
def get_permutations(w):
    if len(w) <= 1: return set(w)
    smaller = get_permutations(w[1:])
    perms = set()
    for x in smaller:
        for pos in range(0, len(x) + 1):
            perm = x[:pos] + w[0] + x[pos:]
            perms.add((perm))

    return perms

print(get_permutations('nan'))