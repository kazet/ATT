class FindUnion(object):
  def __init__(self):
    self._weights = {}
    self._parents = {}

  def __iter__(self):
    return self._parents.keys().__iter__()

  def AddIfNotExists(self, *objs):
    for obj in objs:
      if obj not in self._parents:
        self._parents[obj] = obj
        self._weights[obj] = 1

  def Find(self, obj):
    path = [obj]
    root = self._parents[obj]
    while root != path[-1]:
      path.append(root)
      root = self._parents[root]

    for ancestor in path:
      self._parents[ancestor] = root
    return root

  def Union(self, *objs):
    roots = [self.Find(x) for x in objs]
    heaviest = max([(self._weights[r],r) for r in roots])[1]
    for r in roots:
      if r != heaviest:
        self._weights[heaviest] += self._weights[r]
        self._parents[r] = heaviest
