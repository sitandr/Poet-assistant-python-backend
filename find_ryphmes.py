import argparse
import platform
import coefficients
from coefficients import basic_fields
import sys

# to build:
# pyinstaller find_ryphmes.py -F --add-data res;res --add-data config;config -i "NONE"

def decode(s):
      return s.encode('utf-8', 'surrogateescape').decode('1251')


parser = argparse.ArgumentParser(description =
                                 '''Compex tool for finding ryphms;
List of parts of speech (буквы везде русские):
с      существительное
п      прилагательное
мс     местоимение-существительное
мс-п   местоименное-прилагательное
г      глагол
н      наречие
числ   числительное
числ-п счётное прилагательное
вводн  вводное слово
межд   межометие
предик предикатив
предл  предлог
союз   союз
сравн  сравнительная степень
част   частица
?      куски фразеологизмов и т.п.

Fields available:
''' + ', '.join(basic_fields.keys()),
                                 formatter_class = argparse.RawTextHelpFormatter)

parser.add_argument('to_find', type = str, help = 'what to to find')
parser.add_argument('--mean', type = str, help = '''set meaning by fields&synonyms;
separated with "+"; for example, "сильный" or "Dark + Epic"''')
parser.add_argument('--rps', type = str, help = 'remove parts of speech; separated by "+"')
parser.add_argument('--log', type = str, help = 'where to write log')

debug = False

if debug:
      args = ["сло'во", "--mean", "Battle", '--rps', 'NOUN']
      args = parser.parse_args(args)
else:
      args = parser.parse_args()
      
if platform.python_implementation() == 'PyPy':
      args.to_find = decode(args.to_find)
      if args.mean: args.mean = decode(args.mean)
      if args .rps: args.rps  = decode(args.rps)

import finder

if args.log:
      print_ = print
      def print(*text):
            log_file = open(args.log, 'a', encoding = 'utf-8')
            print_(*text, file = log_file)
            log_file.close()
      
      coefficients.print = print
                
to_find = args.to_find
if "'" not in to_find and 'ё' not in to_find and '`' not in to_find:
      print("Please, mind the stress!")
      if args.log: print('end')
      sys.exit(1)


remove = args.rps.replace(' ', '').split('+') if args.rps else []

best = finder.get_best_by_transcription(to_find, remove)

field = []
if args.mean:
      args.mean = args.mean.replace(' ', '')
      for i in args.mean.split('+'):
            if i in basic_fields:
                  field.extend(basic_fields[i])
            else:
                  field.append(i)

found = finder.get_best(best, words_syn = field, exclude = [to_find])
print('; '.join(found))
if args.log: print('end') 
