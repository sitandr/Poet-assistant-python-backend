import pickle as pkl

zaliz_1 = pkl.load(open('zaliz_1.pkl', 'rb'))
zaliz_2 = pkl.load(open('zaliz_2.pkl', 'rb'))

zaliz = {**zaliz_1, **zaliz_2}
#del zaliz_1, zaliz_2

filtered = {}
#get = ['с', 'п']

def format_stress(s):
      return s.replace('̀', "`").replace('́', "'")

for word in zaliz:
      filtered[word] = {}
      
      if type(zaliz[word]) == list:
            zaliz[word] = zaliz[word][0]
            
      if type(zaliz[word]) == list:
            zaliz[word] = zaliz[word][0]
            
      for key in zaliz[word]:
            if key[0] == 'о' or key == 'п':
                  filtered[word][key] = zaliz[word][key]
            elif key == 'с':
                  filtered[word][key] = zaliz[word][key]['т'] if 'т' in zaliz[word][key] else '?'

            if key == 'п':
                  keys = set(filter(lambda t: not ('-' in t or '?' in t), zaliz[word][key].split(';')))
                  filtered[word][key] = ';'.join(keys)
                  
      filtered[word] = format_stress('+'.join(filtered[word].values()))

pkl.dump(filtered, open('min_zaliz.pkl', 'wb'))
