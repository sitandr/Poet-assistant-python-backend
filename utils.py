import time

def timer(name = None, supress_print = False):
      t = time.time()

      if not supress_print:
            
            if hasattr(timer, 'previous'):
                  if name:
                        print(name, t - timer.previous)
                  else:
                        timer.n += 1
                        print(timer.n, t - timer.previous)
            else:
                  timer.n = 0
            
      timer.previous = t
