"""See `SentenceSimilarityAligner: available signals', `Module conventions'
in the documentation."""

from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory \
  import SignalFactory
from att.aligner.sentence_similarity_signals.common_tokens_signal \
  import CommonTokensSignal
from att.aligner.sentence_similarity_signals.random_signal \
  import RandomSignal
from att.aligner.sentence_similarity_signals.lcs_signal \
  import LCSSignal
from att.aligner.sentence_similarity_signals.unique_tokens_signal \
  import UniqueTokensSignal
from att.aligner.sentence_similarity_signals.format_signal \
  import FormatSignal
from att.aligner.sentence_similarity_signals.size_ratio_signal \
  import SizeRatioSignal
from att.aligner.sentence_similarity_signals.token_start_signal \
  import TokenStartSignal
from att.aligner.sentence_similarity_signals.word_count_ratio_signal \
  import WordCountRatioSignal
from att.aligner.sentence_similarity_signals.punctuation_signal \
  import PunctuationSignal
from att.aligner.sentence_similarity_signals.dictionary_words_signal \
  import DictionaryWordsSignal
