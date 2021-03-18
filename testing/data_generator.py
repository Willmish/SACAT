"""
ListGenerator can be used to generate all data necessary for data gathering
1. Random list: random_lst method
2. Duplicate list: duplicate_lst method
3. Sorted list: sorted_lst method
4. Reverse sorted list: reversed_lst method

To change the list size use the ListGeneratorObject.size = new_size setter method.

Written by Tim
"""

import random

class ListGenerator:
  def __init__(self,min_value=-1000000, max_value=1000000, size=100):
    self.__min_value = min_value
    self.__max_value = max_value
    self.__size = size
  
  @property
  def size(self):
    return self.__size
  
  @size.setter
  def size(self, new_size):
    self.__size = new_size
  
  @property
  def min_value(self):
    return self.__min_value
  
  @min_value.setter
  def min_value(self, new_min_value):
    self.__min_value = new_min_value
  
  @property
  def max_value(self):
    return self.__max_value

  @max_value.setter
  def max_value(self, new_max_value):
    self.__max_value = new_max_value

  # generate a list with random integers
  def random_lst(self):
    lst = [(random.randint(self.__min_value,self.__max_value)) for i in range(self.__size)]
    return lst
  
  # generate a random list with lots of duplicates
  def duplicate_lst(self):
    old_min_value = self.__min_value
    old_max_value = self.__max_value
    self.min_value = -self.__size//100
    self.max_value = self.__size//100
    lst = self.random_lst()
    self.min_value = old_min_value
    self.max_value = old_max_value
    return lst

  # generate a sorted list of integers
  def sorted_lst(self):
    lst = [i for i in range(self.__size)]
    return lst

  # generate a reverse sorted list of integers
  def reversed_lst(self):
    lst = [i for i in range(self.__size, 0, -1)]
    return lst

  # generate a list of 1s
  def equal_lst(self):
    lst = [1 for i in range(self.__size)]
    return lst
  
  # generate a random list of odd length
  def odd_len_lst(self):
    lst = [(random.randint(self.__min_value,self.__max_value)) for i in range(self.__size-1)]
    return lst

if __name__ == "__main__":
  lstgen = ListGenerator()
  print(lstgen.random_lst())
  print("\n")
  print(lstgen.duplicate_lst())
  print("\n")
  print(lstgen.sorted_lst())
  print("\n")
  print(lstgen.reversed_lst())