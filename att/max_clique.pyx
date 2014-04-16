from att.utils import \
  Flatten, \
  Subsets

def MaxClique(graph):
  """Returns S, a subset of V with maximum size such that every two vertices
  in S are connected with an edge in the graph.

  Args: graph should be a list of tuples, each of them describing one graph
        edge."""
  vertices = list(set(Flatten(graph)))
  max_candidate = ()
  print "mc subsetscall for vertices=",vertices
  for candidate in Subsets(vertices):
    good = True
    for candidate_item_1 in candidate:
      for candidate_item_2 in candidate:
        if candidate_item_1 == candidate_item_2:
          continue
        if (candidate_item_1, candidate_item_2,) not in graph and \
           (candidate_item_2, candidate_item_1,) not in graph:
          good = False
    if good and len(candidate) > len(max_candidate):
      max_candidate = candidate
  return max_candidate

