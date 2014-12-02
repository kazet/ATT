import os
import tempfile
import subprocess

from att.log import LogDebug
from att.utils import TupleSplit
from att.alignment import Alignment
from att.language import Languages
from att.aligner.aligner import Aligner
from att.aligner.aligner_factory import AlignerFactory

@AlignerFactory.Register
class HunalignAligner(Aligner):
  def __init__(self, config):
    super(HunalignAligner, self).__init__(config)
    config_dir = config.get('runtime', {}).get('config_dir', '')
    self._hunalign_bin = os.path.join(config_dir,
                                      config['hunalign_bin'])

    self._lang_a = Languages.GetByCode(config['lang_a'])
    self._lang_b = Languages.GetByCode(config['lang_b'])

  def Align(self, multilingual_document, dictionary):
    handle_a, name_a = tempfile.mkstemp(
        suffix='-lang_%s' % self._lang_a.GetCode())
    file_a = os.fdopen(handle_a, 'w')
    for sentence in multilingual_document.GetSentences(self._lang_a):
      file_a.write("%s\n" % sentence.strip().encode('utf-8'))
    file_a.close()

    handle_b, name_b = tempfile.mkstemp(
        suffix='-lang_%s' % self._lang_b.GetCode())
    file_b = os.fdopen(handle_b, 'w')
    for sentence in multilingual_document.GetSentences(self._lang_b):
      file_b.write("%s\n" % sentence.strip().encode('utf-8'))
    file_b.close()

    hunalign_dictionary = dictionary.CachedConvertToHunalignFormat(
        self._lang_a,
        self._lang_b)

    command = [self._hunalign_bin,
               '-bisent',
               hunalign_dictionary,
               name_a,
               name_b]
    LogDebug("HunalignAligner: calling %s\n",
             ' '.join(command))
    out = subprocess.check_output(command)

    alignment = Alignment(multilingual_document)
    for line in out.split('\n'):
      try:
        src_id, trg_id, unused_confidence = TupleSplit(line, '\t', 3)
      except ValueError:
        continue
      alignment.AddMatch([(self._lang_a, int(src_id)), (self._lang_b, int(trg_id))])
    return alignment
