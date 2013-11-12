def word_tokenize(sentence):
  result = []
  last = ""
  for c in sentence:
    if c == " " and last != "":
      result.append(last)
      last = ""
    elif c != '.' and c != ',':
      last += c
  if last != "":
    result.append(last)
    last = ""
  return result
