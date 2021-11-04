import pickle as pkl
import re

zaliz_1 = pkl.load(open('zaliz_1.pkl', 'rb'))
zaliz_2 = pkl.load(open('zaliz_2.pkl', 'rb'))

zaliz = {**zaliz_1, **zaliz_2}
#del zaliz_1, zaliz_2

filtered = {}
#get = ['с', 'п']

def format_stress(s):
      return s.replace('̀', "`").replace('́', "'")


no = ['?', 'част', 'союз', 'н', 'межд', 'вводн']
REMOVE_ANNOTATIONS = re.compile('(\[.*?\])|\(.*?\)')

for word in zaliz:
      filtered[word] = {}
      
      if type(zaliz[word]) == list:
            zaliz[word] = max(zaliz[word], key = len)
            
      if type(zaliz[word]) == list:
            zaliz[word] = max(zaliz[word], key = len)
            
      for key in zaliz[word]:
            if key[0] == 'о' or key == 'п':
                  filtered[word][key] = zaliz[word][key]
            elif key == 'с':
                  filtered[word][key] = zaliz[word][key]['т'] if 'т' in zaliz[word][key] else '?'

            if key == 'п':
                  string = zaliz[word][key].replace(',', ';')
                  keys = set(filter(lambda t: not ('(устар.)' in t or '-' in t or '?' in t), string.split(';')))
                  filtered[word][key] = ';'.join(keys)
                  filtered[word][key] = re.sub(REMOVE_ANNOTATIONS, '', filtered[word][key])
      
      assert 'с' in filtered[word]
      if not ('о' in filtered[word]):
            #print('o not in', word)
            del filtered[word]
            continue
      if not ('п' in filtered[word] or filtered[word]['с'] in no):
            print('п not in', word)
      
      
      filtered[word] = format_stress('+'.join(filtered[word].values()))

pkl.dump(filtered, open('min_zaliz.pkl', 'wb'))
