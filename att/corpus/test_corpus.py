from att.test import TestCase
from att.corpus import MockCorpus

class CorpusTestCase(TestCase):
  def test_get_multilingual_documents(self):
    corpus = MockCorpus({
      'multilingual_documents': [
          {'identifier': 'id1', 'multilingual_document': 'document1'},
          {'identifier': 'id2', 'multilingual_document': 'document2'}]})
    self.assertUnorderedEqual(corpus.GetMultilingualDocuments(),
                              ['document1', 'document2'])
