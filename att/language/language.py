"""See `Languages' in the documentation."""

class Language(object):
  """Represents all information about a language."""
  def __init__(self, **kwargs):
    self._code = kwargs['code']
    self._name = kwargs['name']
    self._id = kwargs['id']
    self._nltk_name = kwargs['nltk_name'] if 'nltk_name' in kwargs \
        else self._name.lower()
    self._cfs_name = kwargs['cfs_name'] if 'cfs_name' in kwargs \
        else self._name.lower()

  def GetCode(self):
    """Returns language two-letter code."""
    return self._code

  def GetNLTKName(self):
    """Returns language name used by NLTK."""
    return self._nltk_name

  def GetCFSName(self):
    """Returns language name used by CFS."""
    return self._cfs_name

  def GetName(self):
    """Returns language human-readable name."""
    return self._name

  def __eq__(self, other):
    # pylint: disable=W0212
    return self._code == other._code

  def __str__(self):
    return self._name

  def __hash__(self):
    return self._id

  def __repr__(self):
    return self.__str__()

  def __unicode__(self):
    return self.__str__()
