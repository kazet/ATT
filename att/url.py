import os
import os.path
import hashlib
import urllib
from att.global_context import global_context

CACHE_ROOT = os.path.join(
    os.path.normpath(os.path.dirname(__file__)),
    '..',
    'cache')

class CachedURL(object):
  def __init__(self, url):
    self._url = url

  def get(self):
    filename = hashlib.sha512(self._url).hexdigest()
    path = os.path.join(CACHE_ROOT, filename)

    text = None
    if os.path.exists(path):
      h = open(path)
      text = h.read()
      h.close()
    else:
      global_context.LogDebug(
          "[CachedURL] downloading %s",
          self._url)

      h = urllib.urlopen(self._url)
      text = h.read()
      h.close()

      hw = open(path, 'w')
      hw.write(text)
      hw.close()
    return text
