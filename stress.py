f = open('zaliznyak.txt', encoding = 'utf-8')
a = True

word_normal_form_list = {}
i = 0

while True:
      a = f.readline().strip()
      
      if not a:
            break
      a, b = a.split('#')
      b = b.split(',')
      n = b[0]
      
      word_normal_form_list[a] = b
      i += 1

      if i == 10_000:
            print(a)
            i = 0
            
print('SUCC')

import pickle

pickle.dump(word_normal_form_list,
            open('normal_stresses.pkl', 'wb'))
