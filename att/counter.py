class ProbabilisticCounter(dict):
  def Inc(self, word):
    if word.__hash__() in self:
      self[word.__hash__()] += 1
    else:
      self[word.__hash__()] = 1

  def GetOr0(self, word):
    if word.__hash__() in self:
      return self[word.__hash__()]
    else:
      return 0

  def Get(self, word):
    return self[word.__hash__()]
