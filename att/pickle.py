import cPickle as pickle

def LoadFromFile(file_name):
  input_file = open(file_name, 'r')
  obj = pickle.load(input_file)
  input_file.close()
  return obj

def SaveToFile(obj, file_name):
  p = pickle.Pickler(open(file_name,"wb"))
  p.fast = True 
  p.dump(obj)

