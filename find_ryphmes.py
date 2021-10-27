import argparse

parser = argparse.ArgumentParser(description = 'Compex tool for finding ryphms')

parser.add_argument('to_find', type = str, help = 'what to to find')
parser.add_argument('--mean', type = str, help = 'set meaning by field/synonym')
parser.add_argument('--rps', type = str, help = 'remove parts of speech')

args = parser.parse_args() # ["сло'во", "--mean", "Battle"]
args.to_find = args.to_find.encode('utf-8', 'surrogateescape').decode('1251')

import finder

print(finder.get_best([(0, "сло'во"), (0, "сло'ва"), (0, "слава"), (0, "слева"), (0, "сла'вы")],
                      words_field = finder.basic_fields[args.mean]))

to_find = args.to_find
all_forms_set = finder.filter_remove_parts_of_speech([])
best = finder.get_best_by_transcription(to_find, all_forms_set)

if args.mean in finder.basic_fields:
      print(finder.get_best(best, words_field = finder.basic_fields[args.mean]))
else:
      print(finder.get_best(best, words_synonym = synonym))
