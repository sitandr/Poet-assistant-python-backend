import time

def timer(name = None):
      t = time.time()
      
      if hasattr(timer, 'previous'):
            if name:
                  print(name, t - timer.previous)
            else:
                  timer.n += 1
                  print(timer.n, t - timer.previous)
            
      else:
            timer.n = 0
            
      timer.previous = t
