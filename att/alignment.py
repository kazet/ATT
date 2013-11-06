import textwrap
from att.html import RenderTemplate
from att.log import LogDebug, LogInfo


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

  def RenderHTML(self, identifier, output_filename):
    def AddUnmatchedSentences(alignment_data, last_matched_sentences, position):
      max_skip = 0
      for lang, sentence_id in position:
        max_skip = max(max_skip, sentence_id - last_matched_sentences[lang])

      for i in range(1, max_skip):
        unmatched_row = []
        for lang, unused_sentence_id in match:
          if last_matched_sentences[lang] + i < sentence_id:
            unmatched_row.append( (lang, last_matched_sentences[lang] + i ) )
        alignment_data.append( (False, unmatched_row) )

    alignment_data = []
    last_matched_sentences = {}
    languages = set()
    for match in self._matches:
      for lang, sentence_id in match:
        languages.add(lang)

    for language in languages:
      last_matched_sentences[language] = 0

    for match in self._matches:
      AddUnmatchedSentences(alignment_data, last_matched_sentences, match)
      alignment_data.append( (True, match) )

      for lang, sentence_id in match:
        if last_matched_sentences[lang] > sentence_id:
          raise Exception("Non-monotonic alignment printing is not supported")
        last_matched_sentences[lang] = sentence_id

    sentence_nums = [(language, self._multilingual_document.NumSentences(language))
                     for language in languages]
    AddUnmatchedSentences(alignment_data, last_matched_sentences, sentence_nums)
    print sentence_nums
    renderable_alignment_data = []
    for is_matched, row in alignment_data:
      sentences = {}
      for language in languages:
        sentences[language] = (u'N/A', u'')
      for language, sent_id in row:
        if sent_id < self._multilingual_document.NumSentences(language):
          sentences[language] = (sent_id, self \
              ._multilingual_document \
              .GetDocument(language) \
              .GetSentence(sent_id))
      renderable_alignment_data.append(
          ( is_matched,
            sorted(sentences.iteritems())))

    result = RenderTemplate(
        'alignment_render.html',
        { 'identifier': identifier,
          'languages': sorted(list(languages)),
          'renderable_alignment_data': renderable_alignment_data},
        output_filename)

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

    LogDebug("alignment=%s, reference=%s",
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

    LogInfo("Single alignment evaluation: precision=%.3f, recall=%.3f,"
            " f_measure=%.3f, length1=%.3f, length2=%.3f",
            precision,
            recall,
            f_measure,
            len(self.GetMatches()),
            len(reference_alignment.GetMatches()))

    return {'precision': precision,
            'recall': recall,
            'f_measure': f_measure}
