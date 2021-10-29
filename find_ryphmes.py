import argparse

def decode(s):
      return s.encode('utf-8', 'surrogateescape').decode('1251')
parser = argparse.ArgumentParser(description = 'Compex tool for finding ryphms')

parser.add_argument('to_find', type = str, help = 'what to to find')
parser.add_argument('--mean', type = str, help = 'set meaning by fields&synonyms')
parser.add_argument('--rps', type = str, help = 'remove parts of speech')

args = parser.parse_args() # ["сло'во", "--mean", "Battle"]
args.to_find = decode(args.to_find)
args.mean = decode(args.mean)


import finder

to_find = args.to_find
all_forms_set = finder.filter_remove_parts_of_speech([])
best = finder.get_best_by_transcription(to_find, all_forms_set)

field = []
if args.mean:
      for i in args.mean.split('+'):
            if i in finder.basic_fields:
                  field.extend(finder.basic_fields[i])
            else:
                  field.append(i)

print(finder.get_best(best, words_syn = field, exclude = [to_find]))

