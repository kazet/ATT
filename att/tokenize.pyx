from libc.string cimport strlen
from libc.stdlib cimport calloc, free

cdef extern from "Python.h":
  char *PyString_AsString(object)

def tokenize(sentence):
  cdef int i
  cdef char* csentence = PyString_AsString(sentence)
  result = []
  cdef char* word = <char*> calloc(sizeof(char), strlen(csentence))
  cdef int word_len = 0
  for i in range(strlen(csentence)):
    if csentence[i] == ' ' and word_len > 0:
      word[word_len] = 0
      result.append(word)
      word_len = 0
    elif csentence[i] != '.' and csentence[i] != ',':
      word[word_len] = csentence[i]
      word_len += 1
  word[word_len] = 0
  result.append(word)
  free(word)
  return result

def pytokenize(sentence):
  result = []
  last = ""
  for c in sentence:
    if c == " " and last != "":
      result.append(last)
      last = ""
    elif c != '.' and c != ',':
      last += c
  if c == " " and last != "":
    result.append(last)
    last = ""
  return result
