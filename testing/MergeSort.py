"""
A merge sort implementation

Written by Tim
"""
def merge(lst1, lst2, compare):
  merged_list = []
  index1 = 0
  index2 = 0
  len1 = len(lst1)
  len2 = len(lst2)

  while index1 < len1 or index2 < len2:
    if index2 == len2 or \
      (index1 < len1 and compare(lst1[index1], lst2[index2])):
      merged_list.append(lst1[index1])
      index1 += 1
    else:
      merged_list.append(lst2[index2])
      index2 += 1
  
  return merged_list

def sort(lst, compare):
  if len(lst) <= 1:
    return lst
  
  pivot = len(lst) // 2

  lst1 = sort(lst[:pivot], compare)
  lst2 = sort(lst[pivot:], compare)
  return merge(lst1, lst2, compare)

def merge_sort(lst):
  return sort(lst, comp_num)


def comp_str(s1, s2):
  return s1.lower() < s2.lower()

def comp_num(n1, n2):
  return n1 < n2

if __name__ == "__main__":
  num_array = [9,8,7,6,5,4,3,2,1]
  string_array = ["Hello", "World!"]
  string_array2 = ["AAB", "AAA", "ABB", "BBB", "BAA"]

  print(sort(num_array, comp_num))
  print(sort(string_array, comp_str))
  print(sort(string_array2, comp_str))