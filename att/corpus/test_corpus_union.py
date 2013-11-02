from corpus_union import CorpusUnion
from att.test import TestCase

class CorpusUnionTestCase(TestCase):
  def test_get_multilingual_documents(self):
    corpus = CorpusUnion({
        'corpora': [
            {'class': 'MockCorpus',
             'multilingual_documents': [
                 {'identifier': 'id1', 'multilingual_document': 'document1'},
                 {'identifier': 'id2', 'multilingual_document': 'document2'}]},
            {'class': 'MockCorpus',
             'multilingual_documents': [
                 {'identifier': 'id3', 'multilingual_document': 'document3'},
                 {'identifier': 'id4', 'multilingual_document': 'document4'}]}]
        })
    self.assertUnorderedEqual(
        corpus.GetMultilingualDocuments(),
        ['document1', 'document2', 'document3', 'document4'])
