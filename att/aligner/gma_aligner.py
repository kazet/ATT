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
class GMAAligner(Aligner):
  def __init__(self, config):
    super(GMAAligner, self).__init__(config)
    config_dir = config.get('runtime', {}).get('config_dir', '')
    self._gma_axis_plain_bin = config['gma_axis_plain_bin']
    self._gma_config = config['gma_config']
    self._gma_output_file = config['gma_output_file']
    self._gma_command_line = config['gma_command_line']

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

    handle_a_axis, name_a_axis = tempfile.mkstemp(suffix="a.axis")
    os.system("%s < %s > %s" % (self._gma_axis_plain_bin, name_a, name_a_axis))
    handle_b_axis, name_b_axis = tempfile.mkstemp(suffix="b.axis")
    os.system("%s < %s > %s" % (self._gma_axis_plain_bin, name_b, name_b_axis))

    print "%s -properties %s -xAxisFile %s -yAxisFile %s" % (
        self._gma_command_line,
        self._gma_config,
        name_a_axis,
        name_b_axis)
    os.system("%s -properties %s -xAxisFile %s -yAxisFile %s" % (
        self._gma_command_line,
        self._gma_config,
        name_a_axis,
        name_b_axis))

    alignment = Alignment(multilingual_document)
    for line in open(self._gma_output_file).readlines():
      tokens = line.strip().split(' ')
      left_sentences = tokens[0].split(',')
      right_sentences = tokens[2].split(',')

      match = []
      for left_sentence in left_sentences:
        if left_sentence != 'omitted':
          match.append( (self._lang_a, int(left_sentence) - 1) )
      for right_sentence in right_sentences:
        if right_sentence != 'omitted':
          match.append( (self._lang_b, int(right_sentence) - 1) )
      alignment.AddMatch(match)
    return alignment
