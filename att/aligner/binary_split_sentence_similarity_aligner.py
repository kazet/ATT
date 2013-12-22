from copy import deepcopy
from unidecode import unidecode

from att.utils import Average
from att.alignment import Alignment
from att.document import Document
from att.language import Languages
from att.log import LogDebug
from att.multilingual_document import MultilingualDocument
from att.aligner.aligner import Aligner
from att.aligner.aligner_factory import AlignerFactory
from att.aligner.combined_dynamic_sentence_similarity_aligner import \
    CombinedDynamicSentenceSimilarityAligner

@AlignerFactory.Register
class BinarySplitSentenceSimilarityAligner(Aligner):
  def __init__(self, config):
    super(BinarySplitSentenceSimilarityAligner, self).__init__(config)

    self._languages = [Languages.GetByCode(code)
                       for code in config['languages']]
    self._child_aligner = CombinedDynamicSentenceSimilarityAligner(config)
    self._min_num_sentences_to_split = config.get('min_num_sentences_to_split', 6)

  def Train(self, training_corpus, training_set_size, dictionary):
    return self._child_aligner.Train(
        training_corpus,
        training_set_size,
        dictionary)

  def Align(self, multilingual_document, dictionary, level=0, ready_sentence_baselines=None):
    def IdentedLogDebug(*args):
      LogDebug('  ' * level + args[0], *args[1:])
    doc_sizes = [doc.NumSentences()
                 for doc in multilingual_document.GetDocuments().values()]
    IdentedLogDebug("Aligning: min doc size=%d, max doc size=%d",
                    min(doc_sizes),
                    max(doc_sizes))
    self._min_num_sentences_to_split = 20

    if ready_sentence_baselines:
      sentence_baselines = ready_sentence_baselines
    else:
      sentence_baselines = self._child_aligner \
          ._CalculateSentenceBaselines(multilingual_document, dictionary)

    if min(doc_sizes) < self._min_num_sentences_to_split:
      return self._child_aligner.Align(
            multilingual_document,
            dictionary,
            sentence_baselines)

    best_cut = None
    best_cut_quality = 0
    for start_language in self._languages:
      sentences_in_start_language = \
          xrange(multilingual_document.NumSentences(start_language))
      for start_sentence_id in sentences_in_start_language:
        cut_quality = 0
        cut = { start_language: start_sentence_id }
        for language in self._languages:
          if language == start_language:
            continue
          best_sentence_id = None
          best_sentence_quality = 0
          for sentence_id in xrange(multilingual_document.NumSentences(language)):
            quality = 0
            start_sent_content = multilingual_document.GetSentence(
                start_language,
                start_sentence_id)
            sent_content = multilingual_document.GetSentence(
                language,
                sentence_id)
            match_baseline = sentence_baselines[(start_language, start_sent_content)] * \
                             sentence_baselines[(language, sent_content)]
            quality += match_baseline * self._child_aligner.GetMatchProbability(
                multilingual_document,
                start_language, start_sentence_id,
                language, sentence_id,
               dictionary)
            if quality > best_sentence_quality:
              best_sentence_id = sentence_id
              best_sentence_quality = quality
          if best_sentence_id is not None:
            cut[language] = best_sentence_id
            cut_quality += best_sentence_quality
        if len(cut) == len(self._languages) and cut_quality > best_cut_quality:
          best_cut = cut
          best_cut_quality = cut_quality
    if best_cut is None:
      IdentedLogDebug("No cut found")
      return self._child_aligner.Align(
          multilingual_document,
          dictionary,
          sentence_baselines)
    IdentedLogDebug("Cut found: from match %s", ', '.join([
        "%s: %d, `%s'" % (
          lang,
          sid,
          unidecode(unicode(
              multilingual_document.GetSentence(lang, sid)[:20]
              .replace('\n', ''))))
        for lang, sid in best_cut.items()]))
    IdentedLogDebug("Cut found: min quality=%.3f",
        best_cut_quality)

    # ok, now we can divide each document in multilingual_document into two
    # document and align each of them
    documents_1 = []
    documents_2 = []
    for language in self._languages:
      document_1 = []
      document_2 = []

      for sentence_id in xrange(multilingual_document.NumSentences(language)):
        if sentence_id < best_cut[language]:
          document_1.append(
            multilingual_document.GetSentence(
                language,
                sentence_id))
        elif sentence_id > best_cut[language]:
          document_2.append(
            multilingual_document.GetSentence(
                language,
                sentence_id))
        else:
          pass

      documents_1.append(Document(document_1, language))
      documents_2.append(Document(document_2, language))
    multilingual_document_1 = MultilingualDocument(documents_1)
    multilingual_document_2 = MultilingualDocument(documents_2)

    alignment_1 = self.Align(multilingual_document_1,
                             dictionary,
                             level + 1,
                             sentence_baselines)
    # The second Align sees only the second part of the document, so
    # it calls the best_cut[lang]+1-th sentence "the 0-th one".
    matches_2 = []
    for match in self.Align(multilingual_document_2,
                             dictionary,
                             level + 1,
                             sentence_baselines).GetMatches():
      corrected_match = []
      for lang, sid in match:
        corrected_match.append( (lang, sid + 1 + best_cut[lang]) )
      matches_2.append(corrected_match)

    # We've splitted the document into two ones and ignored the cut, so
    # we have to add it back to the alignment.
    cut_match = best_cut.items()

    return Alignment(
        multilingual_document,
        alignment_1.GetMatches() + [cut_match] + matches_2)
