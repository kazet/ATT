from corpus_skip import CorpusSkip
from att.test import TestCase

class CorpusSkipTestCase(TestCase):
  def test_get_multilingual_documents(self):
    corpus = CorpusSkip({
        'corpus': {
            'class': 'MockCorpus',
            'multilingual_documents': [
                {'identifier': 'id1', 'multilingual_document': 'document1'},
                {'identifier': 'id2', 'multilingual_document': 'document2'}]},
        'n': 1})
    self.assertUnorderedEqual(corpus.GetMultilingualDocuments(), ['document2'])
