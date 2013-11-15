"""Convert an aligned corpus to a dictionary."""

import os
import sys
import math
import string
import argparse
import subprocess
from nltk import word_tokenize

from att.utils import DictInc, DictIncMultiple
from att.log import LogDebug
from att.utils import TupleSplit
from att.eta_clock import ETAClock
from att.language import Languages
from att.pickle import LoadFromFile
from att.corpus import CorpusFactory
from att.html import CopyDependencies
from att.global_context import global_context
from att.utils import MkdirIfNotExists, StripNonFilenameCharacters

def FilterNotAlnum(s):
  r = ''
  for c in s:
    if c in string.letters or c in string.digits or c == ' ':
      r += c
  return r

def main():
  parser = argparse.ArgumentParser(description='Create a dictionary from an aligned corpus.')
  parser.add_argument('--corpus',
                      help="The corpus that you want to convert to a dictionary.",
                      required=True)
  parser.add_argument('--sentence_size_limit',
                      help="The maximum size of a sentence in corpus (in"
                           " words). Longer sentences will be trimmed to"
                           " minimize the effects of the quadratic time"
                           " complexity of a part of the algorithm.",
                      type=int,
                      default=50)
  parser.add_argument('--output',
                      help="The location of the output dictionary.",
                      required=True)
  parser.add_argument('--verbose', '-v',
                      action='count',
                      default=0,
                      help="Determines verbosity level (none, -v, -vv or"
                           " -vvv). none: prints errors/warnings (default),"
                           " -v - prints some information, -vv: prints debug"
                           " data, -vvv: prints everything.")

  args = parser.parse_args(sys.argv[1:])
  global_context.SetArgs(args)

  english = Languages.GetByCode('en')
  corpus = CorpusFactory.MakeFromFile(args.corpus)
  output = open('%s-temp' % args.output, 'w')
  eta_clock = ETAClock(0, len(list(corpus.GetMultilingualDocumentIdentifiers())))
  num_occurencies = {}
  lines = 0
  for mdoc in corpus.GetMultilingualDocumentIdentifiers():
    alignment = corpus.GetMultilingualAlignedDocument(mdoc)
    for match in alignment.GetMatches():
      per_lang = {}
      for lang, sent in match:
        per_lang[lang] = alignment.GetMultilingualDocument().GetSentence(lang, sent)
        if not lang in num_occurencies:
          num_occurencies[lang] = {}
      if not english in per_lang:
        continue
      english_words = word_tokenize(FilterNotAlnum(per_lang[english]))
      for lang, sentid_foreign in match:
        if lang == english:
          continue
        DictIncMultiple(
            num_occurencies[english],
            english_words[:args.sentence_size_limit])
        sent_foreign = alignment.GetMultilingualDocument().GetSentence(lang, sentid_foreign)
        for word_foreign in word_tokenize(sent_foreign)[:args.sentence_size_limit]:
          DictInc(
              num_occurencies[lang],
              word_foreign)
          for word_english in english_words[:args.sentence_size_limit]:
            output.write(("%s\t%s\t%s\n" % (word_english.lower(),
                                           word_foreign.lower(),
                                           lang.GetCode())).encode('utf-8'))
            lines += 1
    eta_clock.Tick()
  output.close()
  subprocess.call(["sort",
                   '%s-temp' % args.output,
                   '--buffer-size=1G',
                   '-o',
                   args.output])

  output = {}
  for language in corpus.GetLanguages():
    output[language] = open('%s-%s' % (args.output, language.GetCode()), 'w')

  def EmitWord(word_english, cnts):
    if num_occurencies[english].get(word_english, 0) < 30:
      return
    for lang in cnts.keys():
      if lang == english:
        continue
      for word_foreign, count_both in cnts[lang].iteritems():
        if num_occurencies[lang].get(word_foreign, 0) < 30:
          continue
        k = count_both * 2 / float(num_occurencies[english][word_english] +
                                   num_occurencies[lang][word_foreign])
        if k > 0.05:
          output[lang].write("%.3f\n%s\t%s\n" % (
              k,
              word_english.encode('utf-8'),
              word_foreign.encode('utf-8')))

  last = None
  cnts = {}
  eta_clock = ETAClock(0, lines)
  for line in open(args.output):
    word_english, word_foreign, lang_code = TupleSplit(line.strip().decode('utf-8'), '\t', 3)
    if last and last != word_english:
      EmitWord(last, cnts)
      for lang in cnts.keys():
        del cnts[lang]
    lang = Languages.GetByCode(lang_code)
    if not lang in cnts:
      cnts[lang] = {}
    DictInc(cnts[lang], word_foreign)
    last = word_english
    eta_clock.Tick()
  EmitWord(last, cnts)
  for lang in corpus.GetLanguages():
    output[lang].close()

if __name__ == "__main__":
    main()
