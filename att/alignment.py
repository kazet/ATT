import textwrap
from xml.sax.saxutils import escape
from copy import copy

from att.html import RenderTemplate
from att.log import LogDebug, LogDebugFull


def MatchQuasiSort(matches):
  """When matches can be sorted, sorts them. If not, sorts everything but the
  parts that can't be sorted."""
  sorted_matches = []
  matches_remaining = copy(matches)
  while len(matches_remaining) > 0:
    minimas = {}
    for match in matches_remaining:
      for lang, sid in match:
        if lang not in minimas:
          minimas[lang] = sid
        if sid < minimas[lang]:
          minimas[lang] = sid
    minimum_lang, minimum_sid = minimas.items()[0]
    new_matches_remaining = []
    minimum_removed = False
    for match in matches_remaining:
      found_minimum_now = False
      if not minimum_removed:
        if (minimum_lang, minimum_sid) in match:
          found_minimum_now = True
      if not found_minimum_now:
        new_matches_remaining.append(match)
      else:
        minimum_removed = True
        sorted_matches.append(match)
    matches_remaining = new_matches_remaining
  return sorted_matches

class Alignment(object):
  def __init__(self, multilingual_document, matches=None):
    self._multilingual_document = multilingual_document

    # We cannot just write matches=[] because the reference
    # would get copied.
    if matches:
      self._matches = matches
    else:
      self._matches = []

  def GetMultilingualDocument(self):
    return self._multilingual_document

  def AddMatch(self, match):
    self._matches.append(match)

  def GetMatches(self):
    return self._matches

  def __str__(self):
    wrapper = textwrap.TextWrapper(initial_indent='  * ',
                                   subsequent_indent='    ',
                                   width=70)
    result = ""
    i = 1
    for match in self._matches:
      sentences = []
      for language, sentence_id in match:
        sentences.extend(
          wrapper.wrap(
            self._multilingual_document.GetDocument(language).GetSentence(sentence_id)))
      result += "--- %s ---\n" % i
      result += "\n".join(sentences)
      result += "\n"
      i += 1
    return result

  def RenderTMX(self, identifier, output_filename, languages=None):
    return self.Render(identifier, output_filename, 'TMX', languages)

  def RenderHTML(self, identifier, output_filename, languages=None):
    return self.Render(identifier, output_filename, 'HTML', languages)

  def Render(self, identifier, output_filename, render_type='HTML', languages=None):
    if not languages:
      languages = []
      for match in self._matches:
        for language, unused_sentence_id in match:
          languages.append(language)
      languages = set(languages)
    sorted_matches = MatchQuasiSort(self._matches)

    renderable_alignment_data = []
    for match in sorted_matches:
      sentences = {}
      for language in languages:
        sentences[language] = (u'N/A', u'')
      for language, sent_id in row:
        if sent_id < self._multilingual_document.NumSentences(language):
          sentences[language] = (sent_id, self \
              ._multilingual_document \
              .GetDocument(language) \
              .GetSentence(sent_id))
      renderable_alignment_data.append(sorted(sentences.iteritems()))

    if render_type == 'TMX':
      output_file = open(output_filename, 'w')
      output_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
      output_file.write('<!DOCTYPE tmx SYSTEM "tmx14.dtd">\n')
      output_file.write('<tmx version="1.4">\n')
      output_file.write('  <body>\n')
      for renderable_alignment in renderable_alignment_data:
        output_file.write('    <tu>\n')
        output_file.write('      <prop type="Txt::Doc. No.">%s</prop>\n' % escape(identifier))
        for language, value in renderable_alignment.items():
          unused_sent_id, sentence = value
          output_file.write('      <tuv xml:lang="%s">\n' % language)
          output_file.write('        <seg>%s</seg>\n' % sentence)
          output_file.write('      </tuv>')
        output_file.write('    </tu>\n')
      output_file.write('  </body>\n')
      output_file.write('</tmx>\n')
      output_file.close()
    elif render_type == 'HTML':
      result = RenderTemplate(
          'alignment_render.html',
          { 'identifier': identifier,
            'languages': sorted(list(languages)),
            'renderable_alignment_data': renderable_alignment_data},
          output_filename)
    else:
      assert(False)

  def MatchesInNormalForm(self):
    matches = []
    for match in self._matches:
      rendered_match = sorted(['(%s,%s)' % (lang.GetCode(), sentence_id)
                               for lang, sentence_id in match])
      matches.append(','.join(rendered_match))
    return matches

  def Evaluate(self, reference_alignment):
    common = len(set(reference_alignment.MatchesInNormalForm()) &
                 set(self.MatchesInNormalForm()))

    LogDebugFull("alignment=%s, reference=%s",
             str(self.MatchesInNormalForm()),
             str(reference_alignment.MatchesInNormalForm()))

    if self.GetMatches():
      precision = float(common) / float(len(self.GetMatches()))
    else:
      precision = 0.0

    if reference_alignment.GetMatches():
      recall = float(common) / float(len(reference_alignment.GetMatches()))
    else:
      recall = 0.0

    if precision + recall > 0:
      f_measure = 2.0 * (precision * recall) / (precision + recall)
    else:
      f_measure = 0.0

    LogDebug("Single alignment evaluation: precision=%.3f, recall=%.3f,"
            " f_measure=%.3f, length1=%.3f, length2=%.3f",
            precision,
            recall,
            f_measure,
            len(self.GetMatches()),
            len(reference_alignment.GetMatches()))

    return {'precision': precision,
            'recall': recall,
            'f_measure': f_measure}
