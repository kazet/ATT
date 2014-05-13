#!/usr/bin/python

import os
import sys
import nltk
import argparse
from att.aligner import AlignerFactory
from att.dictionary import DictionaryFactory
from att.eta_clock import ETAClock
from att.html import CopyDependencies
from att.utils import MkdirIfNotExists, StripNonFilenameCharacters
from att.log import LogDebug
from att.pickle import LoadFromFile
from att.corpus import CorpusFactory
from att.global_context import global_context

def main():
  parser = argparse.ArgumentParser(description='Align a multilingual corpus'
                                               ' and write the output in the'
                                               ' TMX format.')
  parser.add_argument('--dictionary',
                      help="The location of the aligner dictionary.",
                      required=True)
  parser.add_argument('--trained_aligner',
                      help="Trained aligner (written by train.py) to load.")
  parser.add_argument('--aligner_configuration',
                      help="Configuration of an aligner that doesn't require"
                           " training.")
  parser.add_argument('--corpus',
                      help="The corpus that you want to be aligned.",
                      required=True)
  parser.add_argument('--output_folder',
                      help="The location of the alignment output.",
                      required=True)
  parser.add_argument('--verbose', '-v',
                      action='count',
                      default=0,
                      help="Determines verbosity level (none, -v, -vv or"
                           " -vvv). none: prints errors/warnings (default),"
                           " -v - prints basic information, -vv: prints debug"
                           " data, -vvv: prints everything.")
  args = parser.parse_args(sys.argv[1:])
  global_context.SetArgs(args)

  current_directory = os.path.dirname(__file__)
  nltk.data.path.append(os.path.join(current_directory, "venv/nltk_data"))

  LogDebug("[align.py] loading corpus...")
  corpus = CorpusFactory.MakeFromFile(args.corpus)
  LogDebug("[align.py] loading dictionary...")
  dictionary = DictionaryFactory.MakeFromFile(args.dictionary)
  LogDebug("[align.py] loading aligner...")
  if args.trained_aligner:
    aligner = LoadFromFile(args.trained_aligner)
  elif args.aligner_configuration:
    aligner = AlignerFactory.MakeFromFile(args.aligner_configuration)
  else:
    assert(False)
  LogDebug("[align.py] aligning...")
  MkdirIfNotExists(args.output_folder)
  identifiers = list(corpus.GetMultilingualDocumentIdentifiers())
  LogDebug("[align.py] %d document(s) to align..." % len(identifiers))
  eta_clock = ETAClock(0, len(identifiers), "Aligning corpus")
  for identifier in identifiers:
    output_path = os.path.join(
        args.output_folder,
        '%s.tmx' % StripNonFilenameCharacters(identifier))

    mdoc = corpus.GetMultilingualDocument(identifier)
    if mdoc.NumDocuments() > 0:
      aligner \
          .Align(mdoc, dictionary) \
          .RenderTMX(identifier, output_path)
    eta_clock.Tick()

if __name__ == "__main__":
    main()
