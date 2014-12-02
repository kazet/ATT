#!/usr/bin/python

import cgi
import os
import sys
import nltk
import argparse

from att.corpus import CorpusFactory
from att.dictionary import DictionaryFactory
from att.eta_clock import ETAClock
from att.global_context import global_context
from att.html import CopyDependencies
from att.language import Languages
from att.log import LogInfo
from att.pickle import LoadFromFile
from att.tmx import LoadTMXAlignedDocument
from att.utils import \
    RecursiveListing, \
    HasExtension, \
    StripNonFilenameCharacters, \
    MkdirIfNotExists

def main():
  parser = argparse.ArgumentParser(description='Render an alignment to HTML.')
  parser.add_argument('--input_folder',
                      help="A folder containing aligned documents (in TMX"
                           " format) to render.",
                      required=True)
  parser.add_argument('--output_folder',
                      help="The location of the output.",
                      required=True)
  parser.add_argument('-l', '--languages',
                      nargs='+',
                      help="The languages you want to extract from the aligned"
                           " documents (eg. -l pl en de)",
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

  filenames = RecursiveListing(args.input_folder)
  languages = Languages.GetMultipleByCode(args.languages)

  LogInfo("Rendering %s%s in %s to %s",
          ' '.join(filenames[:5]),
          "..." if len(filenames) > 5 else "",
          ', '.join(map(str, languages)),
         args.output_folder)

  CopyDependencies(['common.css', 'alignment_render.css'], args.output_folder)

  list_file = open(os.path.join(args.output_folder, "index.html"), 'w')
  list_file.write("<html><body>")
  for filename in filenames:
    filename = cgi.escape(StripNonFilenameCharacters(filename[len(args.input_folder):]))
    list_file.write("<a href='%s.html'>%s.html</a><br/>" % (
      filename,
      filename))
  list_file.write("</body></html>");
  list_file.close()

  eta_clock = ETAClock(0, len(filenames), "Rendering")
  for filename in filenames:
    LogInfo("Rendering %s", filename)
    if HasExtension(filename, '.tmx'):
      assert(filename[:len(args.input_folder)] == args.input_folder)

      identifier = StripNonFilenameCharacters(filename[len(args.input_folder):])
      aligned_doc = LoadTMXAlignedDocument(filename, languages)
      output_file_path = os.path.join(
          args.output_folder,
          '%s.html' % identifier)
      aligned_doc.RenderHTML(identifier, output_file_path, languages)
    eta_clock.Tick()

if __name__ == "__main__":
    main()
